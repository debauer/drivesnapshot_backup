#
# areWeAdmin Prüft ob wir admin sind und wenn nicht holen wir uns Admin rechte durch einen Shell Restart mit entsprechenden Rechten.
#

Function areWeAdmin{
	$Invocation=((Get-Variable MyInvocation).value).ScriptName 
	
    if ($Invocation -ne $null) { 
        $arg="-command `"& '"+$Invocation+"'`"" 
        $currentPrincipal = New-Object Security.Principal.WindowsPrincipal( [Security.Principal.WindowsIdentity]::GetCurrent() )
        if (!($currentPrincipal.IsInRole( [Security.Principal.WindowsBuiltInRole]::Administrator ))) {
            Write-Host "Houston we have a problem. Lets get root!"
            Start-Process "$psHome\powershell.exe" -Verb Runas -ArgumentList $arg 
            break 
        } 
        Else {
            Write-Host "Housten no more roots!"
        }
    }else { 
        return "OMG! Something went wrong and we dont know what!" 
        break 
    } 
}

areWeAdmin

# Leider absolute Pfade.
C:\Python33\python.exe E:\Workspace_priv\drivesnapshot_backup\./script.py