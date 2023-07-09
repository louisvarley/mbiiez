!#/bin/sh

#get script path here
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
OPENJKPATH="/opt/openjk"
MBIIPATH="$OPENJKPATH/MBII"
MACHINE_TYPE=`uname -m`

cd $SCRIPTPATH

if [ "$EUID" -ne 0 ]
  then echo "Installation requires root. Please run installation as root"
  exit
fi

show_menu(){
    normal=`echo "\033[m"`
    menu=`echo "\033[36m"` #Blue
    number=`echo "\033[33m"` #yellow
    admin=`echo "\033[32m"` #green
    bgred=`echo "\033[41m"`
    fgred=`echo "\033[31m"`
    printf "\n${menu}*************************************************${normal}\n"
    printf "${menu} 	 Moviebattles II EZ Installer Tool		\n"
    printf "${menu}*************************************************${normal}\n\n"
    printf "${menu}**${number} 1)${menu} Dependencies ${normal}\n"
    printf "${menu}**${number} 2)${menu} Python Tools ${normal}\n"
    printf "${menu}**${number} 3)${menu} MBII Dedicated Server${normal}\n"
    printf "${menu}**${number} 4)${menu} RTVRTM ${normal}\n"
    printf "${menu}**${number} 5)${menu} Install Dotnet${normal}\n"
    printf "${menu}**${number} 6)${menu} Install MBII Server Updater${normal}\n"
    printf "${menu}**${number} 7)${menu} Update MBII Server${normal}\n"
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
            option_picked "\n${menu} Installing System Dependencies...${normal}\n";
	if [ ${MACHINE_TYPE} == 'x86_64' ]; then
		dpkg --add-architecture i386
                apt-get update
		apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 zlib1g:i386 curl:i386 lib32z1 build-essential cmake gcc-multilib g++-multilib libjpeg-dev:i386 libpng-dev:i386 zlib1g-dev:i386
	else
                apt-get update
		apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 zlib1g:i386 curl:i386 lib32z1 build-essential cmake gcc-multilib g++-multilib libjpeg-dev:i386 libpng-dev:i386 zlib1g-dev:i386 
	fi
	   reset;
           show_menu;
        ;;
        2) clear;
            option_picked "\n${menu} Installing Python Tools...${normal}\n";
		apt-get update
		apt-get install python3-pip -y
		apt-get install -y net-tools
		apt-get install -y fping
		apt-get install -y python3
		apt-get install -y nano
		apt-get install -y python3-pip
		apt-get install -y unzip
		pip3 install watchgod --break-system-packages
		pip3 install tailer --break-system-packages
		pip3 install six --break-system-packages
		pip3 install psutil --break-system-packages
		pip3 install PTable --break-system-packages
		pip3 install ConfigParser --break-system-packages
		pip3 install pysqlite3 --break-system-packages
		pip3 install flask --break-system-packages
		pip3 install flask_httpauth --break-system-packages
		pip3 install discord.py --break-system-packages
		pip3 install prettytable --break-system-packages
	   reset;
           show_menu;
        ;;
        3) clear;
            option_picked "\n${menu} Installing Moviebattle II Server...${normal}\n";
 	if [ -d $MBIIPATH ]; then
		clear;
                printf "${menu} MovieBattles 2 Directory found...${normal}\n"
       		sleep 2
	else
        	clear;
        	printf "${menu} Downloading Movie Battles II...${normal}\n"
        	sleep 2

        #Download file lists, get the latest
        wget -O "$SCRIPTPATH/downloads" https://archive.moviebattles.org/releases/

        while IFS= read -r line; do

                SUB='FULL'
                if [[ "$line" == *"$SUB"* ]]; then
                  FILENAME=`echo "$line" | grep -io '<a href=['"'"'"][^"'"'"']*['"'"'"]' | sed -e 's/^<a href=["'"'"']//i' -e 's/["'"'"']$//i'`
                  LINK="https://archive.moviebattles.org/releases/$FILENAME"
                fi
        done < downloads

      		wget -O "$SCRIPTPATH/MBII.zip" $LINK
       		printf "${menu} Extracting Moviebattles 2 Zip file...${normal}\n"
       		unzip -o MBII.zip -d $OPENJKPATH
		rm MBII.zip
		cd $MBIIPATH

		mv -f jampgamei386.so jampgamei386.jamp.so
		cp jampgamei386.nopp.so jampgamei386.so

		cd $SCRIPTPATH

		rm -f /usr/bin/mbii 2> /dev/null
		ln -s $SCRIPTPATH/mbii.py /usr/bin/mbii
		chmod +x /usr/bin/mbii

		mkdir -p /root/.local/share/openjk/
		ln -s /opt/openjk /root/.local/share/openjk/

		# Copies Binaries so you can run mbiided.i386 as your engine
		cp $SCRIPTPATH/mbiided.i386 /usr/bin/

		chmod +x /usr/bin/mbiided.i386

	fi
           reset;
           show_menu;
        ;;
        4) clear;
            option_picked "\n${menu} Installing RTVRTM...${normal}\n";
		cd $SCRIPTPATH
		
		cp rtvrtm.py $OPENJKPATH/  
		chmod +x $OPENJKPATH/rtvrtm.py
           reset;
           show_menu;
        ;;
        5) clear;
            option_picked "\n${menu} Installing Dotnet...${normal}\n";
                apt-get update
                apt-get install -y apt-transport-https dotnet-sdk-6.0

                rm /usr/local/bin/dotnet
                ln -s /usr/lib/dotnet/dotnet /usr/local/bin/dotnet

           reset;
           show_menu;
        ;;
        6) clear;
            option_picked "\n${menu} Installing MBII Server Updater...${normal}\n";
                wget https://www.moviebattles.org/download/MBII_CLI_Updater.zip
                unzip -o MBII_CLI_Updater.zip -d ./updater
                rm MBII_CLI_Updater.zip

           reset;
           show_menu;
        ;;
        7) clear;
            option_picked "\n${menu} Updating MBII Server...${normal}\n";
                cd $OPENJKPATH
                dotnet $SCRIPTPATH/updater/MBII_CommandLine_Update_XPlatform.dll

                cd $MBIIPATH
                mv -f jampgamei386.so jampgamei386.jamp.so
                cp jampgamei386.nopp.so jampgamei386.so

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
