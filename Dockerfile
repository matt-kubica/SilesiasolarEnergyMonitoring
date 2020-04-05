# base Image
FROM python:3.7.6

# create and set working directory
RUN mkdir /app
WORKDIR /app

# add current directory code to working directory
ADD . /app/


# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 


# install system dependencies and psycopg2 dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        postgresql \
        gcc \
        musl-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*



# install environment dependencies
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv

# install project dependencies
RUN pipenv install --skip-lock --system --dev

# ENTRYPOINT ["/app/entrypoint.sh"]
# CMD gunicorn silesiasolar_backend.wsgi:application --bind 0.0.0.0:$PORT --chdir silesiasolar_backend --preload
CMD python silesiasolar_backend/manage.py runserver