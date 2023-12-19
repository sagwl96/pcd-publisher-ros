#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from std_msgs.msg import Header
from open3d import io as o3dio
from open3d import geometry as o3dgeometry
import numpy as np
import os
import time
import argparse

parser = argparse.ArgumentParser(description='publishes point cloud from pcd to pcd_pointcloud')

parser.add_argument('--directory', default='/home/sagrawal/Datasets/JRDBFull/train_dataset_with_activity/pointclouds/lower_velodyne/bytes-cafe-2019-02-07_0' , type=str, help='enter the directory of the pcd files without the trailing forward slash')
parser.add_argument('--rate', default=30, type=float, help='enter the rate at which to publish the pointclouds')

args = parser.parse_args()

directory_path = args.directory
publish_rate = args.rate

def read_pcd_file(file_path):
    cloud = o3dio.read_point_cloud(file_path)
    points = np.asarray(cloud.points)
    return points

def publish_pointcloud(points, pub):
    header = Header()
    header.stamp = rospy.Time.now()
    header.frame_id = 'base_link'  # Change the frame_id as needed

    cloud_msg = point_cloud2.create_cloud_xyz32(header, points)
    pub.publish(cloud_msg)

def publish_pcd_files(directory, rate):
    rospy.init_node('pcd_publisher', anonymous=True)
    pub = rospy.Publisher('pcd_pointcloud', PointCloud2, queue_size=10)
    rate = 1/rate

    directory_list = os.listdir(directory)
    directory_list.sort()


    try:
        for filename in directory_list:
            if rospy.is_shutdown():
                break
            if filename.endswith(".pcd"):
                file_path = os.path.join(directory, filename)
                pointcloud_data = read_pcd_file(file_path)
                publish_pointcloud(pointcloud_data, pub)
                time.sleep(rate)
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    print(len(os.listdir(directory_path)))

    try:
        publish_pcd_files(directory_path, publish_rate)
    except rospy.ROSInterruptException:
        pass
