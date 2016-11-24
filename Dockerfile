FROM resin/raspberrypi-python:2.7-slim

RUN \
 apt-get update -y && \
 apt-get install -y python-smbus && \
 apt-get clean

RUN pip install docker-py rpi-lcd

ADD app.py /app/

CMD ["python", "/app/app.py"]