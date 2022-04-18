FROM python:3.8-alpine
WORKDIR /app
COPY . /app/
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r requirements.txt
RUN python setup.py install
COPY . /app/
CMD python fmapi/app.py
