import os,sys,logging,time
from fabric.state import env
from fabric.api import env,local,run,sudo,put,cd,lcd,puts,task,get,hide
from settings import BUCKET_NAME
import data
from settings import USER,private_key,HOST
env.user = USER
env.key_filename = private_key
env.hosts = [HOST,]
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/fab.log',
                    filemode='a')


@task
def notebook():
    """
    Run IPython notebook on an AWS server
    run("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.key -out mycert.pem")
    c = get_config()
    c.NotebookApp.open_browser = False
    c.NotebookApp.ip = '0.0.0.0'
    c.NotebookApp.port = 8888
    c.NotebookApp.certfile = u'/home/ubuntu/mycert.pem'
    c.NotebookApp.enable_mathjax = False
    c.NotebookApp.password = u'{}'
    #--certfile=mycert.pem
    :return:
    """
    from IPython.lib.security import passwd
    command = "ipython notebook --ip=0.0.0.0  --NotebookApp.password={} --no-browser".format(passwd())
    print command
    run(command)



@task
def setup():
    """
    Task for initial set up of AWS instance.
    """
    sudo("chmod 777 /mnt/")
    run("cp -r index /mnt/")




@task
def connect():
    """
    Creates connect.sh for the current host
    :return:
    """
    fh = open("connect.sh",'w')
    fh.write("#!/bin/bash\n"+"ssh -i "+env.key_filename+" "+"ubuntu"+"@"+HOST+"\n")
    fh.close()


@task
def server(rlocal=False):
    """
    start server
    """
    if rlocal:
        local('python server.py')
    else:
        run('python server.py')


@task
def index():
    """
    Index images
    """
    local('dev_appserver.py .')


@task
def clear():
    """
    delete logs
    """
    local('rm logs/*.log &')
