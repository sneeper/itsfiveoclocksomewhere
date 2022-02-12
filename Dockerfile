FROM python:3.10-slim


#RUN dnf install -y python36 python3-flask
#COPY . /usr/local/fiveoclocksomewhere
#EXPOSE 80
#WORKDIR /usr/local/fiveoclocksomewhere
#ENTRYPOINT ["/usr/local/fiveoclocksomewhere/fiveoclocksomewhere"]


ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 2 --timeout 0 main:app

