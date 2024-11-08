FROM python:3.11-alpine
WORKDIR /code

RUN --mount=type=cache,target=/var/cache/apk apk add ffmpeg
COPY . /code

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt


