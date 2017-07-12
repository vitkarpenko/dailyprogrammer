import argparse
import os
import socket
import sys


def main():
    parser = argparse.ArgumentParser(description='Simple HTTP server.')
    parser.add_argument('-r', '--root', help='Root folder for server.')
    args = parser.parse_args()
    
    root = args.root

    if not os.path.isdir(root) or not os.access(root, os.R_OK):
        raise ValueError('Incorrect or not readable root folder.')

    # TODO
    server_socket = 


if __name__ == '__main__':
    main()
