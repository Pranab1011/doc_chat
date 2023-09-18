# Retriever Augmented Generation Chat Application

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Retriever Augmented Generation Chat Application is a powerful tool that allows users to have dynamic and contextually rich conversations with a text document. Built with Flask, Langchain, OpenAI, and Docker, this application leverages state-of-the-art natural language processing techniques to provide an interactive and informative experience.

![Application Screenshot](/path/to/screenshot.png)

## Features

- **Chat with Text Documents**: Engage in chat conversations with text documents.
- **Retrieval and Generation**: Combine retrieval-based and generation-based methods for intelligent responses.
- **Easy Deployment**: Dockerized for easy deployment to production environments with scaling support.
- **Vector Store**: Utilizes Chroma DB as a vector store for efficient data retrieval.
- **Customizable**: Configure and adapt the application to suit your specific use cases.

## Demo

[Insert link to a live demo of the application, if available.]

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Docker](https://www.docker.com/) installed on your machine.
- An API key from OpenAI for the GPT-3 model.
- [Chroma DB](https://chromadb.org/) configured and running.

## Getting Started

To get started with this application, follow these steps:

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. Install the necessary dependencies:

    ```shell
   pip install -r requirements.txt

3. Configure your API keys and settings. Refer to the Configuration section below.
4. Start the application locally:

    ```shell
   ls src
   python doc_chat/chat_bot/app.py
   
5. Open your web browser and navigate to http://localhost:5000 to access the application.

## Configuration

To configure the application, follow these steps:

Create a .env file in the project root directory if it doesn't already exist.

Add the following environment variables to the .env file:

OPENAI_API_KEY: Your API key for OpenAI's GPT-3 model.
CHROMA_DB_URL: The URL for your Chroma DB instance.
[Add any other configuration variables as needed.]
Save the .env file.

## Deployment

Deploying the application to a production environment with proper scaling can be achieved using Docker. Follow these steps:

1. Build the Docker image using the following command:
    ```shell
   docker-compose build
   
2. Run the Docker container with the following command:
    ```shell
   docker-compose up
   
3. Access the deployed application by navigating to the appropriate URL in your web browser.