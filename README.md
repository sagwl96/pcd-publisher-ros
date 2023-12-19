# pcd-publisher-ros
A python script to publish all the pcd files as pointcloud to a ros topic

- Use this when you have ros installed in your system.
- Additionally, you require open3d "pip install open3d" to run this file successfully

###Usage

The program takes two arguments
--directory -> paste the directory path to where your pcd files are stored
--rate -> the rate at which to publish the pointclouds

#Example:
python pcd_pub.py --directory /home/admin/PCDData --rate 30
