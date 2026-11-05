# Creates a NEXUS shortcut with the octopus icon on your Desktop.
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$desktop = [Environment]::GetFolderPath('Desktop')
$shell = New-Object -ComObject WScript.Shell
$lnk = $shell.CreateShortcut((Join-Path $desktop 'NEXUS.lnk'))
$lnk.TargetPath = Join-Path $dir 'run_nexus.bat'
$lnk.WorkingDirectory = $dir
$lnk.IconLocation = (Join-Path $dir 'assets\nexus.ico')
$lnk.Description = 'NEXUS Personal Automation Engine'
$lnk.Save()
Write-Host 'Done! NEXUS shortcut created on your Desktop.'
