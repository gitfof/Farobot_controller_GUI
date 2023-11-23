import rclpy
import time
from std_msgs.msg import Float64
from my_interfaces.msg import Robot
from threading import Thread
from tkinter import Tk, Label, Scale, Button, HORIZONTAL

# Define points here
predefined_points = {
    1: (140, 90, 90 ,0),
    2: (140, 110, 20 ,0),
    3: (140, 110, 20 ,90),
    4: (140, 60, 90 ,90),
    5: (10, 60, 90 ,90),
    6: (10, 110, 90 ,90),
    7: (10, 110, 20 ,90),
    8: (10, 110, 20 ,0),
    9: (10, 90, 90, 0),
    10: (90, 80, 90, 0)
}

class JointManagerGUI:
    def __init__(self, master, node):
        self.master = master
        master.title("Joint Manager")

        
        self.joint1_label = Label(master, text="Alap (Joint 1)")
        self.joint1_scale = Scale(master, from_=0, to=180, orient=HORIZONTAL)
        self.joint1_label.pack()
        self.joint1_scale.pack()

        self.joint2_label = Label(master, text="Váll (Joint 2)")
        self.joint2_scale = Scale(master, from_=40, to=150, orient=HORIZONTAL)
        self.joint2_label.pack()
        self.joint2_scale.pack()

        self.joint3_label = Label(master, text="Könyök (Joint 3)")
        self.joint3_scale = Scale(master, from_=20, to=110, orient=HORIZONTAL)
        self.joint3_label.pack()
        self.joint3_scale.pack()

        self.joint4_label = Label(master, text="Megfogó (Joint 4)")
        self.joint4_scale = Scale(master, from_=0, to=90, orient=HORIZONTAL)
        self.joint4_label.pack()
        self.joint4_scale.pack()

        self.button1 = Button(master, text="Pick & Place", command=lambda: self.move_robot())
        self.button1.pack()

        self.button1 = Button(master, text="Go home", command=lambda: self.set_predefined_point(10))
        self.button1.pack()

        self.send_button = Button(master, text="Move robot to selected position", command=self.send_joints)
        self.send_button.pack()

        self.node = node

        # Init message
        self.msg = Robot()


    def send_joints(self):
        self.msg.joint1 = self.joint1_scale.get()
        self.msg.joint2 = self.joint2_scale.get()
        self.msg.joint3 = self.joint3_scale.get()
        self.msg.joint4 = self.joint4_scale.get()

        # Publish joint values to ROS 2 topic
        self.node.joint_publisher.publish(self.msg)

    def set_predefined_point(self, point):
        
        if point in predefined_points:
            joint1, joint2, joint3, joint4 = predefined_points[point]
            self.joint1_scale.set(joint1)
            self.joint2_scale.set(joint2)
            self.joint3_scale.set(joint3)
            self.joint4_scale.set(joint4)
            self.send_joints()

    def move_robot(self):
        for x in range(1,10):
            self.set_predefined_point(x)
            time.sleep(2)

class JointManagerNode(Thread):
    def __init__(self):
        Thread.__init__(self)

        # ROS 2 Initialization
        rclpy.init()
        self.node = rclpy.create_node('farobot_controller_node')
        self.joint_publisher = self.node.create_publisher(Robot, 'robot_controller', 10)

    def run(self):
        rclpy.spin(self.node)

def main():
    joint_manager_node = JointManagerNode()
    joint_manager_node.start()

    root = Tk()
    gui = JointManagerGUI(root, joint_manager_node)
    root.mainloop()

    joint_manager_node.node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
