#!/bin/bash
# submenu

#get script path here
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
OPENJKPATH="openjk"
MBIIPATH="$OPENJKPATH/MBII"
MACHINE_TYPE=`uname -m`

cd $SCRIPTPATH

debian () {
  local PS3=$'\nPlease enter sub option: '
  local options=("Dependancies" "Python Tools" "MBII Server" "RTVRTM" "Dotnet" "MBII Updater" "Update MBII" "Back to main menu")
  local opt
  select opt in "${options[@]}"
  do
      case $opt in
          "Dependancies")
	if [ ${MACHINE_TYPE} == 'x86_64' ]; then
		sudo dpkg --add-architecture i386
                sudo apt-get update
		sudo apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 zlib1g:i386 curl:i386 lib32z1 build-essential cmake gcc-multilib g++-multilib libjpeg-dev:i386 libpng-dev:i386 zlib1g-dev:i386
	else
                sudo apt-get update
		sudo apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 zlib1g:i386 curl:i386 lib32z1 build-essential cmake gcc-multilib g++-multilib libjpeg-dev:i386 libpng-dev:i386 zlib1g-dev:i386 
	fi
              ;;
          "Python Tools")
		sudo apt-get update
		sudo apt-get install -y python-is-python3
		sudo apt-get install python3-pip -y
		sudo apt-get install -y net-tools
		sudo apt-get install -y fping
		sudo apt-get install -y python3
		sudo apt-get install -y nano
		sudo apt-get install -y python3-pip
		sudo apt-get install -y unzip
		sudo pip3 install watchgod --break-system-packages
		sudo pip3 install tailer --break-system-packages
		sudo pip3 install six --break-system-packages
		sudo pip3 install psutil --break-system-packages
		sudo pip3 install PTable --break-system-packages
		sudo pip3 install ConfigParser --break-system-packages
		sudo pip3 install pysqlite3 --break-system-packages
		sudo pip3 install flask --break-system-packages
		sudo pip3 install flask_httpauth --break-system-packages
		sudo pip3 install discord.py --break-system-packages
		sudo pip3 install prettytable --break-system-packages
              ;;
          "Python2")
		sudo sed -i '$ a\\ndeb http://archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse' /etc/apt/sources.list
		sudo sed -i '$ a\\ndeb-src http://archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse' /etc/apt/sources.list
		sudo sed -i '$ a\\ndeb http://archive.ubuntu.com/ubuntu/ focal-updates main restricted universe multiverse' /etc/apt/sources.list
		sudo sed -i '$ a\\ndeb-src http://archive.ubuntu.com/ubuntu/ focal-updates main restricted universe multiverse' /etc/apt/sources.list
		sudo sed -i '$ a\\ndeb http://archive.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse' /etc/apt/sources.list
		sudo sed -i '$ a\\ndeb-src http://archive.ubuntu.com/ubuntu/ focal-security main restricted universe multiverse' /etc/apt/sources.list
		sudo sed -i '$ a\\ndeb http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse' /etc/apt/sources.list
		sudo sed -i '$ a\\ndeb-src http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse' /etc/apt/sources.list
		sudo sed -i '$ a\\ndeb http://archive.canonical.com/ubuntu focal partner' /etc/apt/sources.list
		sudo sed -i '$ a\\ndeb-src http://archive.canonical.com/ubuntu focal partner' /etc/apt/sources.list
		sudo apt-get update
		sudo apt-get install python2-dev
                sudo apt-get install python-is-python2
		#sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
              ;;
          "MBII Server")
 	if [ -d $MBIIPATH ]; then
		clear;
       		sleep 2
	else
        	clear;
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
       		unzip -o MBII.zip -d $OPENJKPATH
		rm MBII.zip
		cd $MBIIPATH

		mv -f jampgamei386.so jampgamei386.jamp.so
		cp jampgamei386.nopp.so jampgamei386.so

		cd $SCRIPTPATH

		sudo rm -f /usr/bin/mbii 2> /dev/null
		sudo ln -s $SCRIPTPATH/mbii.py /usr/bin/mbii
		sudo chmod +x /usr/bin/mbii

		mkdir -p $HOME/.local/share/openjk/
		ln -s $HOME/mbiiez/openjk $HOME/.local/share/openjk/

		# Copies Binaries so you can run mbiided.i386 as your engine
		sudo cp $OPENJKPATH/mbiided.i386 /usr/bin/

		sudo chmod +x /usr/bin/mbiided.i386

	fi
              ;;
          "RTVRTM")
		cd $SCRIPTPATH
		
		cp rtvrtm.py $OPENJKPATH/  
		chmod +x $OPENJKPATH/rtvrtm.py
              ;;
          "Dotnet")
		wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
		sudo dpkg -i packages-microsoft-prod.deb
		rm packages-microsoft-prod.deb

                sudo apt-get update
                sudo apt-get install -y apt-transport-https dotnet-sdk-6.0
              ;;
          "MBII Updater")
                wget https://www.moviebattles.org/download/MBII_CLI_Updater.zip
                unzip -o MBII_CLI_Updater.zip -d ./updater
                rm MBII_CLI_Updater.zip
              ;;
          "Update MBII")
                cd $OPENJKPATH
                dotnet $SCRIPTPATH/updater/MBII_CommandLine_Update_XPlatform.dll

                cd $MBIIPATH
                mv -f jampgamei386.so jampgamei386.jamp.so
                cp jampgamei386.nopp.so jampgamei386.so
              ;;
          "Back to main menu")
              main;
              ;;
          *) echo "invalid option $REPLY";;
      esac
  done
}

