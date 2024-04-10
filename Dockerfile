FROM docker.io/bitnami/python:3.10-debian-11
LABEL Daren_salazar "sdaren6@gmail.com"
EXPOSE 80

WORKDIR /app

RUN install_packages libpq-dev python3-dev
COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Bogota
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /app

CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:80", "--access-logfile", "-", "--error-logfile", "-", "--workers=4"]
