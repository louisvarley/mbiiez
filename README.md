
## Movie Battles II / OpenJK Easy Docker Service Manager

Built for the **MBII New Republic Clan** 
This is a docker image and a python management script which runs as a binary. Allowing simple `mbii` commands to be issues to control server instances

## Introduction
This image is based on an older docker build by https://github.com/isair/jedi-academy-server
Some of the components including the use of the OG Engine needed an update. 

Image Changes so far is
- Ubuntu Based Image
- Using the MBII Dedicated OpenJK Server (more stable for MBII)

This package comes with a management file to make managing servers easier and quicker without the need to touch docker itself. 

The Provided python script acts as a "Mangement client" for the images. So you need no knowledge of docker to quickly spin up and manage servers. 

## Setup Requires
- You must have docker installed. `sudo apt-get install docker.io`
- Repo here is pulled `cd ~; git pull https://github.com/louisvarley/nr-mb2-docker-server.git`

## Using Install.sh
- run `chmod +x install.sh` and `./install.sh`

## Manually

- Run `ln -s /root/mbii-eds/mbii.py /usr/bin/mbii` 
- Pull the original docker image `docker pull bsencan/jedi-academy-server` 
- Run `make` within the directory to build the new image and allow the server to use this altered build in place of the above older one

## Game Files

- MBII (Linux) should be downloaded and installed at /opt/openjk/MBII **(follow offical MBII instructions)**
- OpenJK files "should" be installed at /opt/openjk/base Our image does come with the files needed but ensures we have every file we may need **(again follow official OpenJK Documention)**
- Original JA Base files also in /opt/openjk/base

## Instances
"Instances" are a single docker running a single MBII server. each instance has a instance name. This is normally one word refering to the server such as **open**

## Creating an Instance

All that is needed to create an instance is to create your own server.json file located in the `config` folder of this project. 

These config files are a cut down version of both the `server.cfg` and `rtvrtm.cfg` 
not all configs in these files are in the json file. Should you wish to add more global settings, you can edit 
`rtvrtm.template` and `server.template` 
These templates are used to build the server by importing the settings from your config.

There is an example json file called `default.json.example`
Copy this file and name it `some-name.json` replacing `some-name` with a name you wish to give your instance, such as `open` or `clan-private`

Edit the file and make any changes to the config which you want. Should you make any mistakes in the formatting. The server will not start and will warn you about JSON errors. 

Ensure the port you use is one you have not already assigned to another instance otherwise the program will have trouble monitoring and RTV/RTM will not work. 

## Actions against an instance
#### Usage

`-i [Name of your instance] ACTION`

Actions are run against an instance. 
Some examples. Where "instances" are called Open, Dueling and Cheats

`python3 ./MBII.py -i open start`

`python3 ./MBII.py -i dueling restart`

`python3 ./MBII.py -i cheats-on stop`

There a number of actions that can be used when specifying an "instance" 

#### start 
start an instance
#### stop
stop an instance
#### restart
restart an instance
#### status
show stats such as players, the map, uptime, port, ip 
#### ssh
Open a interactive SSH into the instance
#### exec
Run a shell command on the instance
#### log
Returns the entire server log from the instance 
*You can use > server.log to save this locally* 
#### say [message] 
executes svsay on the server
`python3 ./MBII.py -i dueling say "Hello Everyone"` would say "Server: Hello Everyone"
#### rcon [rcon_commands]
`python3 ./MBII.py -i legends rcon "myrconcommand argument"` would send this rcon command to the server
#### cvar key value
You can change CVAR values or just see what the value is using cvar command, for example 
`python3 ./MBII.py -i open cvar g_authenticity 1` would change the mode
`python3 ./MBII.py -i open cvar g_authenticity` would print the current the mode

### Vebose

When you run the start action if there was a problem, you may not know unless it was unable to find a given config file. You can view the output from the dedicated server directly by passing the `-v` arguement for Verbose mode. Pressing `Ctrl + c` will exit and the process will continue from then in non-verbose mode. 

### Still to do

Many things

- [x] Docks will auto restart the dedicated server if for any reason it fails. 
- [x] Use new JSON format files to setup the server
- [x] Log can be read and is extracted by an action
- [ ] Setup to handle auto server messages on the server
- [x] Make Python Management tool work as binary
- [ ] Create an install.sh file to setup all directories download OpenJK and MBII
- [ ] Make management tool auto check for MBII updates and updates server
- [ ] Wizard mode to create configs from scratch (maybe slightly gui)
- [x] Status action to show connected players, their ping and IP
- [ ] Docks to auto reboot after 24 hours and when no players? maybe better than timed
- [x] Management tool to expose RCON


