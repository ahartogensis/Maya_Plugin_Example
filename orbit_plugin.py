from maya import cmds
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from shiboken6 import wrapInstance
import random
import math


global UI

'''
Menu class creates a UI that displays three buttons:
Create Center Mass
Create Satellite
Animate Orbit
These buttons create a scene of a mass in the center and an unlimited number of satellites that
will randomly orbit the center
'''
class menu(QWidget):
    def __init__(self, parent=None):
        super(menu, self).__init__(parent)
        object_name = "menu_UI_id"
        title = "Menu"
        
        # Close previous menu
        if cmds.window(object_name, title=title, exists=True):
            cmds.deleteUI(object_name)

        # Define Menu Window 
        self.setWindowFlags(Qt.Window)
        self.setObjectName(object_name)
        self.setWindowTitle(title)
        self.setGeometry(50, 50, 250, 150)

        # Build Menu
        self.build_ui()
        self.connect_ui()

        # Define initial values 
        self.has_center = False
        self.center_radius = 3

    def build_ui(self):
        #builds the UI in a vertical layout
        vertical_layout = QVBoxLayout()
        self.setLayout(vertical_layout)
        self.center_button = QPushButton(text="Create Center Mass", parent=self)
        self.satellite_button = QPushButton(text="Create Satellite", parent=self)
        self.animate_button = QPushButton(text="Animate Orbit", parent=self)
        vertical_layout.addWidget(self.center_button)
        vertical_layout.addWidget(self.satellite_button)
        vertical_layout.addWidget(self.animate_button)

    def connect_ui(self):
        #connects the buttons to functions 
        self.center_button.clicked.connect(self.create_center)
        self.satellite_button.clicked.connect(self.create_satellite)
        self.animate_button.clicked.connect(self.animate_orbit)

    def create_center(self):
        #creates a center mass for the satellites to orbit 
        print("Creating Center Mass")
        cmds.polySphere(r=self.center_radius, cuv=2, ch=1, name='Center')[0]
        self.has_center = True

    def get_location(self, x, y, z, radius):
        #recursive function that finds a distance that is greater than the radius of the center
        dist = math.sqrt((x*x) + (y*y) + (z*z))
    
        if dist > radius + 1:
            return [x, y, z]
        else:
            new_x = random.randint(-10, 10)
            new_y = random.randint(-10, 10)
            new_z = random.randint(-10, 10)
            return self.get_location(new_x, new_y, new_z, radius)  # Recursively return

    def create_satellite(self):
        #creates satellites with a random location that has a distance greater than the center radius
        #there must be a center radius before the satellites are created 
        if self.has_center:
            print("Creating Satellite")
            init_x = random.randint(-10, 10)
            init_y = random.randint(-10, 10)
            init_z = random.randint(-10, 10)

            location = self.get_location(init_x, init_y, init_z, self.center_radius)
            satellite = cmds.polySphere(r=1, name='Satellite')[0]
            cmds.move(location[0], location[1], location[2], satellite)
        else:
            print("Must Create Center")

    def animate_orbit(self):
        #animates the orbits of the satellites around the center
        print("Animating Orbit")
        sphere_list = cmds.ls("Satellite*", transforms=1)

        for s in sphere_list:
            init_x = cmds.getAttr(s + ".translateX")
            init_y = cmds.getAttr(s + ".translateY")
            init_z = cmds.getAttr(s + ".translateZ")
            
            cmds.setKeyframe(s, at="translateX", v=init_x, t=0)
            cmds.setKeyframe(s, at="translateY", v=init_y, t=0)
            cmds.setKeyframe(s, at="translateZ", v=init_z, t=0)

            #Creates keyframes for orbit
            start_frame = 1
            end_frame = 121
            radius = math.sqrt(init_x ** 2 + init_z ** 2)
            
            for t in range(start_frame, end_frame, 5): 

                #calculate the circular path 
                angle = (t - start_frame)/ 120 * 2 * math.pi
            
                x = init_x + radius * math.cos(angle)
                y = init_y + 2 * math.sin(angle)
                z = init_z + radius * math.sin(angle)

                # Set keyframes at time t
                cmds.setKeyframe(s, at="translateX", v=x, t=t)
                cmds.setKeyframe(s, at="translateY", v=y, t=t)
                cmds.setKeyframe(s, at="translateZ", v=z, t=t)

            # The final frame will be at 360 and will be set to the inital time 
            cmds.setKeyframe(s, at="translateX", v=init_x, t=360)
            cmds.setKeyframe(s, at="translateY", v=init_y, t=360)
            cmds.setKeyframe(s, at="translateZ", v=init_z, t=360)


def get_main_window():
    #opens the UI
    ptr = omui.MQtUtil.mainWindow()
    maya_window = wrapInstance(int(ptr), QWidget)
    return maya_window

def initializePlugin(plugin):
    '''Called when Maya loads the plugin.'''
    global UI
    maya_window = get_main_window()
    try:
        UI.close()
    except Exception as e:
        print(f"No previous UI to close: {e}")

    # Create and show the menu
    UI = menu(maya_window)
    UI.show()

    # Register the plugin in Maya (optional if not registering nodes)
    print("Plugin initialized successfully.")

# Plugin uninitialization function
def uninitializePlugin(plugin):
    '''Called when Maya unloads the plugin.'''
    global UI
    try:
        UI.close()  # Close the UI if it's open
        print("UI closed successfully.")
    except Exception as e:
        print(f"Failed to close UI: {e}")

    # Unregister the plugin in Maya (optional if not registering nodes)
    print("Plugin uninitialized successfully.")

