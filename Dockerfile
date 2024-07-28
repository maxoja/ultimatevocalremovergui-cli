# Use a base image
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

# Clone the repository
RUN git clone --depth=1 https://github.com/maxoja/ultimatevocalremovergui-cli.git .

# Copy screen config from repo to config dir
RUN cp ./xorg.conf /usr/share/X11/xorg.conf.d/xorg.conf

# Make the script executable
RUN export SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True && python3.10 -m pip install -r requirements.txt
RUN mkdir testing-src/output # TODO: automatically create dir instead

# Run the script
CMD (/usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config /etc/X11/xorg.conf :1 > /dev/null 2>&1 &) \
    && export DISPLAY=:1 && python3.10 test_run.py \
    ; tail -f /dev/null
