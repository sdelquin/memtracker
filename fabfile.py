from fabric.api import local, prefix, cd, run, env, get
from config import config

env.hosts = ["production"]


def deploy():
    local("git push")
    with prefix("source ~/.virtualenvs/memtracker/bin/activate"):
        with cd("~/memtracker"):
            run("git pull")
            run("pip install -r requirements.txt")
            run("./run.sh")


def download_db():
    get("~/memtracker/{}".format(config.DATABASE), ".")
