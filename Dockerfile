FROM python:alpine

# Upgrade pip
RUN python -m pip install --upgrade pip
WORKDIR /app
# copy the project into the docker container
COPY . .

# Install dependencies
RUN pip install poetry \
    && poetry install --only main

# Set permissions to scripts.sh
RUN chmod +x ./entrypoint.sh

# Define the entrypoint
ENTRYPOINT ["./entrypoint.sh"]
