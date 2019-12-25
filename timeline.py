from nostalgia.utils import load_entry

load_entry()

import time
import os
import numpy as np
from flask import Flask, request, make_response
from flask_cors import CORS

from plot_graph import plot_graph

from preconvert.output import simplejson as json

res = None
last = None

app = Flask(__name__)
app.secret_key = os.urandom(12)
CORS(app)

loaded = set()


@app.route("/image")
def image():
    global last
    index = request.values["index"]
    html = request.values.get("html")
    if index == "undefined":
        return None
    origin = last.get_original(int(index))
    fname = origin.get("image", origin.get("path", origin.get("url")))
    if not fname or fname.endswith("mp4"):
        return None
    fname = fname.replace("file://", "")
    with open(fname, "rb") as f:
        img = f.read()
        if html == "1":
            return '<html><body><img src="/image?index={}" /></body></html>'.format(index)
        resp = make_response(img)
        ext = fname.split(".")[-1]
        resp.headers = {"Content-Type": "application/" + ext}
        return resp


# "http://localhost:5000/?start=2019-09-25%2014:00&end=2019-09-25%2020:00"


@app.route("/")
def root():
    from nostalgia.ndf import Results, registry

    global last, res
    if res is None:
        res = Results.merge(*[v for k, v in registry.items() if v.df_name != "results"])
    start = request.values.get("start")
    end = request.values.get("end")
    containing = request.values.get("containing") or request.values.get("q")
    allowed_types = [
        k for k, v in request.values.items() if k not in ["start", "end"] and v == "on"
    ]
    if allowed_types:
        new = False
        for tp in allowed_types:
            if tp not in loaded:
                print("loading", tp)
                t1 = time.time()
                registry[tp].load()
                print("loaded", tp, "in", time.time() - t1)
                loaded.add(tp)
                new = True
        if new:
            res = Results.merge(*[v for k, v in registry.items() if v.df_name != "results"])
    if start is not None and end is not None:
        last = res.at_time(start, end)
    elif start is not None:
        last = res.at_time(start)
    else:
        last = res
    if containing is not None:
        last = last.containing(containing)
    if allowed_types:
        last = last[last.type.isin(allowed_types)]
    else:
        allowed_types = list(registry.keys())
    num_results = last.shape[0]
    last = last.sort_values("end")
    if not last.empty:
        max_n = 600 / len(last.type.unique())
        last["sel"] = False
        for name, group in last.groupby("type"):
            mod = 1 if group.shape[0] < max_n else int(group.shape[0] / max_n)
            last.loc[last.type == name, "sel"] = [x % mod == 0 for x in range(group.shape[0])]
        last = Results(last[last.sel])
    else:
        last = Results(last)
    # last = Results(last.tail(1000))
    last.add_heartrate()
    return plot_graph(
        last, allowed_types, num_results, start or "365 days ago", end or "1 days ago"
    )


@app.route("/info")
def info():
    global last
    index = request.values["index"]
    if index == "undefined":
        return None
    origin = last.get_original(int(index))
    return json.dumps(
        {k: v for k, v in dict(origin).items() if not (isinstance(v, float) and np.isnan(v))},
        indent=4,
    )


if __name__ == "__main__":
    app.run()
