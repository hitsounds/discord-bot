FROM python:3.7-stretch	

WORKDIR /usr/src/app

VOLUME ./persist

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt	

RUN apt-get update && \	
    apt-get upgrade -y && \	
    apt-get install -y ffmpeg libopus0	

COPY . .

CMD ["python3", "main.py"]