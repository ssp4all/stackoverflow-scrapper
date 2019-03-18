""" 
This file contains all utility functions!
"""
import os
import subprocess
import time


def toString(byte):
    return byte.decode("utf-8").strip()


def run(args):
    process = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()


def runrealtime(args):
    process = subprocess.Popen(
        args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    
    while process.poll() is None:
        output = process.stdout.readline().decode("utf-8").strip()
        print(output)

    return process.communicate()

def clear_terminal():
    """Clear terminal """
    time.sleep(3)
    if os.name != 'nt':
        os.system("clear")
    else:
        os.system("cls")
