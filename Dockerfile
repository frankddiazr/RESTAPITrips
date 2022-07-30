FROM python:3.9.5

ENV PYTHONBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /jobsity
WORKDIR /jobsity
COPY . /jobsity/
RUN pip install -r requirements.txt


