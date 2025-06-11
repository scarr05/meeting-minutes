#!/bin/bash
set -e

WHISPER_DIR="whisper-server-package"
WHISPER_MODEL="models/ggml-small.bin"

# start whisper server
./$WHISPER_DIR/whisper-server --model $WHISPER_DIR/$WHISPER_MODEL --host 0.0.0.0 --port 8178 --diarize --print-progress &
WHISPER_PID=$!

# start fastapi backend
PORT=${PORT:-5167}
uvicorn app.main:app --host 0.0.0.0 --port $PORT &
BACKEND_PID=$!

# wait for either process to exit
wait -n $WHISPER_PID $BACKEND_PID


