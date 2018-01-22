FROM python:3.6

COPY virgool_cloud /virgool_cloud

WORKDIR /virgool_cloud

RUN pip install -r requirements.txt

CMD ["python", "./bot.py"]
