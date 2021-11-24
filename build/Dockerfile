ARG REGISTRY_GROUP_URL
FROM ${REGISTRY_GROUP_URL}/alphaceti/default-python:0.1.5 as base
ENV PROMETHEUS_MULTIPROC_DIR="/usr/src/app/prometheus" \
    PATH="${PATH}:/home/teabot/.local/bin"
ADD app /usr/src/app
RUN addgroup -S teabot && \
    adduser -S teabot -G teabot && \
    chmod +x /usr/src/app/* && \
    chown -R teabot:teabot /usr/src/app && \
    apk add --update --no-cache
EXPOSE 5000/tcp
USER teabot
WORKDIR /usr/src/app
RUN pip3 install -r ./requirements.txt
ENTRYPOINT [ "./entry.sh" ]
