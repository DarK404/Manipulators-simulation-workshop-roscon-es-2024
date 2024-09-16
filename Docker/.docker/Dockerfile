FROM osrf/ros:humble-desktop-jammy

SHELL ["/bin/bash", "-c", "-o", "pipefail"]

ARG CUDA_MAJOR_VERSION=11
ARG CUDA_MINOR_VERSION=7
ARG USE_LOCAL=false

RUN echo "deb [trusted=yes] https://raw.githubusercontent.com/moveit/moveit2_packages/jammy-humble/ ./" \
    | sudo tee /etc/apt/sources.list.d/moveit_moveit2_packages.list
RUN echo "yaml https://raw.githubusercontent.com/moveit/moveit2_packages/jammy-humble/local.yaml humble" \
    | sudo tee /etc/ros/rosdep/sources.list.d/1-moveit_moveit2_packages.list

# Bring the container up to date to get the latest ROS2 humble sync on 01/27/23
# hadolint ignore=DL3008, DL3013
RUN apt-get update && apt-get upgrade -y && rosdep update

# Install packages required to run the demo
RUN apt-get install -y --no-install-recommends \
    ros-humble-moveit
    
# Create Colcon workspace and clone the needed source code to run the demo
RUN mkdir -p /root/isaac_moveit_tutorial_ws/src
WORKDIR /root/isaac_moveit_tutorial_ws/src

COPY /Docker/common_files /tmp/common_files


# Conditionally copy files or clone repositories
RUN if [ "$USE_LOCAL" = "true" ]; then \
    cp -r /tmp/common_files/UR_Isaac-sim /root/isaac_moveit_tutorial_ws/src/UR_Isaac-sim; \
    cp -r /tmp/common_files/zimmer_gripper /root/isaac_moveit_tutorial_ws/src/zimmer_gripper; \
    else \
        git clone https://github.com/DarK404/UR_Isaac-sim.git && \
        git clone https://github.com/Dark404/robotiq_85_gripper.git; \
    fi

# COPY UR_Isaac-sim /root/isaac_moveit_tutorial_ws/src/UR_Isaac-sim
# COPY zimmer_gripper /root/isaac_moveit_tutorial_ws/src/zimmer_gripper

#RUN git clone https://github.com/DarK404/UR_Isaac-sim .\
#    && git clone https://github.com/Dark404/robotiq_85_gripper.git \

RUN cd .. \
    && source /opt/ros/humble/setup.bash && colcon build --symlink-install

RUN git clone https://github.com/PickNikRobotics/topic_based_ros2_control.git

WORKDIR /root/isaac_moveit_tutorial_ws/src
RUN git clone https://github.com/ros-planning/moveit_resources.git -b humble

WORKDIR /root/isaac_moveit_tutorial_ws/src
RUN git clone https://github.com/DarK404/moveit2_tutorials.git
WORKDIR /root/isaac_moveit_tutorial_ws
# hadolint ignore=SC1091
RUN source /opt/ros/humble/setup.bash \
    && apt-get update -y \
    && rosdep install --from-paths src --ignore-src --rosdistro "$ROS_DISTRO" -y \
    && rm -rf /var/lib/apt/lists/*

# Use Fast DDS as middleware and load the required config for NVIDIA Isaac Sim.
ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp
RUN mkdir -p /opt/.ros
COPY Docker/.docker/fastdds.xml /opt/.ros/fastdds.xml
ENV FASTRTPS_DEFAULT_PROFILES_FILE=/opt/.ros/fastdds.xml

# Build the Colcon workspace for the user
RUN source /opt/ros/humble/setup.bash && colcon build 

# Set up the entrypoint for both container start and interactive terminals.
COPY Docker/.docker/ros_entrypoint.sh /opt/.ros/
RUN echo "source /opt/.ros/ros_entrypoint.sh" >> ~/.bashrc
ENTRYPOINT [ "/opt/.ros/ros_entrypoint.sh" ]