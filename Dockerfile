FROM python:3.7-stretch

COPY requirements.txt /

RUN pip install -r /requirements.txt

RUN apt-get install -y ffmpeg && \
    apt-get install -y libopus0 opus-tools

COPY . /

CMD [ "python3", "bot.py" ]
