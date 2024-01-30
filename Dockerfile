FROM python:3.9

WORKDIR ./app

COPY . .

RUN pip install -r requirements.txt
RUN pip install -e .

CMD [ "skylab" ]
