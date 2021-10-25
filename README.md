# ekos_scripts

Gathering some scripts for ekos (kstars) https://apps.kde.org/kstars/

For now the following scripts are provided:
 - scripts/warm_ccd.py =› script that can be run at the end of the scheduler or at the end of acquisition, warms up the CCD sensor slowly


# How to install and use the scripts
First, clone this repository via `git clone https://github.com/MattBlack85/ekos_scripts` in some folder, then on the scheduler (or in the CCD)
section of ekos, in the script manager click on the folder and find the dolder where you cloned `ekos_scripts`, the full path should be something
like `/home/astroberry/ekos_scripts/scripts/warm_ccd.py`
