FROM python:3.10


RUN mkdir -p /app/resources && \
    mkdir -p /app && \
    mkdir __logger
WORKDIR .
COPY . /app
ADD ./resources/*.pdf /app/resources

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install ghostscript
RUN apt-get update && apt-get -y install ghostscript && apt-get clean

# set display port to avoid crash
ENV DISPLAY=:99
ENV INPUT_FILE_LOCATION=/app/resources
ENV HEADLESS_FLAG=True
ENV QPAY_PORTAL_LOGIN_ID=10002147
ENV QPAY_PORTAL_PWD=Quess@123
ENV URL=https://piqpayrollsim.quesscorp.com/
ENV ELEMENT_WAIT=45
ENV BROWSER_WAIT=60
ENV NOTIFICATION_EMAIL=sibbal@quesscorp.com

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

CMD ["python", "/app/ibm_invoicing_rpa.py"]