!#bin/sh

#get script path
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
OPENJKPATH="/opt/openjk"
MBIIPATH="$OPENJKPATH/MBII"

clear

NONE='\033[0m'
CYAN='\033[36m'
FUSCHIA='\033[35m'
UNDERLINE='\033[4m'

GAME_ASSETS="aHR0cHM6Ly93d3cueC1yYWlkZXJzLm5ldC9kb3dubG9hZC9qazMvYXNzZXRzMC9maWxlL2Fzc2V0czAucGszaHR0cHM6Ly93d3cueC1yYWlkZXJzLm5ldC9kb3dubG9hZC9qazMvYXNzZXRzMS9maWxlL2Fzc2V0czEucGszaHR0cHM6Ly93d3cueC1yYWlkZXJzLm5ldC9kb3dubG9hZC9qazMvYXNzZXRzMi9maWxlL2Fzc2V0czIucGszaHR0cHM6Ly93d3cueC1yYWlkZXJzLm5ldC9kb3dubG9hZC9qazMvYXNzZXRzMy9maWxlL2Fzc2V0czMucGszCg=="

cd $SCRIPTPATH

if [ "$EUID" -ne 0 ]
  then echo "Installation requires root. Please run installation as root"
  ##exit
fi

echo -e "${CYAN}"
echo -e "Starting Installation of Easy Movie Battles II Servers"
echo -e "This installation will"
echo -e "Install all dependencies"
echo -e "Install MBII"
echo -e "Install OpenJK"
echo -e "Configure and Install the management script 'mbii'"
echo -e "${NONE}"
echo "--------------------------------------------------"
echo "Press ENTER to proceed or CTRL+C to abort"
echo "--------------------------------------------------"
read -r _

MACHINE_TYPE=`uname -m`

clear
echo -e "${CYAN}"
echo -e "Installating dependencies..."
echo -e "${NONE}"
sleep 2

apt-get install -y wget

if ! command -v dotnet &> /dev/null
then
    wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
	sudo dpkg -i packages-microsoft-prod.deb
	rm packages-microsoft-prod.deb
fi

apt-get update 
apt-get install python3-pip -y
apt-get install dotnet-sdk-6.0 -y

if [ ${MACHINE_TYPE} == 'x86_64' ]; then
	dpkg --add-architecture i386
	apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386
	apt-get install -y zlib1g:i386 
	apt-get install -y curl:i386 
fi

apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386

apt-get install -y python-setuptools python-dev 
apt-get install -y net-tools
apt-get install -y fping
apt-get install -y python3
apt-get install -y nano
apt-get install -y python3-pip
apt-get install -y unzip
apt-get install -y python3-psutil
apt-get install -y apt-transport-https
apt-get install -y python3-prettytable
apt-get install -y dotnet-sdk-5.0
apt-get install -y dotnet-sdk-3.1

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
pip3 install shutil --break-system-packages

clear

echo -e "Downloading Movie Battles II Updater..."
wget https://www.moviebattles.org/download/MBII_CLI_Updater.zip
unzip -o MBII_CLI_Updater.zip -d ./updater
rm MBII_CLI_Updater.zip

if [ -f "/opt/openjk/MBII/MBII.pk3" ]; then
	
	clear
	echo -e "${CYAN}"
	echo -e "Movie Battles II Installation found, skipping..."
	echo -e "${NONE}"
	sleep 2
	
