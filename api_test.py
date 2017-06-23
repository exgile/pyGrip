import pyGrip

HOST = "192.168.0.31"  # UR3 IP ADDRESS

# gripper initialize, activate reset.
gripper = pyGrip.gripper(HOST)

speed = 50
force = 50

#Set speed and force, ( Default speed, force = 255)
gripper.set_gripper(speed=speed, force=force)

# Basic move
gripper.close()
gripper.open()

# Custom move (Full pose value, min. : 13 , Max. : 226)
pose = 100
gripper.move(104) # move to pose

