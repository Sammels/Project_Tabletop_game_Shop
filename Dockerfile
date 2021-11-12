FROM python:3.9-slim

# update image
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*



# copy all the files to the container
COPY ./requirements.txt /

# install dependencies
RUN pip install  -r /requirements.txt

# Copy directory
COPY . /app
WORKDIR app/
RUN chmod +x /app/entrypoint.sh

RUN groupadd --gid=800 -r vasya && useradd --uid=800 --gid=800 --no-log-init -r vasya

RUN chown -R vasya:vasya /app
USER vasya

# tell the port number the container should expose
#EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]




# run the command
CMD ["run"]
