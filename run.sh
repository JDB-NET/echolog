#!/bin/bash

echo "Generating CSS..."
./tailwindcss -i ./static/input.css -o ./static/output.css --content "./templates/*.html" --minify

echo "Starting app..."
python3 app.py