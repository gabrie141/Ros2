# 🤖 Montacargas Mecanum - Simulación ROS 2 Jazzy

Este repositorio contiene el modelo URDF, archivos de malla (STL) y configuraciones de lanzamiento para visualizar y simular un montacargas con ruedas Mecanum en ROS 2 Jazzy y Gazebo Harmonic.

## 📋 Requisitos previos
Asegúrate de tener instalado:
- Ubuntu 24.04
- ROS 2 Jazzy
- Gazebo Harmonic (ros-jazzy-ros-gz)
- Dependencias de ROS 2:
  sudo apt install ros-jazzy-joint-state-publisher-gui ros-jazzy-teleop-twist-keyboard ros-jazzy-ros-gz-bridge

## 🚀 Instalación rápida (Clonar y compilar)
Si acabas de descargar este repositorio en una computadora nueva:

1. Ir a tu workspace
   cd ~/ros2_intro/src

2. Clonar el repositorio
   git clone https://github.com/gabrie141/Ros2.git mi_montacargas

3. Compilar el paquete
   cd ~/ros2_intro
   colcon build --packages-select mi_montacargas
   source install/setup.bash

## 🖥️ Uso 1: Visualización en RViz
Para ver el modelo del robot, los ejes TF y mover la horquilla con un control gráfico:
ros2 launch mi_montacargas display.launch.py

## 🎮 Uso 2: Simulación y Control en Gazebo
Para simular el robot físico en Gazebo Harmonic (incluye un mundo personalizado sin sombras para mayor fluidez):

Terminal 1 (Simulador):
ros2 launch mi_montacargas gazebo.launch.py

Terminal 2 (Control con teclado):
source ~/ros2_intro/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard

### Controles de teclado:
- i : Avanzar hacia adelante
- , : Retroceder
- j : Girar a la izquierda
- l : Girar a la derecha
- k : Detenerse
