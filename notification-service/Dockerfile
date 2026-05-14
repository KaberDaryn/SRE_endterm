FROM python:3.7
COPY requirements.txt /notifyapp/requirements.txt
WORKDIR /notifyapp
RUN pip install -r requirements.txt
COPY . /notifyapp
ENTRYPOINT ["python"]
CMD ["run.py"]
