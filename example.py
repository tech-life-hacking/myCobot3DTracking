import sys,os
sys.path.append('depthai_hand_tracker')
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
from depthai_hand_tracker.HandTrackerEdge import HandTracker
import controller
import driver

# coordinates = [r, theta, psi]
INITIALCOORDINATE = [0, 0, 0]
THRESHOLDS = [90, 160, 90]

# [center camera frame x, center camera frame y, distance between hands and camera]
TARGETVALUES = [0.5, 0.5, 0.5]

# PID
PIDX = [10, 10, 3.75]
PIDY = [6.5, 5, 2.5]
PIDZ = [50, 30, 20]

INITIALGESTURE = 'FIVE'

if __name__ == "__main__":
    # setup cam and recognizer
    tracker = HandTracker(xyz=True, use_gesture=True, solo=True)
    camera_frame_size = tracker.frame_size
    gestures = INITIALGESTURE

    # setup controller
    pidX = controller.PID(PIDX)
    pidY = controller.PID(PIDY)
    pidZ = controller.PID(PIDZ)
    pidX.setTargetPosition(TARGETVALUES[0])
    pidY.setTargetPosition(TARGETVALUES[1])
    pidZ.setTargetPosition(TARGETVALUES[2])

    # setup driver
    drv = driver.Driver(THRESHOLDS)
    coordinates = INITIALCOORDINATE
    drv.rotate(coordinates)

    while True:
        # capture and recognize
        frame, hands, bag = tracker.next_frame()
        # spacial coordinates and gestures
        for hand in hands:
            x = hand.rect_x_center_a / camera_frame_size
            y = hand.rect_y_center_a / camera_frame_size
            z = hand.xyz[2] / 1000
            gestures = hand.gesture

        if gestures == 'ONE':
            # update error
            pidX.update(x)
            pidY.update(y)
            pidZ.update(z)

            # feedback
            coordinates[2] += pidX.output
            coordinates[1] += pidY.output
            coordinates[0] += pidZ.output

            # guard
            coordinates = drv.guard(coordinates)

            # drive motor
            drv.rotate(coordinates)