FROM  python:3.7-buster

RUN apt-get update -y
RUN apt-get install build-essential python3-dev -y

WORKDIR /usr/src/app

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh ./wait-for-it.sh
RUN chmod +x ./wait-for-it.sh
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY *py ./
COPY templates ./templates/
COPY static ./static

CMD ["./wait-for-it.sh", "db:5432", "--", "python", "./app.py" ]
