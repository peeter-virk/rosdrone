import rospy
import math
from geometry_msgs.msg import Pose
from tf.transformations import euler_from_quaternion, quaternion_from_euler

from beginner_tutorials.msg import cord2D
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import tf

target = [0,0,0]
target_x = 0
target_y = 0
target_a = 0

c_pose = [0,0,0]
c_rot = [0,0,0]

state = 0


def kb_callback(data):
	global target
	
	print(data)
	target[0] = data.position.x
	target[1] = data.position.y
	quat = [0,0,0,0]
	quat[0] = data.orientation.x
	quat[1] = data.orientation.y
	quat[2] = data.orientation.z
	quat[3] = data.orientation.w
	rot = list(tf.transformations.euler_from_quaternion(quat))
	print(rot)
	target[2] = rot[2]
	print(target)
	
	
	pass

def odom_callback(data):
	global c_pose
	global c_rot
	
	c_pose =[
	data.pose.pose.position.x,
	data.pose.pose.position.y,
	data.pose.pose.position.z	
	]
	
	orientation_q = data.pose.pose.orientation
	orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
	c_rot = list(euler_from_quaternion (orientation_list))
		
	#print(c_pose, c_rot)
	
	pass

def get_rotation_prop(current_angle, target_angle, max_speed):
	v = min(abs(current_angle-target_angle), max_speed)
	rotate_right = True
	if current_angle > target_angle:
		if target_angle + math.pi < current_angle:
			rotate_right = False
	else:
		if target_angle - math.pi < current_angle:
			rotate_right = False
	if rotate_right:
		v=v*-1
	return v



if __name__ == "__main__":

	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	rospy.init_node('goto', anonymous=True)
	rospy.Subscriber("/turtlebot/goal_pose", Pose , kb_callback)
	rospy.Subscriber("/odom", Odometry , odom_callback)

	rate = rospy.Rate(10) # 10hz
	
	

	while not rospy.is_shutdown():
		
		heading_x = target[0] - c_pose[0]
		heading_y = target[1] - c_pose[1]
		heading_angle = math.atan2(heading_y, heading_x)
		#print(target)
		
		current_angle = c_rot[2]
		#print(current_angle)
		
		
		distance = math.sqrt((target[0]-c_pose[0])**2 + (target[1]-c_pose[1])**2)
		
		#print(distance, rotspeed)
		
		vel_msg = Twist()
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		
		vel_msg.angular.z = get_rotation_prop(current_angle, heading_angle, 2)
		
		if distance < 0.08 and state == 0:
			state = 1
		if distance > 0.02 and state == 1:
			state = 0
		
		if state == 1:
			#print("stopped")
			vel_msg.linear.x = 0
			vel_msg.angular.z = get_rotation_prop(current_angle, target[2], 0.2)
			state = 1
		elif state == 0:
			#print("moving")
			#print(distance)
			vel_msg.linear.x = min(distance/2, 0.5)
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0
		
		pub.publish(vel_msg)
		#print("distance:",distance, "\n" ,vel_msg)

		
		pass
