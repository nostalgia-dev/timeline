FROM python

RUN mkdir /nostalgia_timeline

WORKDIR /nostalgia_timeline

COPY . /nostalgia_timeline

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "timeline.py" ]
