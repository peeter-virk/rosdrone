import rospy
from beginner_tutorials.msg import cord2D
def talker():
    pub = rospy.Publisher('kbcords', cord2D, queue_size=10)
    rospy.init_node('kb_input', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        msg = cord2D()
        x = input("X:")
        if x == "q":
        	break
        y = input("Y:")
        if x == "q":
        	break
        print (f"sending robot to {x}, {y}.")
        
        try:
            msg.x = int(x)
            msg.y = int(y)
            pub.publish(msg)
        except Exception as e:
            print(e)
        rate.sleep()
talker()
