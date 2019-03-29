FROM python:3.7-stretch	

WORKDIR /usr/src/app

VOLUME ./persist

COPY requirements.txt .

RUN apt-get update && \	
    apt-get upgrade -y && \	
    apt-get install -y ffmpeg libopus0 && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]