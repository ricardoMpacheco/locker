"""Track the advertised EUR price of the selected Homycasa sofa variant."""

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


PRODUCT_URL = (
    "https://homycasa.pt/products/"
    "sofacantovulcan-sofa-de-canto-vulcan-relax-eletrico"
)
VARIANT_ID = "57783062004095"
FIELDS = (
    "timestamp_utc", "variant_id", "price_eur", "compare_at_price_eur",
    "discount_percent", "available",
)
DEFAULT_HISTORY = Path(__file__).resolve().parents[1] / "data/homycasa-vulcan.csv"


def parse_variant(product):
    if not isinstance(product, dict) or not isinstance(product.get("variants"), list):
        raise ValueError("Resposta inválida: faltam as variantes do produto.")
    variant = next(
        (item for item in product["variants"]
         if isinstance(item, dict) and str(item.get("id")) == VARIANT_ID),
        None,
    )
    if variant is None:
        raise ValueError(f"A variante {VARIANT_ID} não foi encontrada.")

    price = variant.get("price")
    reference = variant.get("compare_at_price")
    if type(price) is not int or price <= 0:
        raise ValueError("Preço inválido: esperado um inteiro positivo em cêntimos.")
    if reference is not None and (type(reference) is not int or reference < 0):
        raise ValueError("Preço de referência inválido.")
    if type(variant.get("available")) is not bool:
        raise ValueError("Disponibilidade inválida.")

    price = Decimal(price) / 100
    reference = Decimal(reference) / 100 if reference else None
    discount = (
        (reference - price) * 100 / reference
        if reference and reference > price else Decimal(0)
    )
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "variant_id": VARIANT_ID,
        "price_eur": f"{price:.2f}",
        "compare_at_price_eur": f"{reference:.2f}" if reference else "",
        "discount_percent": f"{discount:.2f}",
        "available": str(variant["available"]).lower(),
    }


def fetch_observation():
    request = Request(
        PRODUCT_URL + ".js",
        headers={"Accept": "application/json", "User-Agent": "LockerPriceTracker/1.0"},
    )
    with urlopen(request, timeout=30) as response:
        product = json.load(response)
    return parse_variant(product)


def record_observation(path, observation):
    previous = None
    if path.exists() and path.stat().st_size:
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != list(FIELDS):
                raise ValueError("Cabeçalho do histórico inválido; ficheiro não alterado.")
            for row in reader:
                if row["variant_id"] != VARIANT_ID:
                    raise ValueError("O histórico contém outra variante.")
                previous = row
    if previous:
        try:
            old_price = Decimal(previous["price_eur"])
            if not old_price.is_finite() or old_price <= 0:
                raise ValueError("Preço inválido no histórico.")
        except (ArithmeticError, TypeError) as error:
            raise ValueError("Preço inválido no histórico.") from error

    path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        if needs_header:
            writer.writeheader()
        writer.writerow(observation)
    return previous


def describe(observation, previous):
    lines = [
        "### Homycasa — sofá de canto Vulcan",
        f"- Preço: {observation['price_eur']} EUR",
        f"- Desconto anunciado: {observation['discount_percent']}%",
        "- Disponível: " + ("sim" if observation["available"] == "true" else "não"),
    ]
    if previous:
        difference = Decimal(observation["price_eur"]) - Decimal(previous["price_eur"])
        lines.append(f"- Variação desde a última consulta: {difference:+.2f} EUR")
        if observation["compare_at_price_eur"] != previous["compare_at_price_eur"]:
            lines.append("- O preço de referência da promoção mudou.")
    else:
        lines.append("- Primeira consulta: criada a referência para comparações futuras.")
    lines.append(f"- [Ver artigo e variante]({PRODUCT_URL}?variant={VARIANT_ID})")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", type=Path, default=DEFAULT_HISTORY)
    args = parser.parse_args()
    try:
        observation = fetch_observation()
        previous = record_observation(args.history, observation)
    except (OSError, URLError, ValueError, csv.Error) as error:
        print(f"Não foi possível atualizar o tracker: {error}", file=sys.stderr)
        return 1
    print(describe(observation, previous))
    return 0


if __name__ == "__main__":
    sys.exit(main())
