FROM python:3.10

WORKDIR /app

COPY ./requirements.txt .

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update \
  && apt-get install netcat gcc \
  && apt-get clean

COPY . .

EXPOSE 8010

CMD ["sh", "start_app.sh"]