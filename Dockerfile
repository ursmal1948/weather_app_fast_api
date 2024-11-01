FROM python:3.12
EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFERED 1
WORKDIR /webapp
COPY Pipfile Pipfile.lock /webapp/
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile
COPY . /webapp/