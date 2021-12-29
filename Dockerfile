FROM python:3.7-slim-buster

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt 

COPY . ./

EXPOSE 8050

CMD [ "python", "multi_armed_bandit_example.py"]