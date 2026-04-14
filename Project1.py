import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance

#Make a tool that makes a picket fence based on user input.
#Parameters for customizing later on.


def get_maya_main_win():
    """Return maya main window"""
    main_win_addr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win_addr), QtWidgets.QWidget)

class PicketFenceWin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.picketFence = PicketFence()
        self.setWindowTitle("Picket Fence Generator")
        self.resize(500,200)
        self._mk_main_layout()
        self._connect_signals()
    
    def build_fence(self):
        self.picketFence.picket_height = self.picket_height_dspnbx.value()
        self.picketFence.picket_width = self.picket_width_dspnbx.value()
        self.picketFence.picket_number = self.picket_number_dspnbx.value()
        self.picketFence.rails = self.rail_rails_dspnbx.value()
        self.picketFence.rail_height = self.rail_height_dspnbx.value()
        self.picketFence.rail_width = self.rail_width_dspnbx.value()
        self.picketFence.picket_top = self.picket_top_chqbx
        self.picketFence.generate_fence()

    def _connect_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.build_btn.clicked.connect(self.build_fence)

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.picket_options()
        self.rail_options()
        self.top_options()
        self.mk_btns_layout()
        self.setLayout(self.main_layout)

    def picket_options(self):
        self.picket_options_layout = QtWidgets.QHBoxLayout()
        self.picket_height_lbl = QtWidgets.QLabel("Picket Height")
        self.picket_height_dspnbx = QtWidgets.QDoubleSpinBox()
        self.picket_height_dspnbx.setValue(5.5)
        self.picket_width_lbl = QtWidgets.QLabel("Picket Width")
        self.picket_width_dspnbx = QtWidgets.QDoubleSpinBox()
        self.picket_width_dspnbx.setValue(1)
        self.picket_number_lbl = QtWidgets.QLabel("Picket Number")
        self.picket_number_dspnbx = QtWidgets.QSpinBox()
        self.picket_number_dspnbx.setValue(3)
        self.picket_options_layout.addWidget(self.picket_height_lbl)
        self.picket_options_layout.addWidget(self.picket_height_dspnbx)
        self.picket_options_layout.addWidget(self.picket_width_lbl)
        self.picket_options_layout.addWidget(self.picket_width_dspnbx)
        self.picket_options_layout.addWidget(self.picket_number_lbl)
        self.picket_options_layout.addWidget(self.picket_number_dspnbx)
        self.main_layout.addLayout(self.picket_options_layout)

    def rail_options(self):
        self.rail_options_layout = QtWidgets.QHBoxLayout()
        self.rail_rails_lbl = QtWidgets.QLabel("Number of Rails")
        self.rail_rails_dspnbx = QtWidgets.QSpinBox()
        self.rail_rails_dspnbx.setValue(2)
        self.rail_height_lbl = QtWidgets.QLabel("Rail Height")
        self.rail_height_dspnbx = QtWidgets.QDoubleSpinBox()
        self.rail_height_dspnbx.setValue(0.25)
        self.rail_width_lbl = QtWidgets.QLabel("Rail Width")
        self.rail_width_dspnbx = QtWidgets.QDoubleSpinBox()
        self.rail_width_dspnbx.setValue(.5)
        self.rail_length_lbl = QtWidgets.QLabel("Rail Length")
        self.rail_length_dspnbx = QtWidgets.QDoubleSpinBox()
        self.rail_length_dspnbx.setValue(15)
        self.rail_options_layout.addWidget(self.rail_rails_lbl)
        self.rail_options_layout.addWidget(self.rail_rails_dspnbx)
        self.rail_options_layout.addWidget(self.rail_height_lbl)
        self.rail_options_layout.addWidget(self.rail_height_dspnbx)
        self.rail_options_layout.addWidget(self.rail_width_lbl)
        self.rail_options_layout.addWidget(self.rail_width_dspnbx)
        self.rail_options_layout.addWidget(self.rail_length_lbl)
        self.rail_options_layout.addWidget(self.rail_length_dspnbx)
        self.main_layout.addLayout(self.rail_options_layout)
    
    def top_options(self):
        self.top_options_layout = QtWidgets.QHBoxLayout()
        self.top_height_lbl = QtWidgets.QLabel("Top Height")
        self.top_height_dspnbx = QtWidgets.QDoubleSpinBox()
        self.top_height_dspnbx.setValue(0.5)
        self.top_width_lbl = QtWidgets.QLabel("Top Width")
        self.top_width_dspnbx = QtWidgets.QDoubleSpinBox()
        self.top_width_dspnbx.setValue(0.5)
        self.picket_top_lbl = QtWidgets.QLabel("Picket Top?")
        self.picket_top_chqbx = QtWidgets.QCheckBox()
        self.picket_top_chqbx.setTristate(True)
        self.top_options_layout.addWidget(self.top_height_lbl)
        self.top_options_layout.addWidget(self.top_height_dspnbx)
        self.top_options_layout.addWidget(self.top_width_lbl)
        self.top_options_layout.addWidget(self.top_width_dspnbx)
        self.top_options_layout.addWidget(self.picket_top_lbl)
        self.top_options_layout.addWidget(self.picket_top_chqbx)


    def mk_btns_layout(self):
        self.build_btn = QtWidgets.QPushButton("Build")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.main_layout.addWidget(self.build_btn)
        self.main_layout.addWidget(self.cancel_btn)

