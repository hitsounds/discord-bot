FROM python:3.7-stretch

COPY requirements.txt /

RUN pip install -r /requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y ffmpeg libopus0

COPY . /

CMD [ "python3", "bot.py" ]
