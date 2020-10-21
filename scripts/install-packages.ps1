[cmdletbinding()]
Param()


try {
    $ErrorActionPreference = "Stop"

    #
    # Install packages
    #
    Write-Verbose "Install Chocolatey"
    $url = 'https://chocolatey.org/install.ps1'
    Invoke-Expression ((new-object net.webclient).DownloadString($url))

    Write-Host "Install 7zip"
    choco install --limit-output -y 7zip

    Write-Host "Install awscli"
    choco install --limit-output -y awscli

    Write-Host "Install Chrome"
    choco install --limit-output --ignore-checksums -y googlechrome

    Write-Host "Install Steam"
    choco install --limit-output -y steam

    Write-Host "Install Parsec"
    choco install --limit-output -y parsec

    Write-Host "choco installs complete"
}
catch {
    Write-Host "catch: $_"
    $_ | Write-AWSQuickStartException
}
