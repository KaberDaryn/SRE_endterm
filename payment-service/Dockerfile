FROM python:3.7
COPY requirements.txt /payapp/requirements.txt
WORKDIR /payapp
RUN pip install -r requirements.txt
COPY . /payapp
ENTRYPOINT ["python"]
CMD ["run.py"]