class PicketFence ():
    """picket_height = 10
    picket_width = 1
    picket_number = 3
    rails = 2
    rail_height = .5
    rail_width = .5
    rail_length = 15
    picket_top = True
    top_height = .5
    top_width = .5"""

    picket_offset = 2
    #create the pickets and space them out
    def make_pickets(self):
        picket_names = []
        for x in range(self.picket_number):
            picket_location = self.picket_width * (self.picket_number + 1)
            picket_name = cmds.polyCube(height=self.picket_height, width=self.picket_width, name="Picket")[0]
            picket_names.append(picket_name)
            cmds.xform(picket_name, pivots=[0, -self.picket_height/2.0, 0])
            cmds.xform(picket_name, translation=[0, self.picket_height/2.0, 0])
            self._set_pivot_to_origin(picket_name)
            #self._freeze_transforms(picket_name)
            cmds.xform(picket_name, translation=[picket_location * 2, 0, 0])
        grp_name = cmds.group(picket_names, name="Pickets")
        cmds.xform(grp_name, translation=[0, 0, 0])
        


    # Generate picket toppers, with selected shape. (cancelled out due to struggling to work functionally)
    """def make_toppers(self, picket_location, picket_top):
        if picket_top == True:
            topper_names = []
            for picket in range(self.picket_number):
                topper_name = cmds.polyPyramid(height=self.top_height, width=self.top_width, name="Topper"[0])
                topper_names.append(topper_name)
                cmds.xform(topper_name, pivots =[0, -top_height/2.0, 0])
                cmds.xform(topper_name, translation=[picket_location, picket_height, 0])
            grp_name = cmds.group(topper_names, name="Toppers")
            cmds.xform(grp_name, translation=[0, 0, 0])"""


    #create the rails and space them out, and run the length of the entire picket range even gaps.
    def make_rails(self, picket_height):
        rail_names = []
        for x in range(self.rails):
            rail_name = cmds.polyCube(height=self.rail_height, width=self.rail_width, length=self.rail_length, name="Rail")[0]
            rail_names.append(rail_name)
            cmds.xform(rail_name, pivots=[0, -self.rail_height/2.0, 0])
            cmds.xform(rail_name, translation=[0, (self.rail_height + 1), 0])
        grp_name = cmds.group(rail_names, name="Rails")   
        cmds.xform(grp_name, translation=[0, (picket_height/2), 0]) 


    #Command it to make the fence
    def generate_fence(self):
        self.make_pickets()
        self.make_toppers()
        self.make_rails()