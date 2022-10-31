import os
import sys
import matplotlib
import webbrowser
import jinja2
from nostalgia.interfaces.chat import ChatInterface
from nostalgia.utils import load_entry

nostalgia_entry = load_entry()

is_chat: set[str] = set()
for x in dir(nostalgia_entry):
    if x.startswith("__"):
        continue
    if x[0] == x[0].upper():
        cls = getattr(nostalgia_entry, x)
        if ChatInterface in cls.mro():
            is_chat.add(cls.class_df_name())


# tab = {
#     'tab:blue',
#     'tab:orange',
#     'tab:green',
#     'tab:red',
#     'tab:purple',
#     'tab:brown',
#     'tab:pink',
#     'tab:gray',
#     'tab:olive',
#     'tab:cyan',
# }

# tab = [matplotlib.colors.get_named_colors_mapping()[x] for x in tab]

tab = [
    ("#010505", "#97B0FD"),
    ("#08201F", "#97B0FD"),
    ("#0C3130", "#97B0FD"),
    ("#124949", "#97B0FD"),
    ("#176160", "#97B0FD"),
    ("#1E7D7C", "#97B0FD"),
    ("#3DFFFC", "#97B0FD"),
    ("#010505", "#97B0FD"),
    ("#08201F", "#97B0FD"),
    ("#0C3130", "#97B0FD"),
]


def c(name):
    # XXX: make this so that they always get the same colors, even with new hashing
    if name not in color_mapping:
        color_mapping[name] = tab[len(color_mapping) % len(tab)]
    return color_mapping[name]


color_mapping = {}
known_groups = set()


def show_row(row, _id, group_counts, groups):
    x = row
    back, front = c(x.type)
    style = "background-color: " + back + "; color: " + front
    try:
        if x.heartrate_value > 80:
            style += "; border: 1px solid #ff7f6e"
    except AttributeError:
        pass
    data = {
        "id": _id,
        "content": str(x.title)[:50] if x is not None else "...",
        "group": x.type,
        "style": style,
    }
    if x.type in is_chat:
        if x.sender == "me":
            data["className"] = "chat right"
        else:
            data["className"] = "chat left"

    if x.type not in groups:
        groups[x.type] = {
            "id": x.type,
            "content": x.type,
            # intervals to the bottom, then based on how many items are fill from bottom
            # if height based rendering this is the best
            # inverse this logic if height is not fixed
            "value": (-group_counts[x.type] / 100) + 1000 * (x.type.endswith("places"))
            # + 500 * (x.type == "heartrate")
        }
    known_groups.add(x.type)
    try:
        data["start"] = x.start.isoformat()
        # if type is on an interval, add it to the data
        if x.interval:
            data["end"] = x.end.isoformat()
    except AttributeError:
        print("AttributeError", _id)
        pass
    return data


# todo: make it a template
with open("templates/plot_graph.html") as f:
    tmpl = f.read()
    tmpl = jinja2.Template(tmpl)


def plot_graph(res, form_groups, num_results, start=None, end=None):
    import json

    groups = {}
    if not color_mapping:
        for x in sorted(res.type.unique()):
            c(x)
    group_counts = res.type.value_counts()
    items = json.dumps([show_row(x, n, group_counts, groups) for n, (_, x) in enumerate(res.iterrows())])
    group_on_off = {k: "checked" if k in form_groups else "" for k in known_groups}
    return tmpl.render(
        colors=tab,
        items=items,
        color_mapping=color_mapping,
        groups=list(groups.values()),
        group_inputs=group_on_off,
        num_results=num_results,
        start=start,
        end=end,
    )
