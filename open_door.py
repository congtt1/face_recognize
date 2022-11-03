import argparse
from gpio import *
parser = argparse.ArgumentParser()

if __name__ == '__main__':
    parser.add_argument('--door_id', default="cam01", type=str, help="list camera for capture, usage: 1,2 for cam01, cam02 or 0-2 for cam00, cam01, cam02. Leave it empty for all cameras")
    args = parser.parse_args()
    door_id = args.door_id
    if str(door_id) == '0':
        open_door1()
    elif str(door_id) == '1':
        open_door2()
    elif str(door_id) == 2:
        open_door3()
    elif str(door_id) == '3':
        open_door4()
