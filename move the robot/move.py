#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist, Point, Quaternion
import tf
from math import radians, copysign, sqrt, pow, pi, atan2
from tf.transformations import euler_from_quaternion
import numpy as np
import rospy
import time

class DrawASquare():
    def __init__(self):
        # initialize
        rospy.init_node('drawasquare', anonymous=False)

        # What to do when you press ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        turtlebot3_model = rospy.get_param("model", "waffle_pi")
        position = Point()
        move_cmd = Twist()
        r = rospy.Rate(10)
        self.tf_listener = tf.TransformListener()
        self.odom_frame = 'odom'
        
        try:
            self.tf_listener.waitForTransform(self.odom_frame, 'base_footprint', rospy.Time(), rospy.Duration(1.0))
            self.base_frame = 'base_footprint'
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            try:
                self.tf_listener.waitForTransform(self.odom_frame, 'base_link', rospy.Time(), rospy.Duration(1.0))
                self.base_frame = 'base_link'
            except (tf.Exception, tf.ConnectivityException, tf.LookupException):
                rospy.loginfo("Cannot find transform between odom and base_link or base_footprint")
                rospy.signal_shutdown("tf Exception")
        
        
        def rotat(angle):
            (position, rotation) = self.get_odom()
            while abs(rotation - angle) > 0.01:
                (position, rotation) = self.get_odom()
        
        
                if (angle) >= 0:
                    if rotation <= (angle) and rotation >= (angle) - pi:
                        move_cmd.linear.x = 0.00
                        move_cmd.angular.z = 0.2
                    else:
                        move_cmd.linear.x = 0.00
                        move_cmd.angular.z = -0.2
                else:
                    if rotation <= (angle) + pi and rotation > (angle):
                        move_cmd.linear.x = 0.00
                        move_cmd.angular.z = -0.2
                    else:
                        move_cmd.linear.x = 0.00
                        move_cmd.angular.z = 0.2
                pub.publish(move_cmd)
                rospy.loginfo(abs(rotation - angle))
                r.sleep()
        def move(x,y):
            move_cmd.angular.z = 0
            last_rotation = 0
            linear_speed = 1
            angular_speed = 1
            (position, rotation) = self.get_odom()
            distance = sqrt(pow(x - position.x, 2) + pow(y - position.y, 2))
            
       
            (position, rotation) = self.get_odom()
            x_start = position.x
            y_start = position.y
            
            
            while distance > 0.05:
                (position, rotation) = self.get_odom()
                x_start = position.x
                y_start = position.y
                path_angle = atan2(y - y_start, x- x_start)

                if path_angle < -pi/4 or path_angle > pi/4:
                    if y < 0 and y_start < y:
                        path_angle = -2*pi + path_angle
                    elif y >= 0 and y_start > y:
                        path_angle = 2*pi + path_angle
                if last_rotation > pi-0.1 and rotation <= 0:
                    rotation = 2*pi + rotation
                elif last_rotation < -pi+0.1 and rotation > 0:
                    rotation = -2*pi + rotation
                move_cmd.angular.z = angular_speed * path_angle-rotation

                distance = sqrt(pow((x - x_start), 2) + pow((y - y_start), 2))
                move_cmd.linear.x = min(linear_speed * distance, 0.05)

                if move_cmd.angular.z > 0:
                    move_cmd.angular.z = min(move_cmd.angular.z, 1.5)
                else:
                    move_cmd.angular.z = max(move_cmd.angular.z, -1.5)

                last_rotation = rotation
                pub.publish(move_cmd)
                r.sleep()
                rospy.loginfo("angle")
                rospy.loginfo(rotation)
                rospy.loginfo("position")
                rospy.loginfo(distance)
                
                        
                           
                           
                              
                               
                            
                               
                           

                   
            
                
        def trai(direction,distance):
            x=0
            y=0
            d_old=0
            while len(direction)>0:
                d=direction.pop(0)
                if d=="n":
                    if d_old==0:
                        x=x+distance.pop(0)
                        move(x,y)
                        d_old=d
                    else:
                        rotat(0)
                        x=x+distance.pop(0)
                        move(x,y)
                        d_old=d
                        
                
                elif d=="e":
                    if d_old==0:
                        y=y-distance.pop(0)
                        move(x,y)
                        d_old=d
                    else:
                        rotat(-pi/2)
                        y=y-distance.pop(0)
                        move(x,y)
                        d_old=d
                        
            
                elif d=="s":
                    if d_old==0:
                        x=x-distance.pop(0)
                        move(x,y)
                        d_old=d
                    else:
                        rotat(pi)
                        x=x-distance.pop(0)
                        move(x,y)
                        d_old=d
                    
                    
                 
                        
                elif d=="w":
                    if d_old==0:
                        y=y+distance.pop(0)
                        move(x,y)
                        d_old=d
                    else:
                        rotat(pi/2)
                        y=y+distance.pop(0)
                        move(x,y)
                        d_old=d
                      
        #rotat(-pi/2)
      
        '''rotat(-pi/2)
        move(0,-0.4)
        rotat(0)
        move(0.97,-0.5)
        rotat(-pi/2)
        move(0.97,-1.35)
        rotat(0)
        move(1.48,-1.47)
        rotat(pi/2)
        move(1.48,-1)
        rotat(0)
        move(1.95,-1)
        rotat(pi/2)
        move(1.95,-0.53)
        rotat(0)
        move(2.45,-0.53)
        rotat(pi/2)
        move(2.45,0.2)'''
        
        
        
        x=['n', 'e', 'n', 'w', 's', 'w', 'n', 'e', 'n', 'w', 'n', 'e', 's', 'e', 'n', 'w', 'n', 'w', 'n', 'w'] 
        y=[0.16, 0.46, 0.76, 0.2, 0.43, 0.26, 0.64, 0.43, 0.33, 0.43, 0.15, 0.68, 0.44, 0.55, 0.33, 0.35, 0.44, 0.42, 0.49, 0.27]
        
        
        
        
        #trai(x,y)
        move(0.45,0)
        move(0.45,0.68)
        move(1.33,1.21)
        move(1.33,1.57)
        move(0.38,2.5)
        move(-0.22,2.45)
                    
                            
                        
                        
                    
                    
                        
                    
                
        
        
        
        
        
        
        
        
        
    
    def shutdown(self):
        move_cmd = Twist()
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        move_cmd.angular.z = 0
        pub.publish(move_cmd)
        
        
        rospy.loginfo("Stop Drawing Squares")
        
        rospy.sleep(1)
        
    def get_odom(self):
        try:
            (trans, rot) = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
            rotation = euler_from_quaternion(rot)

        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            rospy.loginfo("TF Exception")
            return

        return (Point(*trans), rotation[2])
 
if __name__ == '__main__':
    try:
        DrawASquare()
    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated.")