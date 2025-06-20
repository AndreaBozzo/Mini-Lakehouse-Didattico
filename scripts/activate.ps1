# scripts/activate.ps1
$venv = poetry env info --path
& "$venv\Scripts\Activate.ps1"
