# pyGrip
Control API : Robotiq 2-Finger Gripper (2F85) 

# Description
To control the gripper, made this program in python using Modbus command.

This program provided control gripper, detect object, action wait.

# Usage
1. connect keyboard to ur control box(or Teaching pendant)
2. press ctrl + alt + F1
3. Log in UR Control Box ( root : root, pwd : easybot)
4. write in UR Control box OS comm middleware.py, and then execute program as background
5. Check to robot ip, rewrite HOST in api_test.py.
```
python setup.py install  (in your OS to control)
```
