# Use base shared Python image
FROM python:3.11

ENV PYTHONUNBUFFERED=1


# Relevant folder
ARG FOLDER=/travel_adviser

# Create a folder
RUN mkdir -p $FOLDER

# Install packages
COPY ./requirements.txt $FOLDER/requirements.txt
RUN pip install -r $FOLDER/requirements.txt

# Copy the project files into the container
COPY ./src $FOLDER/src

# Expose any necessary ports
EXPOSE 8000

# Set the working directory
WORKDIR $FOLDER/src

# Start the application
CMD ["uvicorn", "--host", "127.0.0.1", "--port", "8000", "--reload", "--reload-dir", "/travel_adviser", "main:app"]