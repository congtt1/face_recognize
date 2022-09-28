import os
import argparse
import sys

if __name__ == "__main__":
    params = sys.argv
    if len(params) < 2:
        exit()
    action = params[1]
    parser = argparse.ArgumentParser()

    actions = ["server_detect"]
    parser.add_argument('action', type=str, choices=actions, help='Action name: {}'.format("|".join(actions)), default=None)

    if action == 'server_detect':
        from tools.appearance_server import serve
        serve(50100)