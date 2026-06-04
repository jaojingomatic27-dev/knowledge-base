<#
.SYNOPSIS
  Register Windows scheduled task for daily pre-market news scan

.DESCRIPTION
  Runs 1 hour before US market open (9:30 AM ET).
  EDT (Mar-Nov): 08:30 ET = 20:30 Beijing time
  EST (Nov-Mar): 08:30 ET = 21:30 Beijing time
  Default: 20:30 local time, Mon-Fri.

.PARAMETER Time
  Execution time (HH:mm), default "20:30"

.PARAMETER PythonPath
  Python path, auto-detected if not specified

.EXAMPLE
  .\setup_scheduled_task.ps1
  .\setup_scheduled_task.ps1 -Time "21:30"
#>

param(
    [string]$Time = "20:30",
    [string]$PythonPath = ""
)

$ErrorActionPreference = "Stop"
$TaskName = "NewsPreMarketScanner"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$ScannerScript = Join-Path $ProjectRoot "code\daily_news_scanner.py"

# Auto-detect Python
if (-not $PythonPath) {
    $PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
}
if (-not $PythonPath) {
    $PythonPath = (Get-Command python3 -ErrorAction SilentlyContinue).Source
}
if (-not $PythonPath) {
    Write-Error "Python not found! Use -PythonPath to specify path."
    exit 1
}

Write-Host "============================================================"
Write-Host "  Register Pre-Market News Scanner Task"
Write-Host "============================================================"
Write-Host "  Task Name: $TaskName"
Write-Host "  Python:    $PythonPath"
Write-Host "  Script:    $ScannerScript"
Write-Host "  Schedule:  Daily $Time (Mon-Fri)"
Write-Host "============================================================"

# Check script exists
if (-not (Test-Path $ScannerScript)) {
    Write-Error "Script not found: $ScannerScript"
    exit 1
}

# Remove existing task with same name (ignore errors if not found)
cmd /c "schtasks /delete /tn `"$TaskName`" /f 2>nul"
$null = $LASTEXITCODE  # reset exit code

# Create scheduled task
$action = "python `"$ScannerScript`""

Write-Host "`nCreating task...`n"

$createCmd = "schtasks /create /tn `"$TaskName`" /tr `"$action`" /sc WEEKLY /d MON,TUE,WED,THU,FRI /st $Time /rl HIGHEST /f"
Write-Host $createCmd

$result = cmd /c "$createCmd 2>&1"
Write-Host $result

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nTask created successfully!"
    Write-Host ""
    Write-Host "Task details:"
    schtasks /query /tn $TaskName /v /fo LIST | Select-String -Pattern "TaskName|Status|Schedule|Start Time|Days|Command"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  View:  schtasks /query /tn $TaskName /v"
    Write-Host "  Run:   schtasks /run /tn $TaskName"
    Write-Host "  Delete: schtasks /delete /tn $TaskName /f"
    Write-Host ""
    Write-Host "NOTES:"
    Write-Host "  1. Task runs at local time $Time, Mon-Fri"
    Write-Host "  2. EDT (Mar-Nov): set Time=20:30 for 08:30 ET"
    Write-Host "  3. EST (Nov-Mar): set Time=21:30 for 08:30 ET"
    Write-Host "  4. To change time: .\setup_scheduled_task.ps1 -Time '21:30'"
} else {
    Write-Error "Failed to create task! Run PowerShell as Administrator."
    exit 1
}
