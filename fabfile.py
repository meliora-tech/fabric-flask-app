"""
Created on Wed 16 Feb 2023

@author: GTZ
"""

from fabric import Connection, task



HOST_NAME    = ""
HOST_USER    = ""
PEM_KEY_FILE = ""
GITHUB_LINK  = ""



@task
def deploy(ctx):
    """
    Deploy the application for the first time on a new server
    """
    with Connection(
        HOST_NAME,
        user=HOST_USER,
        connect_kwargs={"key_filename": PEM_KEY_FILE}
    ) as c:

        # ===============================
        #  Step 1: Update the packages
        # ===============================
        c.run("sudo apt update -y")


        # ===============================
        #  Step 2: Install the required packages
        # ===============================
        c.run("sudo apt-get install git build-essential python3-dev python3-venv python3 python3-pip python3.8-venv python3.8-dev libxml2-dev libxslt1-dev libffi-dev zlib1g-dev libssl-dev gettext libpq-dev libmariadb-dev libjpeg-dev libopenjp2-7-dev -y")


        
        # ===============================
        #  Step 3: Create a python environment
        # ===============================
        c.run("sudo python3.8 -m venv venv")


        # ===============================
        #  Step 4: Clone the repo 
        # ===============================
        c.run(f"sudo git clone {GITHUB_LINK}")

        # ===============================
        #  Step 5: Install the requirements 
        #  First activate the environment
        # ===============================
        c.run("source venv/bin/activate && cd fabric-flask-app && pip3 install -r requirements.txt")

        # ===============================
        #  Step 6: Start the application 
        # ===============================
        c.run("source venv/bin/activate && cd fabric-flask-app && nohup python3.8 start_app.py &")



@task
def redeploy(ctx):
    """
    Deploy the  updated version of the application
    """
    with Connection(
        HOST_NAME,
        user=HOST_USER,
        connect_kwargs={"key_filename": PEM_KEY_FILE}
    ) as c:

        # ===============================
        #  Step 1: Install the requirements  
        # ===============================
        c.run("source venv/bin/activate && cd fabric-flask-app && pip3 install -r requirements.txt")

        # ===============================
        #  Step 2: Pull the repo 
        # ===============================
        c.run("cd fabric-flask-app && sudo git pull")

        # ===============================
        #  Step 3: Stop and start the app 
        # ===============================
        c.run("sudo kill -s SIGTERM `ps -ef | pgrep -f python3.8`")
        c.run("source venv/bin/activate && cd fabric-flask-app && nohup python3.8 start_app.py &")



@task
def rollback(ctx):
    """
    Rollback to the last version of the application
    """
    with Connection(
        HOST_NAME,
        user=HOST_USER,
        connect_kwargs={"key_filename": PEM_KEY_FILE}
    ) as c:

        # ========================================
        #  Step 1: Get the previous deployment sha  
        # ========================================
        latest_sha = c.run("cd fabric-flask-app && git log --pretty=format:'%h' -n 1")
        clean_sha  = latest_sha.stdout.strip()


        # ========================================
        #  Step 2: Revert to the commit 
        # ========================================
        c.run(f"cd fabric-flask-app && git revert {clean_sha}")



        # ===============================
        #  Step 2: Pull the repo 
        # ===============================
        c.run("cd fabric-flask-app && sudo git pull")

        # ===============================
        #  Step 3: Stop and start the app 
        # ===============================
        c.run("sudo kill -s SIGTERM `ps -ef | pgrep -f python3.8`")
        c.run("source venv/bin/activate && cd fabric-flask-app && nohup python3.8 start_app.py &")