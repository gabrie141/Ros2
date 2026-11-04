import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_src = os.path.expanduser('~/ros2_intro/src/mi_montacargas')
    pkg_share_parent = os.path.expanduser('~/ros2_intro/src')
    urdf_file = os.path.join(pkg_src, 'urdf', 'robot_gazebo_nativo.urdf.xacro')
    bridge_config = os.path.join(pkg_src, 'config', 'gazebo_bridge.yaml')
    world_file = os.path.join(pkg_src, 'worlds', 'mundo_slam.sdf')

    # Decirle a Gazebo exactamente donde estan las mallas STL de mi_montacargas
    gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=pkg_share_parent
    )

    doc = xacro.process_file(urdf_file)
    robot_desc = doc.toxml()

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'{world_file} -r'}.items()
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'mi_montacargas', '-topic', 'robot_description', '-z', '0.05'],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config, 'use_sim_time': True}],
        output='screen'
    )

    # Conectar el frame interno del LiDAR de Gazebo con lidar_link de ROS 2 para que SLAM nunca descarte mensajes
    tf_lidar_fix = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'lidar_link', 'mi_montacargas/lidar_link/lidar_sensor'],
        parameters=[{'use_sim_time': True}]
    )

    tf_lidar_fix_alt = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'lidar_link', 'mi_montacargas/base_footprint/lidar_sensor'],
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        gz_resource_path,
        gazebo,
        rsp,
        spawn,
        bridge,
        tf_lidar_fix,
        tf_lidar_fix_alt
    ])
