# Everything for the Shadow Hunter project lives here - nothing is installed on the owner's PC
FROM mcr.microsoft.com/devcontainers/python:3.11
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg fonts-noto-core fonts-noto-ui-core fonts-dejavu-core \
    libraqm0 libfribidi0 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir opencv-python-headless numpy pandas pillow moviepy cryptography requests edge-tts \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir diffusers transformers accelerate peft safetensors
