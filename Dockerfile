 FROM python:3.9-alpine3.13

LABEL maintainer="Book Scope"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY . /app
COPY .env /app/.env

WORKDIR /app

EXPOSE 8000

# devだけ使うパッケージをインストールする用のフラグ
ARG DEV=false

    # venv作成
RUN python -m venv /py && \
    # pipのインストール
    /py/bin/pip install --upgrade pip && \
    # postgreSQL用の追加のパッケージ（apkはAlpine Linuxのpakage manager）
    apk add --update --no-cache postgresql-client jpeg-dev zbar zbar-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps zlib zlib-dev \
        build-base postgresql-dev musl-dev linux-headers && \
    # pythonのパッケージをインストール
    /py/bin/pip install -r /tmp/requirements.txt && \
    # dev用のパッケージをインストール
    if [ $DEV = "true" ]; then \
    apk add --update --no-cache graphviz graphviz-dev pkgconfig && \
    /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # 後処理（もう使わないものを削除）
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    # ユーザを作成
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER django-user