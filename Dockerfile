FROM python:3.6-alpine

WORKDIR /home/crypto

RUN pip install --upgrade pip
RUN pip install pytest hypothesis
RUN apk add aspell aspell-en enchant && pip install pyenchant

CMD ["sh"]
