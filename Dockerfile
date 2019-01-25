FROM python:latest

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN git clone https://github.com/Hitsounds/discord-bot.git

RUN cd /discord-bot && pip install -r requirements.txt

CMD [ "python3", "./discord-bot/bot.py" ]