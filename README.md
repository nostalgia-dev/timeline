## nostalgia-timeline

This repo contains the timeline app for [nostalgia](https://nostalgia-dev.github.io).

### Run the timeline

Using Python:

    git clone https://github.com/nostalgia-dev/timeline
    pip install -r requirements.txt
    python timeline.py

Or using Docker:

    docker build -t nostalgia_timeline .
    docker-compose up

Then visit http://localhost:5551

Except: it will not really work yet since you should...

### Add your own data

Get some [sources connected](https://github.com/nostalgia-dev/nostalgia#available-data-bindings).

Make sure you are loading those sources in `~/nostalgia_data/nostalgia_entry.py`.

For example, to enable loading [Fitbit](https://github.com/nostalgia-dev/nostalgia_fitbit) and [Chrome History](https://github.com/nostalgia-dev/nostalgia_chrome) after setting up those sources:

```python
# File contents of ~/nostalgia_data/nostalgia_entry.py below
from nostalgia.sources.fitbit.heartrate import FitbitHeartrate
from nostalgia.sources.chrome_history import WebHistory

heartrate = FitbitHeartrate.register()
web_history = WebHistory.register()
```

### Updating the code

    git pull

### Developing / Contributing

Suggested to install "Using Python", and then visit http://localhost:5551/sample to see it work without data.

### Screenshots

<img src="https://raw.githubusercontent.com/nostalgia-dev/timeline/master/timeline1.jpg" />

Driving, music, heartrate (my heartrate got lower with less traffic):

<img src="https://raw.githubusercontent.com/nostalgia-dev/timeline/master/less_traffic_jam.png" />
