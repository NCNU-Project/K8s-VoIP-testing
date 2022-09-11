FROM python:3.8

COPY Pipfile Pipfile.lock /
ENV PYTHONUNBUFFERED=0
RUN ["pip", "install", "pipenv"]
RUN ["pipenv", "install"]
COPY main.py /
ENTRYPOINT ["pipenv", "run", "python", "/main.py"]
