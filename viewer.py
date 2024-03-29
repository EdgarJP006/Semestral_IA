#!/usr/bin/env python
# license removed for brevity
import rospy
import numpy as np
#check world debug
import sys
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from libardrone import ardrone
import pygame
from pygame.locals import *
import cv2
import os

drone = None
video_size = 700, 500
velocity_publisher = rospy.Publisher('/ardrone/cmd_vel', Twist, queue_size=10)

def key_action():
    vel_msg = Twist()
    keys=pygame.key.get_pressed()
    if keys[K_LEFT]:
        vel_msg.linear.x = 0
    if keys[K_UP]:
        vel_msg.linear.y = 0
    if keys[K_RIGHT]:
        vel_msg.linear.x = 0
    if keys[K_DOWN]:
        vel_msg.linear.y = 0
    #Con esta porción de codigo funcionó para llamar a las funciones del libardron
    if keys[K_RETURN]:
        drone.takeoff()
    if keys[K_SPACE]:
        drone.land()
    #Con esta porción de codigo funcionó para llamar a las funciones del libardron
    return vel_msg

def callback(ros_data):
    np_arr = np.fromstring(ros_data.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    screen = pygame.display.set_mode(video_size)
    surf = pygame.surfarray.make_surface(image_np)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    vel_msg = key_action()
    velocity_publisher.publish(vel_msg)

def main(args):
    #Con esta porción de codigo funcionó para llamar a las funciones del libardron
    global drone
    drone = ardrone.ARDrone(True)
    #Con esta porción de codigo funcionó para llamar a las funciones del libardron
    '''Initializes and cleanup ros node'''
    rospy.init_node('world_observation_client', anonymous=True)
    subscriber = rospy.Subscriber('/ardrone/front_camera/raw_image_compressed', CompressedImage, callback)
    try:
        screen = pygame.display.set_mode(video_size)
        vel_msg = key_action()
        velocity_publisher.publish(vel_msg)
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down ROS Image Viewer module")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)