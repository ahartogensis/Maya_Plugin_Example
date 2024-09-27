READ ME


This folder contains the README.txt and orbit_plugin.py.
The orbit plugin creates a UI with three buttons: "Create Center Mass," "Create Satellite," and "Animate Orbit." Using the plugin, you can create a center sphere and randomly positioned satellites, which are then animated to orbit around the center. After you click “Animate Orbit”, play the timeline to see the animation. 

Assistance on the structure of the plugin from:
mvanneutigem
kim-maglalang
chatgpt for checking code syntax and changing it to the most updated version of python 

Command to install the plug-in:
import maya.cmds as cmds
cmds.loadPlugin(“/PATH-TO-FILE/orbit_plugin.py")

Then to unload the plug-in:
cmds.unloadPlugin(‘orbit_plugin.py')