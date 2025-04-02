if (Test-Path -Path '.\dist\hprsctool*.whl') {
    $wheel = Get-ChildItem -Path '.\dist\hprsctool*.whl' | Sort-Object -Property LastWriteTime -Descending | Select-Object -First 1
    $wheelPath = $wheel.FullName
    $wheelName = $wheel.Name
    
    Remove-Item dist\wheels -Force -Recurse
    mkdir dist\wheels

    $versionLine = Select-String -Path "pyproject.toml" -Pattern 'version = "([^"]+)"'
    $version = $versionLine.Matches.Groups[1].Value
    $bundle = "hprsctool-$version.zip"

    poetry export -f requirements.txt --output requirements.txt

    python -m pip download -r requirements.txt --prefer-binary -d .\dist\wheels\
    python -m pip download setuptools --prefer-binary -d .\dist\wheels\
    Copy-Item $wheelPath .\dist\wheels\

    $installScript = "python -m pip install --no-index --find-links .\wheels\ --no-cache-dir .\wheels\$wheelName"
    $installScriptPath = ".\dist\install.bat"
    $installScript | Out-File -FilePath $installScriptPath

    Compress-Archive -Path $installScriptPath,dist\wheels -DestinationPath $bundle -Force
    Write-Host "Bundle created at $bundle"
    exit 0
} else {
    Write-Host "Error: hprsctool wheel file not found in dist folder"
    exit 1
}