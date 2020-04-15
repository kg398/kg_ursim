# kg_ursim

initial project for simulating ur5

example: https://drive.google.com/open?id=1hSW8s-fuYBwcZ_t0auBvHnfCvmeZanHb

requirements:

ubuntu 16

coppeliaSim - https://www.coppeliarobotics.com/

URsim - https://www.universal-robots.com/download/?option=66363&alttemplate=SupportSiteDownload#section16632

python 3.5 or greater + pkgs: numpy, pyserial

## configuring coppeliaSim
load kg_ursim/ur5_scene.ttt

remoteApi files are already included, interface is handled by kg_robot_sim.py, for more detail see: https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm

## configuring ursim
copy contents of /kg_ursim/ursim to ../ursim-3.12.1.90940/programs (or your ursim intall equivalent)

interface is based off generic_ur5_controller, more detail here: https://github.com/kg398/Generic_ur5_controller 

## getting started
-start coppeliaSim and ursim

-run example kg_ursim/kg_ursim.py

you should now be able to run most move and get commands from kg_robot with no issues (many fns are currently untested, e.g. movel_tool, more won't work with the current framework, e.g. force_move)
