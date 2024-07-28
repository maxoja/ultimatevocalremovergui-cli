FROM ubuntu:20.04

# Install necessary dependencies
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y git curl
RUN apt-get install -y python3.10
RUN apt-get install -y python3.10-tk
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN apt-get install -y ffmpeg
RUN apt-get install -y python3.10-dev
RUN apt-get install -y gcc
RUN apt-get install -y xserver-xorg-video-dummy
RUN apt-get install -y libglu1-mesa
RUN rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy everything from local repo to the image.
COPY . /app
# Copy dummy display config
RUN cp ./xorg.conf /usr/share/X11/xorg.conf.d/xorg.conf
RUN mkdir /app/testing-src/output; rm /app/testing-src/output/*
# TODO: automatically create dir instead
# TODO: remove huge unused files

# Install python packages and download model
RUN export SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True && python3.10 -m pip install -r requirements.txt
RUN python3.10 download_models.py

# Make the run script executable
COPY ./run.sh ./run.sh
RUN chmod +x ./run.sh

CMD ./run.sh
