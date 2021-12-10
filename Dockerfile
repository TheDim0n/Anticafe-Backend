FROM python:3.9-slim

RUN pip install --upgrade pip

WORKDIR /src

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]
