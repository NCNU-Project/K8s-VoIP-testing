FROM python:3.9

COPY requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py entrypoint.sh /

CMD ["/entrypoint.sh"]
