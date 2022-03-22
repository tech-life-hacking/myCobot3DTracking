from pymycobot.mycobot import MyCobot

class Driver():
    def __init__(self, thresholds):
        self.mc = MyCobot('/dev/ttyAMA0',1000000)
        self.thresholds = thresholds

    def rotate(self, coordinates):
        self.mc.sync_send_angles([coordinates[2],coordinates[0],-coordinates[0],coordinates[1],0,90],100, timeout=0.001)

    def guard(self, coordinates):
        tmp = []
        for coordinate, threshold in zip(coordinates, self.thresholds):
            if coordinate >= threshold:
                tmp.append(threshold)
            elif coordinate <= -threshold:
                tmp.append(-threshold)
            else:
                tmp.append(coordinate)
        return tmp