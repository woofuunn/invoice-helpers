FROM python:3.13.3-slim-bookworm

WORKDIR /workdir

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "app_api.py"]