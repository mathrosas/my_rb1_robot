#!/usr/bin/env python

import rospy
import math
import tf
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from my_rb1_ros.srv import Rotate, RotateResponse

class RotateRobotService:
    def __init__(self):
        rospy.loginfo("RotateRobotService: Initializing...")

        # Publisher to command velocity
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # We'll subscribe to /odom to track current orientation
        rospy.Subscriber('/odom', Odometry, self.odom_callback)

        self.current_yaw = 0.0
        self.is_odom_received = False

    def odom_callback(self, msg):
        """Extract yaw from /odom's quaternion orientation."""
        orientation_q = msg.pose.pose.orientation
        # Convert quaternion to Euler angles
        quaternion = (orientation_q.x, orientation_q.y,
                      orientation_q.z, orientation_q.w)
        euler = tf.transformations.euler_from_quaternion(quaternion)
        yaw = euler[2]  # roll = euler[0], pitch = euler[1], yaw=euler[2]
        self.current_yaw = yaw
        self.is_odom_received = True

    def rotate_handler(self, req):
        """
        Service callback: rotate the robot 'req.degrees' from its current yaw.
        """
        rospy.loginfo("Received request to rotate %d degrees." % req.degrees)

        # Wait until we have at least one odom message
        while not self.is_odom_received and not rospy.is_shutdown():
            rospy.loginfo("Waiting for odom data...")
            rospy.sleep(0.5)

        # Convert degrees to radians
        radians_to_rotate = math.radians(req.degrees)

        # We rotate from the current yaw
        start_yaw = self.current_yaw
        target_yaw = self.normalize_angle(start_yaw + radians_to_rotate)

        rospy.loginfo("Starting yaw=%.2f, target yaw=%.2f" % 
                      (start_yaw, target_yaw))

        twist = Twist()
        angular_speed = 0.5  # rad/s (a moderate rotation speed)
        rate = rospy.Rate(10) # 10 Hz

        while not rospy.is_shutdown():
            current_yaw = self.current_yaw
            # Check if we've reached or passed the target angle
            angle_diff = self.normalize_angle(target_yaw - current_yaw)

            # If close enough to target, stop
            if abs(angle_diff) < 0.02:  # threshold in radians (~1 degree)
                break

            # Determine rotation direction
            # If angle_diff is positive => rotate CCW, negative => rotate CW
            twist.angular.z = angular_speed if angle_diff > 0 else -angular_speed
            self.cmd_vel_pub.publish(twist)
            rate.sleep()

        # Stop
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)

        result_str = "Rotation of %d degrees completed." % req.degrees
        rospy.loginfo(result_str)
        return RotateResponse(result=result_str)

    def normalize_angle(self, angle):
        """Normalize angle to be between -pi and +pi."""
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle

def main():
    rospy.init_node('rotate_service_server')
    rotate_service = RotateRobotService()

    # Create the service: "/rotate_robot"
    service = rospy.Service('/rotate_robot', Rotate, rotate_service.rotate_handler)
    rospy.loginfo("RotateRobotService: /rotate_robot is ready to accept requests.")

    rospy.spin()

if __name__ == '__main__':
    main()