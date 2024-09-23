# Manipulators-simulation-workshop-roscon-es-2024
This tutorial demonstrates simulating UR manipulators with Nvidia Isaac Sim and ROS 2, including single and multi-robot setups and camera vision integration, using planners like LULA, RMPFlow, and Curobo.
## System Requirements

To run the Docker-based simulation tutorial, ensure your system meets the following requirements:

- **Operating System**: Ubuntu 20.04 LTS or later (preferred); Docker is also available for Windows and macOS.
- **Docker**: Docker Engine and Docker Compose installed (version 1.27+ recommended).
- **CPU**: Multi-core processor (e.g., Intel Core i7 or equivalent).
- **GPU**: NVIDIA GPU with CUDA support (e.g., RTX 2060 or higher) and driver version **525.60.11** or later.
- **RAM**: Minimum 8 GB (16 GB recommended).
- **Storage**: At least 50 GB of free disk space for Docker images and data.
- **Network**: Stable internet connection for downloading Docker images and dependencies.

**Important**: Ensure Docker is properly configured to utilize the GPU if required and that your system has adequate resources for smooth operation. Verify GPU availability with the following command:

```bash
docker run --rm --gpus all nvidia/cuda:11.2.2-base-ubuntu20.04 nvidia-smi
```

## Setup using Docker (RECOMENDED)
1. **Setup NVIDIA GPU Cloud (NGC) Environment:**

   Ensure you have an NGC API key. Follow the instructions [here](https://docs.nvidia.com/ngc/gpu-cloud/ngc-user-guide/index.html#generating-api-key) to generate one.

   Log in to NGC using Docker:

   ```bash
   docker login nvcr.io
   Username: $oauthtoken
   Password: [Your NGC API Key]
2. **Install and configure your omniverse Nucleus user:**
   
   Ensure that you have [Omniverse Launcher](https://www.nvidia.com/es-es/omniverse/download/) installed
   
   After installing Omniverse Launcher, configure your local [Nucleus Server](https://docs.omniverse.nvidia.com/nucleus/latest/workstation/installation.html)

3. **Clone the Workshop Repository:**
```bash
git clone https://github.com/DarK404/Manipulators-simulation-workshop-roscon-es-2024.git
cd Manipulators-simulation-workshop-roscon-es-2024/Docker
```
4. **Build the Docker Image:**

Run the provided script to set up the environment and build the Docker images:
```bash
bash build_docker.sh isaac_sim_2023.1.0
```
Then, build the required services:
```bash
docker compose build demo_isaac demo_isaac_zimmer
```
5. **Run the Docker Containers:**

Enable GUI visualization on your host machine:
```bash
xhost + # this will enable gui visualization
```
Start the Isaac Sim container:

```bash
bash start_docker.sh isaac_sim_2023.1.0
cd examples/code/
```
## Running the Demos

To Run Isaac_moveit.py, execute the following command inside the Docker terminal
```bash
# Isaac Sim Docker Terminal
$omni_python isaac_moveit.py
```
In your computer, open a second terminal and execute 
```bash
cd Manipulators-simulation-workshop-roscon-es-2024/Docker
docker compose up demo_isaac
```
To Run the simple_stacking_ur.py, execute the following command inside the Docker terminal
```bash
# Isaac Sim Docker Terminal
$omni_python simple_stacking_ur.py
```
In your computer, open a second terminal and execute 
```bash
cd Manipulators-simulation-workshop-roscon-es-2024/Docker
docker compose up demo_isaac_zimmer
```



