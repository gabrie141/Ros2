# Simulacion de Montacargas Mecanum (Gemelo Digital)

Repositorio oficial del proyecto de gemelo digital para la simulacion fisica y cinematica de un montacargas omnidireccional con ruedas Mecanum. Desarrollado para ROS 2 Jazzy y Gazebo Harmonic sobre Ubuntu 24.04.

## 1. Requerimientos e Instalacion

Para ejecutar este entorno en una maquina limpia, asegurate de tener Ubuntu 24.04 y ejecuta los siguientes comandos para instalar ROS 2 Jazzy, Gazebo, SLAM Toolbox y las herramientas necesarias:

    sudo apt update
    sudo apt install -y ros-jazzy-desktop ros-jazzy-ros-gz ros-jazzy-xacro git-lfs
    sudo apt install -y ros-jazzy-slam-toolbox ros-jazzy-teleop-twist-keyboard ros-jazzy-rviz-imu-plugin

Inicializa Git LFS para descargar correctamente los modelos 3D (.stl):

    git lfs install

## 2. Compilacion del Workspace

Si acabas de clonar el repositorio, compila el paquete y carga el entorno:

    cd ~/ros2_intro
    colcon build --symlink-install
    source install/setup.bash

## 3. Ejecucion de la Simulacion

El proyecto cuenta con dos archivos launch principales, disenados para evaluar diferentes partes del sistema.

### 3.1. Simulacion Base y Movimiento (URDF)

Para visualizar el robot, su estructura URDF, las fisicas y mover el montacargas en el mundo de Gazebo, ejecuta:

    ros2 launch mi_montacargas gazebo.launch.py

Control de Movimiento (Teleoperacion): Abre una nueva terminal y ejecuta el nodo de teleoperacion. Las ruedas Mecanum permiten movimiento holonomico. Para moverte de lado, manten presionada la tecla Shift y usa las teclas J o L.

    ros2 run teleop_twist_keyboard teleop_twist_keyboard

Control de la Paleta Elevadora (Eje Prismatico): Para subir o bajar la horquilla, envia un mensaje directo al controlador de posicion (el valor maximo es 0.158 metros):

    gz topic -t /fork_cmd -m gz.msgs.Double -p 'data: 0.12'

### 3.2. Simulacion de Sensores y Mapeo SLAM

Para iniciar el entorno completo (Gazebo, sensores, SLAM Toolbox y RViz), ejecuta:

    ros2 launch mi_montacargas slam_mapping.launch.py

## 4. Visualizacion de Sensores en RViz

Cuando se abre RViz mediante el launch de mapeo, los datos de los sensores estan disponibles, pero requieren ciertas configuraciones visuales:

1. Politica de Calidad (QoS): Los sensores de Gazebo publican a alta velocidad usando "Best Effort". Si un display en RViz se muestra vacio o con "0 points", debes desplegar las opciones del display, ir a la pestana Topic y cambiar Reliability Policy de "Reliable" a "Best Effort".
2. Transformadas (TF): Gazebo nombra los frames de los sensores de forma interna (por ejemplo, mi_montacargas/ultrasonic_right_link/sonar_right). Para que RViz pueda dibujarlos, el archivo slam_mapping.launch.py inyecta automaticamente nodos static_transform_publisher que conectan los frames del URDF con los frames internos de Gazebo.
3. IMU: Para visualizar el sensor inercial, se debe agregar el display "Imu" en RViz. Se recomienda desactivar la opcion "Enable acceleration" y activar "Enable axes" para ver los ejes XYZ rotar con el robot en tiempo real.

## 5. Proceso de Mapeo SLAM

El mapeo se realiza exclusivamente utilizando los datos del LiDAR (topico /scan). El algoritmo SLAM Toolbox procesa estos datos para construir un mapa de ocupacion en tiempo real.

Pasos para mapear:
1. Inicia el launch de mapeo.
2. En RViz, cambia el "Fixed Frame" de odom a map.
3. En el panel de Displays, activa la casilla del display Map (topico /map).
4. Abre una terminal y mueve el robot con el teclado.
5. A medida que el robot explora el mundo, veras como las paredes y obstaculos se dibujan en el mapa.

Para guardar el mapa generado al finalizar la exploracion:

    ros2 run nav2_map_server map_saver_cli -f ~/mi_mapa_generado

## 6. Modelo Fisico y Gemelo Digital

Para garantizar que la simulacion sea un reflejo fiel del hardware real, se implementaron las siguientes caracteristicas:

- Sensores preservados: El URDF incluye bloques de inercia en los links de los sensores. Sin esto, Gazebo Harmonic descarta los links sin masa y elimina los sensores asociados.
- IMU Realista: El sensor inercial lee el vector de gravedad en el eje Z y se le inyecto un modelo de ruido gaussiano basado en las hojas de datos de un chip MPU6050.
- Mundo Optimizado: El archivo del mundo tiene las sombras desactivadas y la cuadricula apagada para reducir la latencia del renderizado.

## 7. Estructura del Repositorio

- config/: Archivos YAML para el puente ROS-Gazebo y los parametros de SLAM.
- launch/: Archivos de arranque de ROS 2.
- meshes/: Modelos 3D en formato STL (gestionados con Git LFS).
- rviz/: Configuracion visual para el entorno de mapeo.
- urdf/: Modelos XACRO con inercias, colisiones y definicion de sensores.
- worlds/: Entorno de simulacion en formato SDF.
