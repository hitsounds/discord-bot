FROM python:latest

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY . /

CMD [ "python3", "bot.py" ]
