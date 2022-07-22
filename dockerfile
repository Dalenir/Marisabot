FROM python:3.8

ENV PYTHONUNBUFFERED=1

LABEL version = '0.2'
LABEL master = 'Neveric'

RUN mkdir /Snow
WORKDIR /Snow

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

COPY ./* /Snow/

EXPOSE 696

CMD ["Marisabot.py"]
