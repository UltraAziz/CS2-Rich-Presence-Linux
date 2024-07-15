# CS2-Rich-Presence
A simple py script for displaying details from CS2's Game State Integration into Discord Rich Presence, thanks to [pypresence](https://github.com/qwertyquerty/pypresence) and [csgo-gsi-python](https://github.com/Erlendeikeland/csgo-gsi-python) now running on linux!

The original build used the winreg library to get the steam installation path which doesn't work on linux, this build uses a manually configurated json to find the install path.

# Usage
In order for this script to work you must manually enter the install directory for CS2 in the config.json file.

Example config.json file (defaut install path on debian based systems):
```
{
"directory": "~/.steam/debian-installation/steamapps/common/Counter-Strike Global Offensive"
}
```
Then run the script and it should work fine, the message "CS:GO GSI Server starting.." stays indefenitely but everything still works, not sure if this is how it worked in the original build.

this should work fine on all operating systems but if you are using windows I'd recommend using the [original build](https://github.com/skelcium/CS2-Rich-Presence) as it spares you the hassle of specifying the install directory 
