FROM python:3.12.8-alpine3.20
LABEL description="Deflakyzavr (https://github.com/Legion18z/deflakyzavr) plugin."

WORKDIR /deflakyzavr
ADD . .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install .

CMD ["sh", "-c", "deflakyzavr"]