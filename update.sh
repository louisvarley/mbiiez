#!/usr/bin/env bash

# Run script to update your server to the current version (use argument "openjk" if using OpenJK engine).
# Customize variables below as necessary. 

# directory where base and MBII folder reside (AKA GameData on clients)
[ ! -d "MBII/" ] && echo "You must execute this script from the gamedata folder with the MBII subfolder." && exit 1

read -p "Update MBII?" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then

    # download newer files
    wget --execute="robots = off" -r -l 1 -nd -nH -N -A i386,pk3,so,dll,bat,sh,txt,exe https://update.moviebattles.org/files/
    cd MBII
    wget --execute="robots = off" -r -l 1 -nd -nH -N -A pk3,so,cfg,txt,mb2c,mbcr https://update.moviebattles.org/files/MBII/
    if [ "$1" == "openjk" ]
    then
        mv -f jampgamei386.so jampgamei386.jamp.so
        cp jampgamei386.nopp.so jampgamei386.so
    fi

    # start servers
    
    echo "***** Done! *****"
else
	echo "Aborting"
fi
