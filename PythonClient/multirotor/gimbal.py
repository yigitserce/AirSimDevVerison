import setup_path
import airsim

import time

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# print("Taking off")
# client.takeoffAsync().join()
# print("Ready")

print(client.simGetCameraInfo("0"))

for i in range(5):
    # time.sleep(6)
    # camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0.5, 0.5, 0.1))
    # client.simSetCameraPose("1", camera_pose)

    time.sleep(6)
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(-0.2, -0.2, -0.1))
    client.simSetCameraPose("0", camera_pose)
