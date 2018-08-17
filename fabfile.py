from fabric.api import local, cd, run, env, get
import config

env.hosts = ["production"]


def deploy():
    local("git push")
    with cd("~/memtracker"):
        run("git pull")
        run("pipenv install")


def download_db():
    get("~/memtracker/{}".format(config.DATABASE), ".")
