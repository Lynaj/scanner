# pull official base image
FROM juusechec/firefox-headless-selenium-python

# set work directory
WORKDIR /app/scanner
COPY . .

# install dependencies
RUN apt update; \
    apt install python3-pip; \
    pip3 install -r requirements.txt; \
    ls -l -a -h

CMD [ "python3", "./main.py" ]