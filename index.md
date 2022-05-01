## Ricardo's Script Locker

This page is used for easy access to all the scripts I have put together.

### [SaRACMDScript (Automated SaRA Command-Line Version)](https://github.com/ricardoMpacheco/SaRACMDScript)
This small script allows the process for the usage of the SaRA support tool command-line version to be as automated as possible.

More information about the orignal tool can be found here:
  https://docs.microsoft.com/en-us/office365/troubleshoot/administration/sara-command-line-version


### [Outlook Network Tests](https://github.com/ricardoMpacheco/ONT)

This powershell script will perform a range of connectivity tests to Office 365 to ensure that TCP connections via port 80 and 443 are happening without any issues. The tool achieves this by downloading PSPing and running it from the machine.
This script will also check the machine settings for proxy servers and at the end provide articles that can be helpfull for further understanding of recommendations and best practices related to networking configurations in Office 365

The script can be easily accessed / run by running the following powershell cmdlets:
```ps
$ONTScript = Invoke-WebRequest https://raw.githubusercontent.com/ricardoMpacheco/ONT/master/ONT.ps1
Invoke-Expression $($ONTScript.Content)
```
or by downloading it directly from the button to the right.




