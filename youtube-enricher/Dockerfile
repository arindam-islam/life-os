FROM python:3.12-slim

RUN pip install --no-cache-dir flask yt-dlp

WORKDIR /app
COPY app.py /app/app.py

EXPOSE 8080

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=8080"]