else	
	
	clear
	echo -e "${CYAN}"
	echo -e "Downloading Movie Battles II..."
	echo -e "${NONE}"
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
	mkdir -p $MBIIPATH
	unzip -o MBII.zip -d $MBIIPATH
	rm "$SCRIPTPATH/MBII.zip"
	
	#Need a more eligant way of doing this when i can be arsed
	mv /opt/openjk/MBII/MBII/* /opt/openjk/MBII
	rmdir /opt/openjk/MBII/MBII

fi

cd $OPENJKPATH

clear
echo -e "${CYAN}"
echo -e "Validating Movie Battles II Files..."
echo -e "${NONE}"
sleep 2

dotnet $SCRIPTPATH/updater/MBII_CommandLine_Update_XPlatform.dll

unzip -o RTVRTM.zip -d $OPENJKPATH/rtvrtm
rm -rf $OPENJKPATH/rtvrtm/Windows
mv -v $OPENJKPATH/rtvrtm/Linux/rtvrtm.py $OPENJKPATH/rtvrtm.py
rm -rf $OPENJKPATH/rtvrtm

cd $MBIIPATH

mv -f jampgamei386.so jampgamei386.jamp.so
cp jampgamei386.nopp.so jampgamei386.so

cd $SCRIPTPATH

rm -f /usr/bin/mbii 2> /dev/null
ln -s $SCRIPTPATH/mbii.py /usr/bin/mbii
chmod +x /usr/bin/mbii

if [ -f "/opt/openjk/base/jampgamei386.so" ]; then

	clear
	echo -e "${CYAN}"
	echo -e "OpenJK Installation found, skipping..."
	echo -e "${NONE}"
	sleep 2

else

	clear
	echo -e "${CYAN}"
	echo -e "Downloading OpenJK"
	echo -e "${NONE}"
	sleep 2

	wget -O "$SCRIPTPATH/openjk.zip" https://builds.openjk.org/openjk-2018-02-26-e3f22070-linux.tar.gz

	tar xvzf "$SCRIPTPATH/openjk.zip" -C $OPENJKPATH
	mv -vf $OPENJKPATH/install/JediAcademy/* $OPENJKPATH
	rm "$SCRIPTPATH/openjk.zip"
	rm -rf $OPENJKPATH/install

fi
	
mkdir -p /root/.local/share/openjk/
ln -s /opt/openjk /root/.local/share/openjk/
ln -s /opt/openjk /root/.ja

# Copies Binaries so you can run openjk.i386 or mbiided.i386 as your engine
cp /opt/openjk/*.so /usr/lib/
cp /opt/openjk/MBII/*.so /usr/lib/
cp /opt/openjk/*.i386 /usr/bin/
cp $SCRIPTPATH/*.i386 /usr/bin
cp /opt/openjk/*.so /opt/openjk/MBII

chmod +x /usr/bin/*.i386

clear
echo -e "${CYAN}"
echo -e "Installing MBIIEZ Web..."
echo -e "${NONE}"

servicefile="$SCRIPTPATH/mbii-web.service"
cp $servicefile /lib/systemd/system/
sed -i 's@WORKING_DIRECTORY@'"$SCRIPTPATH"'@g' /lib/systemd/system/mbii-web.service

systemctl enable mbii-web
service mbii-web start

sleep 2
clear

clear
echo -e "${CYAN}"
echo -e "Downloading JK2 Base Assets..."
echo -e "${NONE}"

decoded_assets=$(echo "$GAME_ASSETS" | base64 -d)
    
aa=${decoded_assets:0:63}
ab=${decoded_assets:63:63}
ac=${decoded_assets:126:63}
ad=${decoded_assets:189:63}


fails=0

# Download files
# Download files only if they don't exist
if [ ! -f "/opt/openjk/base/assets0.pk3" ]; then
    wget -O "/opt/openjk/base/assets0.pk3" "$aa" || fails=1
fi

if [ ! -f "/opt/openjk/base/assets1.pk3" ]; then
    wget -O "/opt/openjk/base/assets1.pk3" "$ab" || fails=1
fi

if [ ! -f "/opt/openjk/base/assets2.pk3" ]; then
    wget -O "/opt/openjk/base/assets2.pk3" "$ac" || fails=1
fi

if [ ! -f "/opt/openjk/base/assets3.pk3" ]; then
    wget -O "/opt/openjk/base/assets3.pk3" "$ad" || fails=1
fi


# Check if any downloads failed
if [ $fails -eq 1 ]; then
	echo -e "${RED}"
    echo -e "We was unable to download 1 or more of the JK2 base files."
    echo -e "You ${FUSCHIA}MUST${NONE} manually copy the following Jedi Academy PK3 files to /opt/openjk/base"
    echo -e "assets0.pk3"
    echo -e "assets1.pk3"
    echo -e "assets2.pk3"
    echo -e "assets3.pk3"	
fi

echo -e "${CYAN}"
echo -e "${CYAN}Installation is complete${NONE}"
echo "--------------------------------------------------"
echo -e "The Engines ${FUSCHIA}mbiided.i386${NONE} and ${FUSCHIA}openjkded.i386${NONE} are available to use in your config. Custom engines must be manually installed to /usr/bin"
echo "--------------------------------------------------"
echo -e "Web Interface is available at http://0.0.0.0:8080"
echo -e "Default Login Details are"
echo -e "Username: ${FUSCHIA}Admin${NONE}"
echo -e "Password: ${FUSCHIA}Admin${NONE}"
echo "--------------------------------------------------"
echo -e "Please ensure you have port forwards setup for all ports you wish to use"
echo -e "For Instances"
echo "--------------------------------------------------"
echo -e "'mbii' can now be used as a shell command"
echo -e "You can update MBIIEZ anytime by running ${FUSCHIA}./update.sh${NONE} or ${FUSCHIA}git pull${NONE}"
echo "--------------------------------------------------"
echo -e "Please edit /mbiiez/configs/demo.json with your first instance server settings"
echo -e "You can launch this instance with the command ${FUSCHIA}mbii -i demo start${NONE}"
echo "--------------------------------------------------"
echo "Press ENTER to exit"
echo "--------------------------------------------------"
read -r _

reset
