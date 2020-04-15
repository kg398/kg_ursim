# kg_ursim

initial project for simulating ur5

requirements:

ubuntu 16

coppeliaSim - https://www.coppeliarobotics.com/

URsim - https://www.universal-robots.com/download/?option=66363&alttemplate=SupportSiteDownload#section16632

python 3.5 or greater + pkgs: numpy, pyserial

## configuring coppeliaSim
load kg_ursim/ur5_scene.ttt

remoteApi files are already included

## configuring ursim
copy contents of /kg_ursim/ursim to ../ursim-3.12.1.90940/programs (or your ursim intall equivalent)

## getting started
-start coppeliaSim and ursim

-run example kg_ursim/kg_ursim.py

you should now be able to run most move and get commands from kg_robot with no issues (many fns are currently untested, e.g. movel_tool, more won't work with the current framework, e.g. force_move)
