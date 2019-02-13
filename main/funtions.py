import re
import random
import subprocess
import sys


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