ubuntu () {
  local PS3=$'\nPlease enter sub option: '
  local options=("Dependancies" "Python Tools" "MBII Server" "RTVRTM" "Dotnet" "MBII Updater" "Update MBII" "Back to main menu")
  local opt
  select opt in "${options[@]}"
  do
      case $opt in
          "Dependancies")
	if [ ${MACHINE_TYPE} == 'x86_64' ]; then
		sudo dpkg --add-architecture i386
                sudo apt-get update
		sudo apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 zlib1g:i386 curl:i386 lib32z1 build-essential cmake gcc-multilib g++-multilib libjpeg-dev:i386 libpng-dev:i386 zlib1g-dev:i386
	else
                sudo apt-get update
		sudo apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 zlib1g:i386 curl:i386 lib32z1 build-essential cmake gcc-multilib g++-multilib libjpeg-dev:i386 libpng-dev:i386 zlib1g-dev:i386 
	fi
              ;;
          "Python Tools")
		sudo apt-get update
		sudo apt-get install -y python-is-python3
		sudo apt-get install python3-pip -y
		sudo apt-get install -y net-tools
		sudo apt-get install -y fping
		sudo apt-get install -y python3
		sudo apt-get install -y nano
		sudo apt-get install -y python3-pip
		sudo apt-get install -y unzip
		sudo pip3 install watchgod --break-system-packages
		sudo pip3 install tailer --break-system-packages
		sudo pip3 install six --break-system-packages
		sudo pip3 install psutil --break-system-packages
		sudo pip3 install PTable --break-system-packages
		sudo pip3 install ConfigParser --break-system-packages
		sudo pip3 install pysqlite3 --break-system-packages
		sudo pip3 install flask --break-system-packages
		sudo pip3 install flask_httpauth --break-system-packages
		sudo pip3 install discord.py --break-system-packages
		sudo pip3 install prettytable --break-system-packages
              ;;
          "Python2")
		sed -i '$ a\\ndeb http://ftp.us.debian.org/debian bullseye main' /etc/apt/sources.list
		sudo apt-get update
		sudo apt-get install python2-dev
                sudo apt-get install python-is-python2
		#sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
              ;;
          "MBII Server")
 	if [ -d $MBIIPATH ]; then
		clear;
       		sleep 2
	else
        	clear;
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
       		unzip -o MBII.zip -d $OPENJKPATH
		rm MBII.zip
		cd $MBIIPATH

		mv -f jampgamei386.so jampgamei386.jamp.so
		cp jampgamei386.nopp.so jampgamei386.so

		cd $SCRIPTPATH

		sudo rm -f /usr/bin/mbii 2> /dev/null
		sudo ln -s $SCRIPTPATH/mbii.py /usr/bin/mbii
		sudo chmod +x /usr/bin/mbii

		mkdir -p $HOME/.local/share/openjk/
		ln -s $HOME/mbiiez/openjk $HOME/.local/share/openjk/

		# Copies Binaries so you can run mbiided.i386 as your engine
		sudo cp $OPENJKPATH/mbiided.i386 /usr/bin/

		sudo chmod +x /usr/bin/mbiided.i386

	fi
              ;;
          "RTVRTM")
		cd $SCRIPTPATH
		
		cp rtvrtm.py $OPENJKPATH/  
		chmod +x $OPENJKPATH/rtvrtm.py
              ;;
          "Dotnet")
		wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
		sudo dpkg -i packages-microsoft-prod.deb
		rm packages-microsoft-prod.deb

                sudo apt-get update
                sudo apt-get install -y apt-transport-https dotnet-sdk-6.0
              ;;
          "MBII Updater")
                wget https://www.moviebattles.org/download/MBII_CLI_Updater.zip
                unzip -o MBII_CLI_Updater.zip -d ./updater
                rm MBII_CLI_Updater.zip
              ;;
          "Update MBII")
                cd $OPENJKPATH
                dotnet $SCRIPTPATH/updater/MBII_CommandLine_Update_XPlatform.dll

                cd $MBIIPATH
                mv -f jampgamei386.so jampgamei386.jamp.so
                cp jampgamei386.nopp.so jampgamei386.so
              ;;
          "Back to main menu")
              main;
              ;;
          *) echo "invalid option $REPLY";;
      esac
  done
}

main () {
local PS3=$'\nEnter a number and press enter: '
local options=("Debian" "Ubuntu" "Quit")
local opt
select opt in "${options[@]}"
do
    case $opt in
        "Debian")
            debian
            ;;
        "Ubuntu")
            ubuntu
            ;;
        "Quit")
            exit
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
}


# main menu
echo "*************************************************"
echo " 	   Moviebattles II EZ Installer Tool           "
echo "        	  Interactive Menu                     "
echo "*************************************************"
echo ""
echo "		Press a number to install 	       "

PS3=$'\nEnter a number and press enter: '
options=("Debian" "Ubuntu" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Debian")
            debian
            ;;
        "Ubuntu")
            ubuntu
            ;;
        "Quit")
            exit
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
