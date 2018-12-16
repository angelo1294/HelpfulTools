#!/bin/bash

#                          __    _                                   
#                     _wr""        "-q__                             
#                  _dP                 9m_     
#                _#P                     9#_                         
#               d#@                       9#m                        
#              d##                         ###                       
#             J###                         ###L                      
#             {###K                       J###K                      
#             ]####K      ___aaa___      J####F                      
#         __gmM######_  w#P""   ""9#m  _d#####Mmw__                  
#      _g##############mZ_         __g##############m_               
#    _d####M@PPPP@@M#######Mmp gm#########@@PPP9@M####m_             
#   a###""          ,Z"#####@" '######"\g          ""M##m            
#  J#@"             0L  "*##     ##@"  J#              *#K           
#  #"               `#    "_gmwgm_~    dF               `#_          
# 7F                 "#_   ]#####F   _dK                 JE          
# ]                    *m__ ##### __g@"                   F          
#                        "PJ#####LP"                                 
#  `                       0######_                      '           
#                        _0########_                                   
#      .               _d#####^#####m__              ,              
#       "*w_________am#####P"   ~9#####mw_________w*"                  
#           ""9@#####@M""           ""P@#####@M""  


POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -vcenter|--vcenter)
    vcenter="$2"
    shift # past argument
    shift # past value
    ;;
    -vel|--vel)
    vel="$2"
    shift # past argument
    shift # past value
    ;;
    -ite|--ite)
    ite="$2"
    shift # past argument
    shift # past value
    ;;
    -version|--version)
    version="$2"
    shift # past argument
    shift # past value
    ;;
    -user|--user)
    user="$2"
    shift # past argument
    shift # past value
    ;;
    -password|--password)
    password="$2"
    shift # past argument
    shift # past value
    ;;
    --default)
    DEFAULT=YES
    shift # past argument
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

###Verify powershell is installed###
if (! pwsh -v )
then
	#Install powershell
	wget -q https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb
	sudo dpkg -i packages-microsoft-prod.deb
	sudo apt-get update | echo Y
	sudo apt-get install -y powershell
	#Instal PowerCLI module
	pwsh -command  Install-Module VMware.PowerCLI -Scope CurrentUser
	pwsh -command Set-PowerCLIConfiguration -Scope User -ParticipateInCEIP \$false -Confirm:\$false
fi

###Execute script in powershell###
pwsh -file changeBuildPWSH.sh $vcenter $vel $ite $version $user $password
