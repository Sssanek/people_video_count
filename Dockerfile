FROM python:3.10-buster AS base

WORKDIR /usr/src/app/

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 liblzma-dev -y
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install --user torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt
COPY . /usr/src/app/

CMD ["python", "main.py"]