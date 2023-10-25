FROM python:3.10.12-alpine

WORKDIR /usr/src/app

ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./init.sh /usr/src/app/init.sh

COPY . /usr/src/app/

ENTRYPOINT [ "/usr/src/app/init.sh" ]



