FROM python:3.6

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y libopus0 ffmpeg libffi-dev

WORKDIR /app
COPY /src /app/src

CMD ["python", "src/main.py"]