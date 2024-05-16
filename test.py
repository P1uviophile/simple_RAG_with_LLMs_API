#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 该例程将发布turtle1/cmd_vel话题，消息类型geometry_msgs::Twist
import rospy
from turtlesim.msg import Pose
from threading import Thread


def poseCallback(msg):
    rospy.loginfo("Turtle pose: x:%0.3f, y:%0.3f", msg.x, msg.y)


def turtle_pose_test():
    ros = rospy.init_node('turtle_test', anonymous=True)  # ROS节点初始化

    return ros


def turtle_pub_test(rospy):
    # 创建一个小海龟速度发布者，发布名为/turtle1/cmd_vel的topic，消息类型为geometry_msgs::Twist，8代表消息队列长度
    turtle_pose_pub = rospy.Publisher('/turtle1/Pose', Pose, queue_size=8)
    rate = ros.Rate(1)  # 设置循环的频率
    flag = 1
    turtle_pose_msg = Pose()

    while not rospy.is_shutdown():
        turtle_pose_pub.x
        flag *= -1
        turtle_pose_msg.x = 114 * flag
        turtle_pose_msg.y = 514 * flag
        # 发布消息
        turtle_pose_pub.publish(turtle_pose_msg)
        rospy.loginfo("pub x is :%0.2f m/s, pub y is :%0.2f m/s",
                      turtle_pose_msg.x, turtle_pose_msg.y)
        rate.sleep()  # 按照循环频率延时


def turtle_sub_test(rospy):
    # 创建一个Subscriber，订阅名为/pose的topic，注册回调函数poseCallback
    rospy.Subscriber("/turtle1/Pose", Pose, poseCallback)
    rospy.spin()  # 循环等待回调函数


if __name__ == '__main__':
    try:
        ros = turtle_pose_test()
    except rospy.ROSInterruptException:
        pass

    # 创建 Thread 实例
    t1 = Thread(target=turtle_pub_test, args=(ros,))
    t2 = Thread(target=turtle_sub_test, args=(ros,))

    # 启动线程运行
    t1.start()
    t2.start()