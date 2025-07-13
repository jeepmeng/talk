FROM docker.elastic.co/elasticsearch/elasticsearch:8.13.2

COPY elasticsearch-analysis-ik-8.13.2.zip /tmp/

RUN elasticsearch-plugin install --batch file:///tmp/elasticsearch-analysis-ik-8.13.2.zip
