FROM python:3.9-slim

LABEL maintainer=“maazkarim02@gmail.com”

ARG POETRY_VERSION="1.5.1"

ENV POETRY_VERSION=${POETRY_VERSION}
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /cdc_chatbot

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN pip --no-cache-dir install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root
RUN rm -rf ~/.cache/pypoetry/{cache,artifacts}

EXPOSE 8501

COPY . .

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]