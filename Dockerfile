FROM  python:3.8

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app

COPY requirements.txt /tmp/requirements.txt

RUN python3 -m pip install -r /tmp/requirements.txt

EXPOSE 3000

CMD ["python","aplicativo.py"]