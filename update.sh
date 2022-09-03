!#/bin/sh

#get script path
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
OPENJKPATH="/opt/openjk"
MBIIPATH="$OPENJKPATH/MBII"
MACHINE_TYPE=`uname -m`

cd $SCRIPTPATH

if [ "$EUID" -ne 0 ]
  then echo "Installation requires root. Please run installation as root"
  ##exit
fi

show_menu(){
    normal=`echo "\033[m"`
    menu=`echo "\033[36m"` #Blue
    number=`echo "\033[33m"` #yellow
    admin=`echo "\033[32m"` #green
    bgred=`echo "\033[41m"`
    fgred=`echo "\033[31m"`
    printf "\n${menu}*************************************************${normal}\n"
    printf "${menu} 	 Moviebattles II EZ Server Tool Updater		\n"
    printf "${menu}*************************************************${normal}\n\n"
    printf "${menu}**${number} 1)${menu} Install Dependancies${normal}\n"
    printf "${menu}**${number} 2)${menu} Install MBII Server Updater${normal}\n"
    printf "${menu}**${number} 3)${menu} Update MBII Server${normal}\n"
    printf "${menu}**${number} 4)${menu} Fix Symbolic Links${normal}\n"
    printf "\n${menu}*************************************************${normal}\n"
    printf "Please enter a menu option and enter or ${fgred}x to exit. ${normal}"
    read opt
}

option_picked(){
    msgcolor=`echo "\033[01;31m"` # bold red
    normal=`echo "\033[00;00m"` # normal white
    message=${@:-"${normal}Error: No message passed"}
    printf "${msgcolor}${message}${normal}\n"
}



clear
show_menu
while [ $opt != '' ]
    do
    if [ $opt = '' ]; then
      exit;
    else
      case $opt in
        1) clear;
            option_picked "\n${menu} Installing Dependancies...${normal}\n";
                apt-get update
                apt-get install -y apt-transport-https
                wget -O "dotnet.tar.gz" https://download.visualstudio.microsoft.com/download/pr/4fd83694-c9ad-487f-bf26-ef80f3cbfd9e/6ca93b498019311e6f7732717c350811/dotnet-sdk-3.1.422-linux-x64.tar.gz
		mkdir -p dotnet && tar -xzvf dotnet.tar.gz -C dotnet
		ln -s /root/mbiiez/dotnet/dotnet /usr/local/bin/dotnet

	   reset;
           show_menu;
        ;;
        2) clear;
            option_picked "\n${menu} Installing MBII Server Updater...${normal}\n";
		wget https://www.moviebattles.org/download/MBII_CLI_Updater.zip
		unzip -o MBII_CLI_Updater.zip -d ./updater
		rm MBII_CLI_Updater.zip

	   reset;
           show_menu;
        ;;
        3) clear;
            option_picked "\n${menu} Updating MBII Server...${normal}\n";
                cd $OPENJKPATH
                dotnet $SCRIPTPATH/updater/MBII_CommandLine_Update_XPlatform.dll

                cd $MBIIPATH
	        mv -f jampgamei386.so jampgamei386.jamp.so
	        cp jampgamei386.nopp.so jampgamei386.so

           reset;
           show_menu;
        ;;
        4) clear;
            option_picked "\n${menu} Fixing Symbolics Links...${normal}\n";
                cd /root/.local/share/openjk/
		unlink openjk 
		mkdir -p /root/.local/share/openjk/
		ln -s /opt/openjk /root/.local/share/openjk/
           reset;
           show_menu;
        ;;
        x)exit;
        ;;
        \n)exit;
        ;;
        *)clear;
            option_picked "Pick an option from the menu";
            show_menu;
        ;;
      esac
    fi
done
