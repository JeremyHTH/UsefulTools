FROM ubuntu:focal-20230801

WORKDIR /code

RUN apt-get -y update
RUN apt-get install ffmpeg libsm6 libxext6 libxcb-xinerama0 -y
RUN apt-get install -y libxcb-util-dev
RUN apt-get install -y python3
RUN apt-get -y install python3-pip
RUN pip install --no-cache-dir --upgrade pip
RUN apt-get install qt5-default -y
RUN pip install PyQt5
RUN pip install pytube


ENV QT_DEBUG_PLUGINS=1

COPY / .

CMD ["python3", "MainUI.py"]