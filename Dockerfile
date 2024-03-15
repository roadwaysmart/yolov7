FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /yolov7
RUN apt update && apt install -y locales python3 python3-pip iputils-ping curl vim \
    zip htop screen libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

COPY requirements.txt .
RUN pip install -r requirements.txt
    
RUN mkdir /coco
ENV LANG en_US.utf8

RUN curl -O -L https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7.pt
COPY . .

CMD python3 rtsp-multi.py --weights yolov7.pt --conf-thres 0.25 --img-size 640 --config config.yaml
