# Project Setup and Execution Guide

This guide will walk you through setting up the project environment and running the application.

## Prerequisites

Before you begin, ensure you have the following installed:

  * **Python:** Version 3.10 or higher.
  * **Ollama:** The Ollama server must be running. For installation, refer to the [Ollama GitHub repository](https://github.com/ollama/ollama).
  * **Ollama Model:** The `gemma3:4b` model must be pulled. Run the following command:
    ```bash
    ollama pull gemma3:4b
    ```

## Step 1: Environment Setup

1.  **Create Conda Environment:**

    ```bash
    conda create --name langraph-workflow python=3.10
    conda activate langraph-workflow
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Step 2: Run the Application

With the environment configured, you can launch the LangGraph agents using the main application script:

```bash
python app/graph.py
```
