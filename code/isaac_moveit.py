# -*- coding: utf-8 -*-
# Copyright (c) 2020-2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import sys

import carb
import numpy as np
from omni.isaac.kit import SimulationApp
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
default_path = os.path.abspath(os.path.join(current_dir, '../../src/curobo/content/assets'))

UR_STAGE_PATH = "/ur3e/ur3e"
UR_STAGE_PATH1 = "/ur3e"
UR_USD_PATH = "/usd_files/ur3e.usd"

BACKGROUND_STAGE_PATH = "/background"
BACKGROUND_USD_PATH = "/usd_files/testbed_table.usd"
CONFIG = {"renderer": "RayTracedLighting", "headless": False}

# Example ROS2 bridge sample demonstrating the manual loading of stages
# and creation of ROS components
simulation_app = SimulationApp(CONFIG)
import omni.graph.core as og  # noqa E402
from omni.isaac.core import SimulationContext  # noqa E402
from omni.isaac.core.utils import (  # noqa E402
    extensions,
    prims,
    stage,
    viewports,
)
from omni.isaac.core_nodes.scripts.utils import set_target_prims  # noqa E402
from pxr import Gf  # noqa E402

# enable ROS2 bridge extension
extensions.enable_extension("omni.isaac.ros2_bridge")

simulation_context = SimulationContext(stage_units_in_meters=1.0)

# default_path=".."
# Locate Isaac Sim assets folder to load environment and robot stages
# assets_root_path = "omniverse://localhost/"
# if assets_root_path is None:
#     carb.log_error("Could not find Isaac Sim assets folder")
#     simulation_app.close()
#     sys.exit()

# Preparing stage
viewports.set_camera_view(eye=np.array([1.20193, 1.33053, 1.46214]), target=np.array([0, 0.000001, 1]))

# Loading the simple_room environment
stage.add_reference_to_stage(
    default_path + BACKGROUND_USD_PATH, BACKGROUND_STAGE_PATH
)

# Loading the UR robot USD
prims.create_prim(
    UR_STAGE_PATH1,
    "Xform",
    position=np.array([0.06, 0.06, 0.82]),
    orientation=([1.0, 0.0, 0.0, 0.0]),
    usd_path=default_path + UR_USD_PATH,
)

simulation_app.update()

# Creating a action graph with ROS component nodes
try:
    og.Controller.edit(
        {"graph_path": "/ActionGraph", "evaluator_name": "execution"},
        {
            og.Controller.Keys.CREATE_NODES: [
                ("OnImpulseEvent", "omni.graph.action.OnImpulseEvent"),
                ("ReadSimTime", "omni.isaac.core_nodes.IsaacReadSimulationTime"),
                ("Context", "omni.isaac.ros2_bridge.ROS2Context"),
                ("PublishJointState", "omni.isaac.ros2_bridge.ROS2PublishJointState"),
                (
                    "SubscribeJointState",
                    "omni.isaac.ros2_bridge.ROS2SubscribeJointState",
                ),
                (
                    "ArticulationController",
                    "omni.isaac.core_nodes.IsaacArticulationController",
                ),
                ("PublishClock", "omni.isaac.ros2_bridge.ROS2PublishClock"),
            ],
            og.Controller.Keys.CONNECT: [
                ("OnImpulseEvent.outputs:execOut", "PublishJointState.inputs:execIn"),
                ("OnImpulseEvent.outputs:execOut", "SubscribeJointState.inputs:execIn"),
                ("OnImpulseEvent.outputs:execOut", "PublishClock.inputs:execIn"),
                (
                    "OnImpulseEvent.outputs:execOut",
                    "ArticulationController.inputs:execIn",
                ),
                ("Context.outputs:context", "PublishJointState.inputs:context"),
                ("Context.outputs:context", "SubscribeJointState.inputs:context"),
                ("Context.outputs:context", "PublishClock.inputs:context"),
                (
                    "ReadSimTime.outputs:simulationTime",
                    "PublishJointState.inputs:timeStamp",
                ),
                ("ReadSimTime.outputs:simulationTime", "PublishClock.inputs:timeStamp"),
                (
                    "SubscribeJointState.outputs:jointNames",
                    "ArticulationController.inputs:jointNames",
                ),
                (
                    "SubscribeJointState.outputs:positionCommand",
                    "ArticulationController.inputs:positionCommand",
                ),
                (
                    "SubscribeJointState.outputs:velocityCommand",
                    "ArticulationController.inputs:velocityCommand",
                ),
                (
                    "SubscribeJointState.outputs:effortCommand",
                    "ArticulationController.inputs:effortCommand",
                ),
            ],
            og.Controller.Keys.SET_VALUES: [
                ("Context.inputs:useDomainIDEnvVar", 1),
                # Setting the /UR target prim to Articulation Controller node
                ("ArticulationController.inputs:usePath", True),
                ("ArticulationController.inputs:robotPath", UR_STAGE_PATH),
                ("PublishJointState.inputs:topicName", "isaac_joint_states"),
                ("SubscribeJointState.inputs:topicName", "isaac_joint_commands"),
            ],
        },
    )

except Exception as e:
    print(e)

# Setting the /UR target prim to Publish JointState node
set_target_prims(
    primPath="/ActionGraph/PublishJointState", targetPrimPaths=[UR_STAGE_PATH]
)

simulation_app.update()

# need to initialize physics getting any articulation..etc
simulation_context.initialize_physics()

simulation_context.play()

while simulation_app.is_running():

    # Run with a fixed step size
    simulation_context.step(render=True)

    # Tick the Publish/Subscribe JointState, Publish TF and Publish Clock nodes each frame
    og.Controller.set(
        og.Controller.attribute("/ActionGraph/OnImpulseEvent.state:enableImpulse"), True
    )

simulation_context.stop()
simulation_app.close()
