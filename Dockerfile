FROM python:3.4

RUN groupadd --gid 1000 -r uwsgi && useradd --uid 1000 -r -g uwsgi uWSGI

RUN pip install Flask==0.10.1 uWSGI
WORKDIR /app
COPY app /app
COPY cmd.sh /

USER 1000:1000
EXPOSE 9090 9191
CMD ["/cmd.sh"]
