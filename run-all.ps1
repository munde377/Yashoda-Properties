$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $root 'backend'
$frontendDir = Join-Path $root 'frontend'

function Resolve-Python {
    $paths = @(
        Join-Path $backendDir 'venv310\Scripts\python.exe',
        Join-Path $backendDir 'venv\Scripts\python.exe',
        Join-Path $root '.venv\Scripts\python.exe'
    )
    foreach ($path in $paths) {
        if (Test-Path $path) { return $path }
    }

    if (Get-Command py -ErrorAction SilentlyContinue) {
        return 'py -3.10'
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return 'python'
    }
    return $null
}

function Start-Terminal {
    param(
        [string]$WorkingDirectory,
        [string]$Command,
        [string]$WindowTitle
    )
    $cmd = "Set-Location '$WorkingDirectory'; $Command"
    Start-Process -FilePath 'powershell.exe' -ArgumentList "-NoExit", "-Command", $cmd -WindowStyle Normal
}

$python = Resolve-Python
if (-not $python) {
    Write-Error 'No Python interpreter found. Install Python 3.10+ and make sure py or python is on PATH.'
    exit 1
}

$backendPythonCommand = if ($python -match '\\python.exe$') { "& '$python' -m pip install -r requirements.txt; & '$python' -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" } else { "& $python -m pip install -r requirements.txt; & $python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" }

if (Get-Command npm -ErrorAction SilentlyContinue) {
    $frontendCommand = "if (-not (Test-Path 'node_modules')) { npm install }; npm run dev"
} elseif (Get-Command yarn -ErrorAction SilentlyContinue) {
    $frontendCommand = "if (-not (Test-Path 'node_modules')) { yarn install }; yarn dev"
} else {
    Write-Error 'npm or yarn not found. Install Node.js and make sure npm/yarn is on PATH.'
    exit 1
}

Start-Terminal -WorkingDirectory $backendDir -Command $backendPythonCommand -WindowTitle 'Backend'
Start-Terminal -WorkingDirectory $frontendDir -Command $frontendCommand -WindowTitle 'Frontend'

Write-Host 'Started backend and frontend in separate PowerShell windows.'
Write-Host 'Backend: http://localhost:8000'
Write-Host 'Frontend: http://localhost:5173'