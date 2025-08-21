FROM python:3.13-alpine

RUN apk add git openssh

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
