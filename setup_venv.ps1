# Script PowerShell para criar um virtual environment e instalar dependências
# Uso: abra o PowerShell na pasta do projeto e execute: .\setup_venv.ps1

param(
    [string]$venvName = "venv",
    [string]$pythonExe = "python"
)

Write-Host "Criando virtual environment '$venvName'..."
$venvPath = Join-Path -Path (Get-Location) -ChildPath $venvName

if (-Not (Test-Path $venvPath)) {
    & $pythonExe -m venv $venvPath
} else {
    Write-Host "Virtual environment já existe em: $venvPath"
}

# Ativar venv (PowerShell)
$activate = Join-Path -Path $venvPath -ChildPath "Scripts\Activate.ps1"
if (Test-Path $activate) {
    Write-Host "Ativando virtual environment..."
    & $activate
} else {
    Write-Host "Não foi possível encontrar o script de ativação: $activate"
}

# Atualizar pip
Write-Host "Atualizando pip..."
& $venvPath\Scripts\python.exe -m pip install --upgrade pip

# Instalar dependências
if (Test-Path "requirements.txt") {
    Write-Host "Instalando dependências de requirements.txt..."
    & $venvPath\Scripts\python.exe -m pip install -r requirements.txt
} else {
    Write-Host "requirements.txt não encontrado na pasta atual."
}

Write-Host "Concluído. Para ativar o venv em futuros shells execute:"
Write-Host "    .\$venvName\Scripts\Activate.ps1"
