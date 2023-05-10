FROM python:3
RUN apt update
RUN apt install unixodbc-dev -y
ENV VIRTUOSO_DRIVER /opt/virtuoso-opensource/lib/virtodbc_r.so
COPY --from=openlink/virtuoso-opensource-7:latest ${VIRTUOSO_DRIVER} ${VIRTUOSO_DRIVER}
WORKDIR /ndbi040
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .
CMD [ "/bin/bash" ]