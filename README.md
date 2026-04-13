# Checkpoint 1 - Introduction to Gazebo

Mobile robot simulation built from scratch using **URDF** and **Gazebo Classic** on **ROS Noetic**. This project creates a simplified replica of the [Robotnik RB-1](https://robotnik.eu/products/mobile-robots/rb-1-base/) mobile robot, defines its physical properties, spawns it into a warehouse environment, and adds sensor/actuator plugins to make it controllable.

Part of the [ROS & ROS 2 Developer Master Class](https://www.theconstructsim.com/) certification (Phase 1).

## Robot Description

The RB-1 replica is a differential-drive cylindrical robot with the following specs:

| Component | Geometry | Dimensions | Mass |
|---|---|---|---|
| Base body | Cylinder | 50 cm diameter, 30 cm height | 22 kg |
| Drive wheels (x2) | Cylinder | 5 cm diameter, 3 cm width | 1 kg each |
| Caster wheels (x2) | Sphere | 2.5 cm radius | 0.5 kg each |
| Laser scanner | Box | 2.5 cm cube | ~0 kg |
| **Total** | | | **25 kg** |

### Link Tree

```
base_footprint (fixed)
  └── base_link
        ├── left_wheel       (continuous) @ (0.0, 0.2, -0.15)
        ├── right_wheel      (continuous) @ (0.0, -0.2, -0.15)
        ├── front_caster     (fixed)      @ (0.2, 0.0, -0.15)
        ├── back_caster      (fixed)      @ (-0.2, 0.0, -0.15)
        └── front_laser      (fixed)      @ (0.25, 0.0, 0.075) rotated 180 on X
```

Caster wheels have zero friction (`mu1=0`, `mu2=0`) to allow free sliding. Drive wheels have friction of 1.0. All links include visual, collision, and inertial properties with computed moments of inertia.

## Tasks Breakdown

The project was developed incrementally across three tasks, each marked with a Git tag.

### Task 1 - Build the URDF (`git checkout task1`)

- Created the `my_rb1_description` package with the full URDF model
- Defined all links and joints with proper dimensions, mass distribution, and inertia tensors
- Created `display.launch` to visualize the robot in **RViz** using `joint_state_publisher_gui` and `robot_state_publisher`
- Drive wheel joints are controllable via the GUI slider

### Task 2 - Spawn in Gazebo (`git checkout task2`)

- Created the `my_rb1_gazebo` package with `my_rb1_robot_warehouse.launch`
- Spawned the robot inside a warehouse world (from `rb1_base_gazebo`) using `gazebo_ros/spawn_model`
- Positioned the robot at the center of the yellow-taped starting area (`x=-0.383, y=-1.386, z=0.175`)
- Applied Gazebo material colors: black body, red wheels, grey casters, orange laser

### Task 3 - Sensor and Actuator Plugins (`git checkout task3`)

Added two Gazebo plugins to the URDF:

**Differential Drive** (`libgazebo_ros_diff_drive.so`)
- Subscribes to `/cmd_vel` (geometry_msgs/Twist)
- Publishes odometry on `/odom`
- Wheel separation: 0.4 m, wheel diameter: 0.05 m

**Laser Scanner** (`libgazebo_ros_laser.so`)
- Hokuyo-style lidar attached to `front_laser`
- Publishes on `/scan` (sensor_msgs/LaserScan)
- 720 samples, FOV: 180 degrees, range: 0.2 - 10.0 m

## Project Structure

```
my_rb1_robot/
├── my_rb1_description/
│   ├── CMakeLists.txt
│   ├── package.xml
│   ├── launch/
│   │   └── display.launch            # RViz visualization
│   └── urdf/
│       └── my_rb1_robot.urdf         # Full robot model + plugins
│
└── my_rb1_gazebo/
    ├── CMakeLists.txt
    ├── package.xml
    └── launch/
        └── my_rb1_robot_warehouse.launch  # Gazebo warehouse simulation
```

## How to Use

### Prerequisites

- ROS Noetic
- Gazebo 11
- Packages: `joint_state_publisher_gui`, `robot_state_publisher`, `gazebo_ros`

### Build

```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

### Visualize in RViz

```bash
roslaunch my_rb1_description display.launch
```

Use the `joint_state_publisher_gui` sliders to rotate the drive wheels. In RViz, add a `RobotModel` display and set the Alpha to see the link frames.

### Launch Gazebo Simulation

```bash
# Make sure simulation_ws is in the package path
export ROS_PACKAGE_PATH='/home/user/catkin_ws/src:/opt/ros/noetic/share:/home/user/simulation_ws/src'

roslaunch my_rb1_gazebo my_rb1_robot_warehouse.launch
```

### Move the Robot

```bash
# Drive forward
rostopic pub /cmd_vel geometry_msgs/Twist "linear: {x: 0.2}" -r 10

# Rotate in place
rostopic pub /cmd_vel geometry_msgs/Twist "angular: {z: 0.5}" -r 10
```

### Read Laser Data

```bash
rostopic echo /scan
```

## Key Concepts Covered

- **URDF modeling**: links, joints, visual/collision/inertial properties
- **Inertia computation**: cylinder and sphere moment of inertia formulas
- **Gazebo integration**: materials, friction coefficients, spawn positioning
- **Gazebo plugins**: differential drive controller, laser scanner sensor
- **ROS launch files**: parameter loading, node orchestration, package includes
- **RViz visualization**: robot model display, TF frames, joint state publishing

## Technologies

- ROS Noetic (Python 2 compatibility layer)
- Gazebo Classic 11
- URDF (Unified Robot Description Format)
- RViz
