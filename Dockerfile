FROM python:3.13-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt \
    && apt-get update \
    && apt-get install curl -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64 \
    && chmod +x tailwindcss-linux-x64 \
    && mv tailwindcss-linux-x64 tailwindcss \
    && ./tailwindcss -i ./static/input.css -o ./static/output.css --content "./templates/*.html" --minify \
    && rm tailwindcss
EXPOSE 5000
CMD ["python", "app.py"]