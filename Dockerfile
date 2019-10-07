# Use python 3
FROM python:3

# Copy source code
COPY . /shop40

# Change working directory to app
WORKDIR /shop40

# Install dependencies
RUN pip install -r requirements.txt

RUN pip install -r dev-requirements.txt

