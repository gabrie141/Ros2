import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, AppendEnvironmentVariable
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_share = get_package_share_directory('mi_montacargas')
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot_gazebo_nativo.urdf.xacro')
    world_file = os.path.join(pkg_share, 'worlds', 'empty_no_shadows.sdf')
    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)

    set_env_vars = AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.path.join(pkg_share, '..'))
    gazebo = ExecuteProcess(cmd=['gz', 'sim', '-r', world_file], output='screen')

    # El puente traduce /cmd_vel de ROS a Gazebo
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry'
        ],
        output='screen'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'mecanum_forklift', '-z', '0.1'],
        output='screen'
    )

    return LaunchDescription([set_env_vars, gazebo, bridge, robot_state_publisher, spawn_entity])
