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
            option_picked "\n${menu} Option 1...${normal}\n";

	   clear;
           show_menu;
        ;;
        2) clear;
            option_picked "\n${menu} Option 2...${normal}\n";

	   clear;
           show_menu;
        ;;
        3) clear;
            option_picked "\n${menu} Option 3...${normal}\n";

	    clear;
            show_menu;
        ;;
        4) clear;
            option_picked "\n${menu} Option 4...${normal}\n";

           clear;
           show_menu;
        ;;
        5) clear;
            option_picked "\n${menu} Option 5...${normal}\n";

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
