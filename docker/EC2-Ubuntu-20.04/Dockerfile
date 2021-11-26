FROM python:3.8


RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get -y update \
    && apt-get install -y google-chrome-stable

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
    && apt-get install -yqq unzip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

COPY ["requirements.txt", "pinterestScraper.py", "./"]

ENV DISPLAY=:99

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "pinterestScraper.py"]

# CMD [ "22", "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22",  "Y", "A", "Y", "<your-bucket-name>", "Y", "A", "Y", "4", "Y", "Y"]
CMD [ "1", "3",  "N", "1", "N", "s3-and-boto3", "N", "A", "N", "4", "N", "N", "postgres", "****", "localhost", "5432", "Pagila", "djalkjfia"]