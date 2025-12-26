ARG PYTHON_IMAGE_VERSION=python:3.12.8-alpine3.20

FROM ${PYTHON_IMAGE_VERSION}
LABEL description="Deflakyzavr (https://github.com/Legion18z/deflakyzavr) plugin."

WORKDIR /deflakyzavr
ADD . .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install .

ENTRYPOINT ["sh"]
CMD ["-c", "python -m deflakyzavr"]