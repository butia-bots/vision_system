#!/usr/bin/env python

import rospy
import cv_bridge
import cv2
from butia_vision_msgs.msg import Recognitions
from sensor_msgs.msg import Image
import sys


def on_recognition(msg):
    for description in msg.descriptions:
        rospy.loginfo("Category/Object: {}, Score: {:.2f}%, Bounding Box (min_x, min_y, width, height): ({}, {}, {}, {})".format(
            description.label_class,
            description.probability*100,
            description.bounding_box.minX,
            description.bounding_box.minY,
            description.bounding_box.width,
            description.bounding_box.height
        ))


if __name__ == '__main__' and len(sys.argv) > 1:
    rospy.init_node("static_image_object_recognition")
    recognitions_topic = rospy.get_param("butia_vision/or/publishers/object_recognition/topic", "/butia_vision/or/object_recognition")
    recognitions_subscriber = rospy.Subscriber(recognitions_topic, Recognitions, callback=on_recognition, queue_size=1)
    image_topic = rospy.get_param("darknet_ros/subscribers/camera_reading/topic", "/camera/rgb/image_raw")
    image_publisher = rospy.Publisher(image_topic, Image, queue_size=1)
    filename = sys.argv[1]
    image = cv2.imread(filename)
    bridge = cv_bridge.CvBridge()
    rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        img_message = bridge.cv2_to_imgmsg(image, encoding="bgr8")
        image_publisher.publish(img_message)
        rate.sleep()

