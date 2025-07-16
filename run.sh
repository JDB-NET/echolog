#!/bin/bash

echo "Generating CSS..."
./tailwindcss -i ./static/input.css -o ./static/output.css --content "./templates/*.html" --minify

echo "Starting app..."
gunicorn --workers 2 --bind 0.0.0.0:5000 app:app --log-level warning