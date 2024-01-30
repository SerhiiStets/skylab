FROM python:3.9

WORKDIR ./app

COPY requirements.txt .
COPY README.md .

RUN pip install -r requirements.txt

COPY ./skylab ./skylab

CMD [ "python", "skylab"]
