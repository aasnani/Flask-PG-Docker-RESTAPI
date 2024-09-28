FROM python:3.12
WORKDIR /app
# Build arguments from compose
ARG FLASK_APP
ARG FLASK_RUN_PORT
ARG FLASK_RUN_HOST
# Setting environment variables from build args for flask
ENV FLASK_APP=$FLASK_APP
ENV FLASK_RUN_PORT=${FLASK_RUN_PORT}
ENV FLASK_RUN_HOST=${FLASK_RUN_HOST}
COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt
# Staring backend
CMD ["flask", "run"]