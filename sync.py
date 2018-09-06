# coding=utf-8
"""Parse the README.md file and extract the directory and file structure. 

TODO: Search for urls on MS Academic/Google scholar if missing.

Author: Eric Wan
Email:  ericwannn@foxmail.com
Date:   2018-09-06
"""
from __future__ import print_function
import os
import shlex
import datetime
import subprocess
import time
from collections import namedtuple

_paper    = "[paper]"
_tutorial = "[tutorial]" 

def execute_command(cmd, cwd=None, timeout=None, shell=False):
    """Execute a shell command. Encapsulate subprocess.Popen. Support timeout and stdout/stderr

    Parameter: 
        cmd:        command
        cwd:        change the directory to cwd if it's set
        timeout:    in second
        shell:      if the command is executed by shell
    Raises:        Exception: timeout
    Return:        returncode
    """
    cmd_list = cmd if shell else shlex.split(cmd)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    
    subp = subprocess.Popen(
        cmd_list, cwd=cwd, stdin=subprocess.PIPE,
        shell=shell, bufsize=4097
        )
    
    while subp.poll() is not None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：{}".format(cmd))
            
    return subp.returncode

def download_file(url, file_name, directory):
    execute_command(
        "wget {} -nv -O {}".format(url, file_name),
        cwd=directory,
        shell=True
        )

def make_directory(dir_name, directory):
    execute_command(
        "mkdir {}".format(dir_name),
        cwd=directory,
        shell=True
        )

def sync_papers():
    root_path = os.getcwd()
    src_list = []
    src = namedtuple("src", ["file_name", "file_type", "directory", "url"])
    start = False
    with open("README.md") as f:
        for _ in range(40): next(f) # Skip instructions part
        for line in f.readlines():
            sline = line.strip().split()
            if not len(sline):continue
            if sline[0] == "##": # Subjects i.e. computer_vision
                h2 = "_".join(sline[1:])
                if h2 not in os.listdir(root_path):
                    make_directory(h2, root_path)
                current_path = os.path.join(root_path, h2)
            elif sline[0] == "###": # Domains i.e. OCR
                h3 = "_".join(sline[1:])
                if h3 not in os.listdir(current_path):
                    make_directory(h3, current_path)
                current_path = os.path.join(current_path, h3)
            elif sline[0] == "####": # Title of the resource 
                file_type = sline[1]
                if file_type == _paper: file_name = "_".join(sline[2:]) + ".pdf"
            elif sline[0] == "*" and sline[1].startswith("[url]"):
                url  = line[8:-2]
                src_list.append(src(file_name, file_type, current_path, url))
    for file_name, file_type, directory, url in src_list:
        if file_type == _paper:
            if file_name not in os.listdir(directory):
                download_file(
                    url, file_name, directory
                    )
            else:
                print("The file {} already exists!\n".format(file_name))


if __name__=="__main__":
    sync_papers()
