FROM python:3.9.5-slim-buster

WORKDIR /eyo

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

#CMD ["python", "./server.py"]
CMD tail -f /dev/null

