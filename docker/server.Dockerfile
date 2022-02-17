FROM python:3.8 AS base
WORKDIR /app/

FROM base AS dependencies
COPY ./requirements.txt ./
RUN python3 -m venv venv && \
    venv/bin/pip install -U pip wheel setuptools && \
    venv/bin/pip install -r requirements.txt

FROM base AS release
COPY --from=dependencies /app/venv ./venv
COPY . .
EXPOSE 3579
CMD ["venv/bin/python", "-m", "server.main"]
