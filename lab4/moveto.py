import rospy
import math
from tf.transformations import euler_from_quaternion, quaternion_from_euler

from beginner_tutorials.msg import cord2D
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


target_x = 0
target_y = 0
state = 0

c_pose = [0,0,0]
c_rot = [0,0,0]


def kb_callback(data):
	global target_x
	global target_y
	global target_swiched
	
	target_x = data.x
	target_y = data.y
	state = 1
	
	
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




if __name__ == "__main__":

	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	rospy.init_node('goto', anonymous=True)
	rospy.Subscriber("/kbcords", cord2D , kb_callback)
	rospy.Subscriber("/odom", Odometry , odom_callback)

	rate = rospy.Rate(5) # 5hz
	
	

	while not rospy.is_shutdown():
		
		heading_x = target_x - c_pose[0]
		heading_y = target_y - c_pose[1]
		heading_angle = math.atan2(heading_y, heading_x)
		#print(target_x, target_y,heading_angle)
		
		current_angle = c_rot[2]
		#print(current_angle)
		
		rotate_right = True
		
		if current_angle > heading_angle:
			if heading_angle + math.pi < current_angle:
				rotate_right = False
		else:
			if heading_angle - math.pi < current_angle:
				rotate_right = False
		
		#print(rotate_right)
		
		rotspeed = min(abs(heading_angle - current_angle), abs(heading_angle + 2 * math.pi - current_angle))
		
		distance = math.sqrt((target_x-c_pose[0])**2 + (target_y-c_pose[1])**2)
		
		#print(distance, rotspeed)
		
		vel_msg = Twist()
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		if rotate_right:
			vel_msg.angular.z = -1 * rotspeed
		else:
			vel_msg.angular.z = 1 * rotspeed
		if distance < 0.001:
			#print("stopped")
			vel_msg.linear.x = 0
			vel_msg.angular.z = 0
		else:
			#print("moving")
			vel_msg.linear.x = min(distance/2, 0.1/(rotspeed))
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0
		
		pub.publish(vel_msg)
		print("distance:",distance, "\n" ,vel_msg)

		
		pass
