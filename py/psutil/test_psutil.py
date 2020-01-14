import json
import psutil


import os
ref = {}
for p in os.listdir("/proc/"):
    if not p.isdigit():
        continue
    d = "/proc/%s/fd/" % p
    try:
        for fd in os.listdir(d):
            f = os.readlink(d+fd)
            if f not in ref:
                ref[f] = []
            ref[f].append(p)
    except OSError:
        pass
for (k, v) in ref.items():
    print(k, " ".join(v))


if __name__ == "__main__":

    objs = []

    connections = open_files = list()

    objs.append(connections)
    objs.append(open_files)

    for proc in psutil.process_iter():
        try:
            open_files.extend(proc.open_files())
        except Exception as e:
            print(e)

    with open('test_psutil.json', 'w') as f:
        json.dump(objs, f, indent=4)
