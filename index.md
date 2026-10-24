## Ricardo's Script Locker

This page is used for easy access to all the scripts I have put together.

### Tracker de preços — Homycasa Vulcan

O tracker acompanha [este sofá e a variante selecionada](https://homycasa.pt/products/sofacantovulcan-sofa-de-canto-vulcan-relax-eletrico?variant=57783062004095).
Regista o preço em EUR, o preço de referência, a percentagem de desconto anunciada
e a disponibilidade num [histórico CSV](data/homycasa-vulcan.csv).
O histórico só passa a existir depois da primeira consulta bem-sucedida.

- **Automático:** o workflow **Homycasa price tracker** consulta diariamente às 08:00 UTC
  (09:00 em Portugal continental no horário de verão) e guarda o histórico neste repositório.
  O agendamento só fica ativo depois de o workflow estar na branch predefinida, com
  GitHub Actions ativo e permissões para escrever nessa branch.
- **Manual:** em **Actions → Homycasa price tracker → Run workflow**.
  O resumo da execução mostra o preço, o desconto e a variação desde a consulta anterior.
- **Local:** com Python 3.10 ou superior, executar `python3 tracker/homycasa.py`
  a partir da raiz do repositório. Não precisa de instalar bibliotecas.
  Para escolher outro histórico: `python3 tracker/homycasa.py --history /caminho/historico.csv`.
- **Testes:** `python3 -m unittest discover -s tests -v`.

O tracker usa o endpoint JSON público do produto (`.js`), esperando preços em cêntimos.
Se o site mudar esse formato, bloquear o acesso ou remover a variante, a consulta falha
sem registar um preço fictício. Não recupera preços anteriores à primeira execução.
Os descontos são calculados a partir do preço de referência da loja: não validam o
menor preço dos últimos 30 dias e não incluem cupões, portes ou campanhas no checkout.
Não são enviadas notificações de preço por email ou outros canais.
O acesso real ao site não pôde ser confirmado no ambiente de desenvolvimento;
é necessário confirmar a primeira execução manual.

### [SaRACMDScript (Automated SaRA Command-Line Version)](https://github.com/ricardoMpacheco/SaRACMDScript)
This small script allows the process for the usage of the SaRA support tool command-line version to be as automated as possible.

The script can be easily accessed / run by running the following powershell cmdlets:
```ps
$SaRACMDScript = Invoke-WebRequest https://raw.githubusercontent.com/ricardoMpacheco/SaRACMDScript/main/SaRACMDScript.ps1
Invoke-Expression ($SaRACMDScript.Content)
```
  
 <a href="https://docs.microsoft.com/en-us/office365/troubleshoot/administration/sara-command-line-version" target="_blank">More information about the orignal tool can be found in this article.</a>

### [Outlook Network Tests](https://github.com/ricardoMpacheco/ONT)

This powershell script will perform a range of connectivity tests to Office 365 to ensure that TCP connections via port 80 and 443 are happening without any issues. The tool achieves this by downloading PSPing and running it from the machine.
This script will also check the machine settings for proxy servers and at the end provide articles that can be helpfull for further understanding of recommendations and best practices related to networking configurations in Office 365

The script can be easily accessed / run by running the following powershell cmdlets:
```ps
$ONTScript = Invoke-WebRequest https://raw.githubusercontent.com/ricardoMpacheco/ONT/master/ONT.ps1
Invoke-Expression ($ONTScript.Content)
```
or by downloading it directly from the button to the right.


### [FiddlerChecker](https://github.com/ricardoMpacheco/FiddlerChecker)

FiddlerChecker allows it's user to understand if a Fiddler trace (.saz) file has been collected correctly (HTTPS Decryption was performed). It's under development the hability to understand without any additional type of knowledge, if the are observing EWS calls, MAPI calls or other errors are found within the Fiddler trace without actually opening it or inspecting it. Giving a small idea of the if the file will possibly contain valuable data or not.

The script can be access by downloading it directly from the button to the right. The password for the file is FiddlerChecker.

1.Export The files inside the zip

2.Double click the .bat file named "FiddlerChecker"

3.Follow the steps

