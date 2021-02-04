FROM python:3.7 as base
WORKDIR /app
RUN pip3 install gunicorn

COPY requirements.txt /app/requirements.txt
COPY requirements-internal.txt /app/requirements-internal.txt
RUN pip3 install -r requirements.txt
# RUN pip3 install -i http://127.0.0.1:3141/testuser/dev -r requirements-internal.txt

COPY . /app

# LDAP install
RUN apt-get update
RUN apt-get install -y build-essential python3-dev libldap2-dev libsasl2-dev ldap-utils tox lcov valgrind
RUN pip3 install python-ldap

CMD [ "python3", "metadata_service/metadata_wsgi.py" ]

FROM base as oidc-release

RUN pip3 install .[oidc]
RUN python3 setup.py install
ENV FLASK_APP_MODULE_NAME flaskoidc
ENV FLASK_APP_CLASS_NAME FlaskOIDC
ENV FLASK_OIDC_WHITELISTED_ENDPOINTS status,healthcheck,health
ENV SQLALCHEMY_DATABASE_URI sqlite:///sessions.db

# You will need to set these environment variables in order to use the oidc image
# FLASK_OIDC_CLIENT_SECRETS - a path to a client_secrets.json file
# FLASK_OIDC_SECRET_KEY - A secret key from your oidc provider
# You will also need to mount a volume for the clients_secrets.json file.

FROM base as release
RUN python3 setup.py install
