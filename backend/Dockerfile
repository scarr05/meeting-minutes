# syntax=docker/dockerfile:1
FROM python:3.11-slim as base

# install build tools for whisper.cpp
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy backend sources
COPY backend/ ./backend/
WORKDIR /app/backend

# fetch whisper.cpp submodule and build whisper server
RUN git submodule update --init --recursive \
    && cd whisper.cpp \
    && cp -r ../whisper-custom/server/* examples/server/ \
    && mkdir build && cd build \
    && cmake .. -DCMAKE_C_FLAGS="-w" -DCMAKE_CXX_FLAGS="-w" \
    && make -j$(nproc) \
    && mkdir -p ../whisper-server-package \
    && cp build/bin/whisper-server ../whisper-server-package/

# download a default model (small) into package directory
RUN mkdir -p whisper-server-package/models \
    && bash ./download-ggml-model.sh small whisper-server-package/models

# install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5167 8178
CMD ["/entrypoint.sh"]
