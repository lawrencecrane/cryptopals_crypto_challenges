FROM python:3.6-alpine

WORKDIR /home/crypto

RUN pip install --upgrade pip
RUN pip install pytest
RUN pip install hypothesis

CMD ["sh"]
