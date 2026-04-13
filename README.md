# Introduction to Gazebo

This project provides an introduction to using Gazebo with ROS (Robot Operating System). It includes a custom robot model and configurations for visualization and simulation in Gazebo.

## Project Structure

```
Introduction-to-Gazebo-main/
├── my_rb1_description/
│   ├── CMakeLists.txt
│   ├── package.xml
│   ├── launch/
│   │   ├── display.launch
│   ├── urdf/
│       ├── my_rb1_robot.urdf
│
├── my_rb1_gazebo/
│   ├── CMakeLists.txt
│   ├── package.xml
│   ├── launch/
│       ├── my_rb1_robot_warehouse.launch
```

## Installation

Ensure you have ROS and Gazebo installed before proceeding.

```sh
sudo apt update && sudo apt install ros-noetic-gazebo-ros
```

Clone this repository into your ROS workspace:

```sh
cd ~/catkin_ws/src
git clone https://github.com/mathrosas/Introduction-to-Gazebo.git
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

## Usage

### 1. View the Robot Model in RViz

```sh
roslaunch my_rb1_description display.launch
```

### 2. Launch the Robot in Gazebo

```sh
roslaunch my_rb1_gazebo my_rb1_robot_warehouse.launch
```

This will spawn the robot in a Gazebo environment, allowing you to test its simulation behavior.

## Dependencies

- ROS (Noetic recommended)
- Gazebo

## Contributing

Feel free to fork this repository and contribute improvements!
