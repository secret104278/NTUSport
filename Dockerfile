FROM python:3
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install pipenv
RUN pipenv --python 3
RUN pipenv install --system --deploy
