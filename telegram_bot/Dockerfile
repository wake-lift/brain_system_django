# для запуска на ядрах linux x86_64
FROM python:3.12-slim-bookworm

# для запуска на ядрах linux ARM64/v8
# FROM arm64v8/python:3.12-slim-bookworm 

WORKDIR /app

COPY . .

RUN pip install -r requirements_bot.txt --no-cache-dir

RUN chmod +x brain_bot.py

CMD python3 ./brain_bot.py;
