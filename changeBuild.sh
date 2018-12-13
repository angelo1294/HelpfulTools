#!/bin/bash

$vcenter = $args[0]
$vel = $args[1]
$ite = $args[2]
$version = $args[3]
$user = $args[4]
$password = $args[5]

###Connect to vCenter###
Connect-VIServer -Server $vcenter -User $user -Password $password

###Get last build for Velocity###
$result = get-childitem vmstore:\Sunnyvale-Lab\live-iso\vel\${version}\build -Recurse -Include *.iso | Select Name
if( $result.length -gt 1 )
{
	$result = $($result.name | sort -n)
	$velBuild = $result[-1]
}
else
{
	$velBuild = $result.name
}
$velIso = "vel\${version}\build\${velBuild}"

# ###Get last build for ITE###
$result = get-childitem vmstore:\Sunnyvale-Lab\live-iso\ite\${version}\build -Recurse -Include *.iso | Select Name
if ( $result.length -gt 1 )
{
	$result = $($result.name | sort -n)
	$iteBuild = $result[-1]
}
else
{
	$iteBuild = $result.name
}
$iteIso = "ite\${version}\build\${iteBuild}"

###Power off ite and change build
if( $(get-vm $ite).PowerState -ne "PoweredOff" )
{
	stop-vm $ite -confirm:$false 
}
Get-CDDrive $ite | Set-CDDrive -IsoPath "[live-iso] ${iteIso}" -Confirm:$false

###Power off velo and change build
if( $(get-vm $vel).PowerState -ne "PoweredOff" )
{
	stop-vm $vel -confirm:$false
}

Get-CDDrive $vel | Set-CDDrive -IsoPath "[live-iso] ${velIso}" -Confirm:$false

###Power on ITE and wait for it to boot###
start-vm $ite -confirm:$false
sleep 120
###Power on Velocity once ITE is up and running###
start-vm $vel -confirm:$false

###Exit pwsh###
exit
