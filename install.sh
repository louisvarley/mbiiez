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

cd $SCRIPTPATH

if [ "$EUID" -ne 0 ]
  then echo "Installation requires root. Please run installation as root"
  exit
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

wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

apt-get update 
apt-get install python3-pip -y
apt-get update 

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
apt-get install -y apt-transport-https
apt-get install -y dotnet-sdk-5.0
apt-get install -y dotnet-sdk-3.1

pip3 install watchgod 
pip3 install tailer
pip3 install six
pip3 install psutil
pip3 install PTable
pip3 install ConfigParser
pip3 install sqlite3
pip3 install flask

clear

echo -e "${CYAN}"
echo -e "Downloading Movie Battles II CLI Updater..."
echo -e "${NONE}"
sleep 2

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
	unzip -o MBII.zip -d MBIIPATH
	rm "$SCRIPTPATH/MBII.zip"

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

cd ./MBII

mv -f jampgamei386.so jampgamei386.jamp.so
cp jampgamei386.nopp.so jampgamei386.so

cd $SCRIPTPATH

rm -f /usr/bin/mbii 2> /dev/null
rm -f /usr/bin/mbii-server 2> /dev/null

ln -s $SCRIPTPATH/mbii.py /usr/bin/mbii
chmod +x /usr/bin/mbii

ln -s $SCRIPTPATH/mbii-server.py /usr/bin/mbii-server
chmod +x /usr/bin/mbii-server

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
	mv -vf $OPENJKPATH/install/JediAcademy/* ../../
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
cp $SCRIPTPATH/mbiided.i386 /usr/bin
cp /opt/openjk/*.so /opt/openjk/MBII

chmod +x /usr/bin/*.i386

clear

echo -e "${CYAN}"
echo -e "Installation is complete"
echo -e "You now ${FUSCHIA}MUST${NONE} manually copy the following official Jedia Academy PK3 files to /opt/openjk/base"
echo -e "assets0.pk3"
echo -e "assets1.pk3"
echo -e "assets2.pk3"
echo -e "assets3.pk3"
echo -e "${NONE}"
echo -e "The Engine ${FUSCHIA}mbiided.i386${NONE}is available to use in your config. Custom configs must be manually installed to /usr/bin"
echo "--------------------------------------------------"
echo "Press ENTER to exit"
echo "--------------------------------------------------"
read -r _

reset
