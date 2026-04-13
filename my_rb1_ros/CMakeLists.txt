cmake_minimum_required(VERSION 3.0.2)
project(my_rb1_ros)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  geometry_msgs
  nav_msgs
  message_generation
)

## Declare your custom service files
add_service_files(
  FILES
    Rotate.srv
)

## Generate added messages and services
generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
  nav_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime rospy std_msgs geometry_msgs nav_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)