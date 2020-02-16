FROM python

RUN mkdir /nostalgia_timeline

WORKDIR /nostalgia_timeline

COPY . /nostalgia_timeline

RUN pip install -r requirements.txt
RUN pip install nostalgia_chrome

ENTRYPOINT ["python", "timeline.py" ]
