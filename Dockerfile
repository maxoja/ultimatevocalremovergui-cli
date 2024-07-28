# Use a base image
FROM ubuntu:20.04

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    python3.10.14-tk \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/maxoja/ultimatevocalremovergui-cli.git .

# Make the script executable
RUN chmod +x /app/install.sh

# Run the script
CMD ["./install.sh"]
CMD ["python3 test_run.py"]
