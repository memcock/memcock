FROM gliderlabs/alpine:edge

ENV MODE prod

ADD https://github.com/just-containers/s6-overlay/releases/download/v1.18.1.5/s6-overlay-amd64.tar.gz /tmp/s6-overlay-amd64.tar.gz
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C /

COPY ./requirements.txt /tmp/requirements.txt
RUN apk --update add python3 uwsgi uwsgi-python3 postgresql-libs && \
	apk add --virtual build-deps build-base postgresql-dev python3-dev && \
	python3 -m pip install -r /tmp/requirements.txt && \
	apk del build-deps

COPY ./s6/services.d /etc/services.d
COPY ./s6/init /etc/cont-init.d

COPY . /app
WORKDIR /app

EXPOSE 80 443
ENTRYPOINT /init
