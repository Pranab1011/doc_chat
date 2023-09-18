FROM python

# Update the package manager and install pip
RUN apt-get update && apt-get install -y python3-pip

# Optionally, upgrade pip to the latest version
RUN python3 -m pip install --upgrade pip

WORKDIR /app

COPY src /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

ENV PYTHONPATH=.

EXPOSE 5000

CMD ["python", "doc_chat/chat_bot/app.py"]