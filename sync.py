# coding=utf-8
from __future__ import print_function
import os
import platform
import shlex
import datetime
import subprocess
import time
from collections import namedtuple

def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    """Execute a shell command. Encapsulate subprocess.Popen. Support timeout and stdout/stderr

    @Parameter: 
        cmdstring:  command
        cwd:        change the directory to cwd if it's set
        timeout:    in second
        shell:      if the command is executed by shell

    @Return:        returncode
    @Raises:        Exception: timeout
    """
    cmdstring_list = cmdstring if shell else shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    
    sub = subprocess.Popen(
        cmdstring_list, cwd=cwd, stdin=subprocess.PIPE,
        shell=shell, bufsize=4097
        )
    
    while sub.poll() is not None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：{}".format(cmdstring))
            
    return str(sub.returncode)

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
    system = platform.system().lower()
    assert system in ["windows", "linux", "darwin"]
    src_list = []
    src = namedtuple("src", ["file_name", "file_type", "directory", "url"])
    with open("README.md") as f:
        for line in f.readlines():
            sline = line.strip().split()
            if not len(sline): 
                continue
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
                file_name = "_".join(sline[2:]) + ".pdf"
            elif sline[0] == "*" and sline[1].startswith("[url]"):
                url  = line[8:-2]
                src_list.append(src(file_name, file_type, current_path, url))
    for file_name, file_type, directory, url in src_list:
        if file_type == "[paper]":
            if file_name not in os.listdir(directory):
                download_file(
                    url, file_name, directory
                    )
            else:
                print("The file {} already exists!".format(file_name))


if __name__=="__main__":
    sync_papers()
