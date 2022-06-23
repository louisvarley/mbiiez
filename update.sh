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
    printf "${menu}**${number} 1)${menu} Update MBII Server${normal}\n"
    printf "${menu}**${number} 2)${menu} Fix Symbolic Links${normal}\n"
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
            option_picked "\n${menu} Updating MBII Server...${normal}\n";
#
        #Download file lists, get the latest
#        wget -O "$SCRIPTPATH/downloads" https://archive.moviebattles.org/releases/
#
 #       while IFS= read -r line; do
#
#                SUB='UPGRADE'
 #               if [[ "$line" == *"$SUB"* ]]; then
  #                FILENAME=`echo "$line" | grep -io '<a href=['"'"'"][^"'"'"']*['"'"'"]' | sed -e 's/^<a href=["'"'"']//i' -e 's/["'"'"']$//i'`
   #               LINK="https://archive.moviebattles.org/releases/$FILENAME"
    #            fi
    #    done < downloads
#
     		wget -O "$SCRIPTPATH/UPGRADE.zip" https://update.moviebattles.org/MovieBattlesII_Upgrade_V1.9.1_V1.9.1.1.zip
 
      		printf "${menu} Extracting Moviebattles 2 Zip file...${normal}\n"
       		unzip -o UPGRADE.zip -d $OPENJKPATH
		rm UPGRADE.zip
		cd $MBIIPATH

                cd $MBIIPATH
	        mv -f jampgamei386.so jampgamei386.jamp.so
	        cp jampgamei386.nopp.so jampgamei386.so

           reset;
           show_menu;
        ;;
        2) clear;
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
