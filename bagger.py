import os
import signal
import sys
import time
from datetime import datetime

import argparse


def parse_args():
    # Create the parser
    parser = argparse.ArgumentParser(description='ros2 bag recording tool')

    # Add the arguments
    parser.add_argument('-n', '--name', dest='name', required=False,
                        help='bag file name')

    parser.add_argument('-u', '--user', dest='username', default='nickgurnard',
                        help='user name of the host machine')
    
    parser.add_argument('-i', '--ip', dest='ip', default='')

    # Parse the arguments
    return parser.parse_args()

def main():

    # topic_list = ["-a"] # all topics cmd currently broken in ros

    topic_list = ["/drive",
                  "/odom",
                  "/ackermann_cmd",
                  "/map",
                  "/clicked_point",
                  "/commands/motor/speed",
                  "/initialpose",
                #   "/pf/pose/odom",
                #   "/pf/viz/inferred_pose",
                  "/scan",
                #   "/waypoint", # this needs to be an exception with -e
                  "/waypoint_vis",
                  "/cur_point_vis",
                  "/tf",
                  "/tf_static"
                  ]
    
    # exception_list = ["/waypoint"]
    
    
    print(f"there are {len(topic_list)} topics that are being subscribed to:\n")
    bash_arg = ""
    for arg in topic_list:
        print(arg)
        bash_arg += " " + arg + " "

    # bash_ex_arg = ' -x "'  
    # for ex in exception_list:
    #     bash_ex_arg += ex + "|"
    # bash_ex_arg += '" '

    print() # add a space to the terminal for viewing
    
    args = parse_args()
    
    def handler(signum, frame):
        # upon pressing ctrl+c, stop the bag recording and scp to host.
        print("stopping bag recording")
        # get the environment variable $SSH_CLIENT
        if args.ip:
            client_ip = args.ip
        else:
            client_ip = os.environ['SSH_CLIENT'].split()[0]
        # destination is the save_path but strip the last directory
        destination = save_path.rsplit('/', 1)[0]
        # scp the bag file to the host 
        scp_cmd = "scp " + "-r " + save_path + " " + args.username + "@" + client_ip + ":" + destination

        os.system(scp_cmd)
        print("bag file saved at: ", save_path)
        sys.exit(0)
        
    signal.signal(signal.SIGINT, handler)
    
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    home_dir = "~"
    bag_path = "jetson_bag_files"
    if args.name:
        save_path = os.path.join(home_dir, bag_path, args.name)
    else:
        save_path = os.path.join(home_dir, bag_path, date_time)
    
    # cmd = ['ros2', 'bag', 'record', '-s', 'mcap', '-a', '-o', save_path]
    cmd = ['ros2', 'bag', 'record', '-s', 'mcap', bash_arg, '-o', save_path]

    # cmd = ['ros2', 'bag', 'record', '-s', 'mcap', bash_arg, bash_ex_arg, '-o', save_path]

    cmd = ' '.join(cmd)
    # call cmd using os.system(cmd)
    print("calling bag command: ", cmd)
    os.system(cmd)
    time.sleep(1000000)
    
if __name__ == '__main__':
    main()
    