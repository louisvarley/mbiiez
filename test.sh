#!/bin/sh
#get script path
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
OPENJKPATH="/opt/openjk"
MBIIPATH="$OPENJKPATH/MBII"
FUSCHIA='\033[35m'
UNDERLINE='\033[4m'

cd $SCRIPTPATH

if [ "$EUID" -ne 0 ]
  then echo "Installation requires root. Please run installation as root"
  ##exit
fi

show_menu(){
    normal=`echo "\033[m"`
    menu=`echo "\033[36m"` #Blue
    number=`echo "\033[33m"` #yellow
    bgred=`echo "\033[41m"`
    fgred=`echo "\033[31m"`
    printf "\n${menu}*************************************************${normal}\n"
    printf "${menu} 	 Moviebattles II EZ Installer		\n"
    printf "${menu}*************************************************${normal}\n\n"
    printf "${menu}**${number} 1)${menu} Dependencies ${normal}\n"
    printf "${menu}**${number} 2)${menu} Python Tools ${normal}\n"
    printf "${menu}**${number} 3)${menu} MBIIWeb Tools${normal}\n"
    printf "${menu}**${number} 4)${menu} MBII Dedicated Server${normal}\n"
    printf "${menu}**${number} 5)${menu} RTVRTM ${normal}\n"
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
            option_picked "\n${menu} Installing System Dependencies...\n";
	    apt-get update 
	
	    dpkg --add-architecture i386
	    apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386
	    apt-get install -y zlib1g:i386 
	    apt-get install -y curl:i386 
	   clear;
           show_menu;
        ;;
        2) clear;
            option_picked "\n${menu} Installing Python Tools...\n";
		apt-get update
		apt-get install python3-pip -y
		apt-get install -y python-setuptools python-dev 
		apt-get install -y net-tools
		apt-get install -y fping
		apt-get install -y python3
		apt-get install -y nano
		apt-get install -y python3-pip
		apt-get install -y unzip
		pip3 install watchgod 
		pip3 install tailer
		pip3 install six
		pip3 install psutil
		pip3 install PTable
		pip3 install ConfigParser
		pip3 install pysqlite3
		pip3 install flask
		pip3 install flask_httpauth
		pip3 install discord.py
	   clear;
           show_menu;
        ;;
        3) clear;
            option_picked "\n${menu} Installing MBIIWeb Tools...\n";
		wget https://packages.microsoft.com/config/ubuntu/21.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
		dpkg -i packages-microsoft-prod.deb
		rm packages-microsoft-prod.deb

		apt-get update 
		apt-get install -y apt-transport-https
		apt-get install -y dotnet-sdk-5.0
		apt-get install -y dotnet-sdk-3.1

		servicefile="$SCRIPTPATH/mbii-web.service"
		cp $servicefile /lib/systemd/system/
		sed -i 's@WORKING_DIRECTORY@'"$SCRIPTPATH"'@g' /lib/systemd/system/mbii-web.service

		systemctl enable mbii-web
		service mbii-web start
	   clear;
    		printf "\n${menu}*************************************************${normal}\n"
		printf "${menu}Web Interface is available at http://0.0.0.0:8080\n"
		printf "${menu}Default Login Details are\n"
		printf "${menu}Username: ${FUSCHIA}Admin${NONE}\n"
		printf "${menu}Password: ${FUSCHIA}Admin${NONE}\n"
                printf "\n${menu}*************************************************${normal}\n"
                printf "Press any key to return back to the menu.\n"
		read -r _
		clear;
            show_menu;
        ;;
        4) clear;
            option_picked "\n${menu} Installing Moviebattle II Server...\n";
 	if [ -d $MBIIPATH ]; then
		clear;
                printf "${menu} MovieBattles 2 Directory found...\n"
       		sleep 2
	else

        	clear;
        	printf "${menu} Downloading Movie Battles II...\n"
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
       printf "${menu} Extracting Moviebattles 2 Zip file...\n"
       unzip -o MBII.zip -d $OPENJKPATH
fi
           clear;
           show_menu;
        ;;
        5) clear;
            option_picked "\n${menu} Installing something...\n";


           clear;
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
