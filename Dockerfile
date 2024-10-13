FROM python:3.8-slim

WORKDIR /api-flask

COPY environment/ /api-flask/environment
COPY services/ /api-flask/services/
COPY data/ /api-flask/data/
COPY models/ /api-flask/models/
COPY application.py requirements.txt  /api-flask/

RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "application:app", "-b", "0.0.0.0:5000", "-w", "4"]