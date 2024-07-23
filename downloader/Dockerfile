# downloader/Dockerfile
FROM alpine:latest

RUN apk update && apk add --no-cache bash wget openssl

# Create the target directory
RUN mkdir -p /downloader

# Copy the script into the image
COPY download_files.sh /downloader/download_files.sh

# Ensure the script has execute permissions
RUN chmod +x /downloader/download_files.sh

# Set the entrypoint to the script
ENTRYPOINT ["bash", "/downloader/download_files.sh"]
