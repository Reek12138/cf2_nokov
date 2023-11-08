from pycrazyswarm import Crazyswarm
import time
import threading
import signal  # Import the signal module

TAKEOFF_DURATION = 2.5
HOVER_DURATION = 5.0

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs
cfs = allcfs.crazyflies

def run_sequence(scf, file_name):
    coords = read_pose(file_name)
    for coord in coords:
        scf.cmdPosition([coord[0], coord[1], coord[2]], 0)
        timeHelper.sleepForRate(25)

    scf.land(targetHeight=-0.05, duration=coord[2] * 2)
    timeHelper.sleep(coord[2] * 2 + 2)

def read_pose(filename):
    with open("./xiezhuanquan/" + filename, 'r') as f:
        coords = []
        for line in f:
            parts = line.split()
            x, y, z = float(parts[0]), float(parts[1]), float(parts[2]) - 0.2
            coords.append([x, y, z])
    return coords

def main():
    Z = 1.3
    allcfs.takeoff(targetHeight=Z, duration=3.0 + Z)
    timeHelper.sleep(3 + Z)

    threads = []
    for i in range(len(cfs)):
        thread = threading.Thread(target=run_sequence, args=(cfs[i], f"{i + 1}.txt"))
        threads.append(thread)

    try:
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("Ctrl+C pressed,Exiting.")
        for cf in cfs:
            cf.land(targetHeight=-0.05, duration=4.0)
        timeHelper.sleep(4.0)
        allcfs.stop()

if __name__ == "__main__":
    main()
