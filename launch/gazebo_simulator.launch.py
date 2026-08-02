import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    simulator_dir = get_package_share_directory('orne_simulator')
    # world内の package://orne_simulator/... URIを解決するためのリソースパス（installのshareディレクトリ）
    resource_path = os.path.dirname(simulator_dir)

    declare_world_arg = DeclareLaunchArgument(
        'world',
        default_value='tsudanuma2-3_colors.sdf',
        description='worlds/ディレクトリ内のワールドファイル名'
    )
    declare_verbosity_arg = DeclareLaunchArgument(
        'verbosity',
        default_value='1',
        description='Gazeboのログレベル'
    )
    declare_use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='シミュレーション時刻(/clock)を使用するかどうか'
    )

    world = LaunchConfiguration('world')
    verbosity = LaunchConfiguration('verbosity')
    use_sim_time = LaunchConfiguration('use_sim_time')

    use_sim_time_param = ParameterValue(use_sim_time, value_type=bool)

    set_ign_resource_path = AppendEnvironmentVariable(
        'IGN_GAZEBO_RESOURCE_PATH', resource_path
    )
    set_gz_resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH', resource_path
    )

    world_path = PathJoinSubstitution([
        FindPackageShare('orne_simulator'), 'worlds', world
    ])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments=[
            ('gz_args', ['-r -v ', verbosity, ' ', world_path]),
        ]
    )

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        parameters=[{
            'config_file': PathJoinSubstitution([
                FindPackageShare('orne_simulator'), 'config', 'gz_bridge.yaml'
            ]),
            'use_sim_time': use_sim_time_param,
        }],
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        output='screen',
        parameters=[
            PathJoinSubstitution([FindPackageShare('orne_simulator'), 'config', 'params.yaml']),
            {'use_sim_time': use_sim_time_param},
        ],
    )

    teleop_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        output='screen',
        parameters=[
            PathJoinSubstitution([FindPackageShare('orne_simulator'), 'config', 'params.yaml']),
            {'use_sim_time': use_sim_time_param},
        ],
    )

    return LaunchDescription([
        declare_world_arg,
        declare_verbosity_arg,
        declare_use_sim_time_arg,
        set_ign_resource_path,
        set_gz_resource_path,
        gazebo,
        bridge_node,
        joy_node,
        teleop_node,
    ])
