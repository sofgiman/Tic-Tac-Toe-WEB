FROM python:latest

WORKDIR /usr/app/src

#COPY requirements.txt requirements.txt

#RUN pip install -r requirements.txt 

COPY . .

CMD [ "python" , "./server.py" ]
