FROM alpine:3.4
RUN apk update && apk upgrade
RUN apk add --no-cache python py-pip git
RUN pip install git+https://github.com/googlei18n/cu2qu.git
RUN pip install fonttools
RUN pip install robofab
RUN mkdir /opt
ADD otf2ttf.py /opt
