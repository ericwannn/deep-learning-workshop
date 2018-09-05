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
        shell=shell, bufsize=4096
        )
    
    while sub.poll() is not None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：{}".format(cmdstring))
            
    return str(sub.returncode)

def download_file(url, file_name, directory):
    execute_command(
        "wget {} -O {}".format(url, file_name),
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
    current_path = os.getcwd()
    system = platform.system().lower()
    assert system in ["windows", "linux", "darwin"]
    download_list = []
    with open("README.md") as f:
        for line in f.readlines():
            sline = line.strip().split()
            if not len(sline): 
                continue
            if sline[0] == "##":
                h2 = "_".join(sline[1:])
            elif sline[0] == "###":
                h3 = "_".join(sline[1:])
            elif sline[0] == "####":
                file_name = "_".join(sline[1:]) + ".pdf"
            elif sline[1].startswith("[url]"):
                url  = line[8:-2]
                if system == "windows":
                    directory = current_path + "\\{}\\{}\\".format(h2, h3)
                else:
                    directory = current_path + "/{}/{}/".format(h2, h3)
                
                if file_name not in os.listdir(directory):
                    download_file(
                        url, file_name, directory
                        )
                else:
                    print("The file {} already exists!".format(file_name))


if __name__=="__main__":
    sync_papers()
