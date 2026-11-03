# 🤖 Simulación de Montacargas Mecanum (Gemelo Digital ABET)

Repositorio oficial del proyecto de gemelo digital para la simulación física y cinemática de un montacargas omnidireccional con ruedas Mecanum[cite: 7]. Desarrollado para **ROS 2 Jazzy** y **Gazebo Harmonic** sobre **Ubuntu 24.04**.

---

## 📋 1. Requerimientos del Sistema

Para ejecutar este entorno de simulación correctamente, tu equipo debe contar con lo siguiente:
* **Sistema Operativo:** Ubuntu 24.04 LTS (Noble Numbat)
* **Framework:** ROS 2 Jazzy Jalisco
* **Simulador:** Gazebo Harmonic (`gz-sim 8`) con motor de físicas DART
* **Herramientas y Dependencias de ROS 2:**
  * `colcon` (Build tool de ROS 2)
  * `ros-jazzy-ros-gz` (Puente de integración ROS 2 - Gazebo)
  * `xacro` (Procesador de macros URDF)
  * `teleop_twist_keyboard` (Para control manual por teclado)

---

## ⚙️ 2. Guía de Clonación e Instalación en una Nueva Computadora

Si estás configurando este repositorio en una máquina limpia, abre tu terminal y sigue estos pasos:

### 2.1. Instalar dependencias base de ROS 2 Jazzy y Gazebo
Asegúrate de tener instalado el escritorio de ROS 2 Jazzy junto con los paquetes de simulación y herramientas[cite: 6]:
```bash
sudo apt update && sudo apt install -y ros-jazzy-desktop ros-jazzy-ros-gz ros-jazzy-xacro git-lfs
2.2. Clonar el repositorio y configurar Git LFS
Dado que los modelos 3D (.stl) de las mallas están gestionados mediante Git LFS debido a su peso, inicializa LFS en tu equipo antes de clonar:

Bash
git lfs install
Crea tu espacio de trabajo (workspace) de ROS 2 y clona el proyecto:

Bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone [https://github.com/gabrie141/Ros2.git](https://github.com/gabrie141/Ros2.git) .
git lfs pull
2.3. Compilar el Workspace
Bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
(Opcional) Para evitar tener que escribir source install/setup.bash en cada terminal nueva, puedes agregarlo a tu archivo de configuración global:

Bash
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
🚀 3. Modo de Operación y Ejecución
3.1. Iniciar la Simulación (Gazebo + RViz)
Para levantar el gemelo digital completo con el mundo virtual en Gazebo Harmonic, la visualización de los marcos en RViz y la carga del URDF parametrizado, ejecuta:

Bash
ros2 launch mi_montacargas gazebo.launch.py
3.2. Control de Movimiento (Omnidireccional / Holonómico)
El robot utiliza tracción Mecanum real, lo que le permite desplazarse hacia adelante, atrás, girar e incluso realizar traslaciones laterales (strafe) y en diagonal.

Control con Teclado (Modo Holonómico con Shift):
Abre una nueva terminal y lanza el nodo de teleoperación:

Bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
Nota de operación: Para activar el movimiento lateral (strafe), debes mantener presionada la tecla Shift de tu teclado junto con las teclas asignadas (Shift + J para la izquierda, Shift + L para la derecha).

Pruebas directas mediante comandos de Tópicos (/cmd_vel):

Desplazamiento lateral puro a la izquierda (+Y):

Bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.25, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" -r 10
Movimiento en diagonal a 45°:

Bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.20, y: 0.20, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" -r 10
Control de la Paleta Elevadora (Eje Prismático):
Puedes gobernar la altura del sistema de elevación enviando un comando directo al tópico del controlador de posición:

Bash
gz topic -t /fork_cmd -m gz.msgs.Double -p 'data: 0.12'
📂 4. Estructura del Repositorio
mi_montacargas/meshes/: Almacena los modelos CAD en formato .stl (chasis, horquilla y ruedas Mecanum).

mi_montacargas/urdf/: Modelos XACRO con la estructuración de eslabones, colisiones simplificadas y matrices de inercia calculadas.

mi_montacargas/launch/: Archivos de automatización de arranque (gazebo.launch.py).

mi_montacargas/config/: Archivos YAML de configuración de controladores y puentes ROS-Gazebo.