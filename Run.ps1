$currentDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition

$pythonRunScript = Join-Path -Path $currentDirectory -ChildPath '\run.py'

$pythonPath = Join-Path -Path $currentDirectory -ChildPath '\venv\scripts\python.exe'

$activateScriptPath = Join-Path -Path $currentDirectory -ChildPath '\venv\scripts\activate.ps1'

Invoke-Expression -Command $activateScriptPath

Invoke-Expression -Command "$pythonPath $pythonRunScript"

deactivate