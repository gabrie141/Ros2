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

    urdf_file        = os.path.join(pkg_src, 'urdf', 'robot_gazebo_nativo.urdf.xacro')
    bridge_config    = os.path.join(pkg_src, 'config', 'gazebo_bridge.yaml')
    world_file       = os.path.join(pkg_src, 'worlds', 'mundo_slam.sdf')
    slam_params_file = os.path.join(pkg_src, 'config', 'slam_params.yaml')
    rviz_config_file = os.path.join(pkg_src, 'rviz', 'slam_config.rviz')

    # 1. Decirle a Gazebo donde estan las mallas STL
    gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=pkg_share_parent
    )

    # 2. Procesar URDF
    doc = xacro.process_file(urdf_file)
    robot_desc = doc.toxml()

    # 3. Lanzar Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'{world_file} -r'}.items()
    )

    # 4. Nodos del robot
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

    # 5. Transformadas estaticas para los sensores (lidar fix)
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

    # 6. Lanzar SLAM Toolbox usando su propio launch (maneja el ciclo de vida automaticamente)
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('slam_toolbox'), 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'slam_params_file': slam_params_file,
            'use_sim_time': 'true'
        }.items()
    )

    # 7. Lanzar RViz con tu configuracion
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        gz_resource_path,
        gazebo,
        rsp,
        spawn,
        bridge,
        tf_lidar_fix,
        tf_lidar_fix_alt,
        slam,
        rviz
    ])
