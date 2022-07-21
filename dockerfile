FROM ubuntu:latest

LABEL version = '0.1'
LABEL master = 'Neveric'

RUN apt-get update && apt-get upgrade -y

RUN apt-get install python3 -y

RUN apt-get install pip -y

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

ADD ./* /Marisabot/

EXPOSE 696

CMD [ "python3" , "./Marisabot/Marisabot.py" ]
