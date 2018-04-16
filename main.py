import subprocess
import re
import config
from models import MemHistory
import jinja2
import datetime
import logging
import logging.handlers
import peewee

# Logging configuration
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler("memtracker.log",
                                               maxBytes=1048576,
                                               backupCount=1)
formatter = logging.Formatter("%(asctime)s - %(name)s [%(levelname)s] \
%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

MemHistory.create_table(True)
if not (MemHistory.select().
        where(MemHistory.date == datetime.date.today()).count()):
    cmd = f"ps -u {config.USER} -o pid,rss,command"
    logger.debug(f"Running {cmd}")
    lines = subprocess.check_output(cmd, shell=True).\
        decode("utf-8").\
        split("\n")
    logger.info("Reading memory from shell output")
    for app, command in config.APPS.items():
        aux = 0
        for line in lines:
            r = re.match(r"^\s*\d+\s*(\d+).*{}.*$".format(command), line)
            if r:
                aux += int(r.group(1))
        MemHistory.create(app=app, used_mem=float(aux) / 1024)

memhistory = []

logger.info("Querying distinct dates")
dates = MemHistory.select(MemHistory.date).\
    distinct().\
    order_by(MemHistory.date.desc()).\
    limit(config.MAX_DATES)
dates = reversed([d.date for d in dates])
for date in dates:
    record = {"date": date, "used_mem": []}
    for app in config.APPS.keys():
        try:
            m = MemHistory.get((MemHistory.date == date) &
                               (MemHistory.app == app))
        except peewee.DoesNotExist:
            used_mem = 0
        else:
            used_mem = m.used_mem
        record["used_mem"].append(used_mem)
    # total used memory
    record["used_mem"].append(sum(record["used_mem"]))
    memhistory.append(record)
logger.debug(memhistory)

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
template = template_env.get_template("index.tmpl.html")
rendered_template = template.render(apps=config.APPS.keys(),
                                    num_apps=len(config.APPS.keys()),
                                    memhistory=memhistory,
                                    user=config.USER,
                                    place=config.PLACE)
with open("index.html", "w") as f:
    f.write(rendered_template)
