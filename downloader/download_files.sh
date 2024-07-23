#!/bin/bash

echo "Starting download_files.sh script..."

# Create the target directory if it doesn't exist
mkdir -p ./.cache

# Define the files and their URLs
declare -A files
files["Meta-Llama-3-8B-Instruct.Q4_0.gguf"]="https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct.Q4_0.gguf"
files["nomic-embed-text-v1.5.f16.gguf"]="https://huggingface.co/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.f16.gguf"

# Loop through the files and download them if they don't exist
for file in "${!files[@]}"; do
  if [ -f "./.cache/$file" ]; then
    echo "$file already exists, skipping download."
  else
    echo "Downloading $file..."
    wget -O "./.cache/$file" "${files[$file]}"
  fi
done

echo "Finished download_files.sh script..."

exit 0
