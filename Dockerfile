FROM python:3.8.2-slim-buster
COPY . /app/
WORKDIR /app/src
pip install -r doc_chat/requirements.txt
CMD ["python", "doc_chat/chat_bot/app.py"]