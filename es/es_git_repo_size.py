#!/usr/bin/env python3
import subprocess
import sys, json
from time import time

from os.path import dirname, abspath

if __file__:
    cmsbot_dir = dirname(dirname(abspath(__file__)))
else:
    cmsbot_dir = dirname(dirname(abspath(sys.argv[0])))
sys.path.insert(0, cmsbot_dir)
from es_utils import send_payload

repo = sys.argv[1]
e, o = subprocess.getstatusoutput("git clone --bare https://github.com/%s.git repo" % repo)
if e:
    print(o)
    sys.exit(1)

e, size = subprocess.getstatusoutput(
    "du -k -s -c repo/objects/pack/ | grep total | awk '{print $1}'"
)
if e:
    print(size)
    sys.exit(1)

e, o = subprocess.getstatusoutput("ls -d repo/objects/pack/pack-*.pack")
if e:
    print(o)
    sys.exit(1)

rid = o.split("/")[-1][5:-5]

payload = {}
payload["repository"] = repo
payload["size"] = int(size)
payload["@timestamp"] = int(time() * 1000)
index = "git-repository-size"
document = "stats"
send_payload(index, document, rid, json.dumps(payload))
