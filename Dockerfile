FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

# RUN python initdb.py

CMD ["python", "app.py"]
