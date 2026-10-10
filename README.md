# StudySprint AI

**Learn something today. Take your next step tomorrow.**

StudySprint AI is an AI-powered learning companion that helps students understand concepts, practise through quizzes, review mistakes, and decide what to study next.

## Features

* AI-generated topic explanations
* Multiple-choice quizzes tailored to a selected subject, topic, and difficulty
* Automatic scoring and percentage calculation
* Correct answers and explanations after submission
* Learning recommendations based on quiz performance
* Validation checks for generated quiz structure and duplicate questions

## Technology Stack

* Python
* Streamlit
* OpenAI Python SDK
* Amazon Bedrock Mantle API
* Environment variables for API credentials

## Setup

1. Clone this repository.

2. Create and activate a Python virtual environment.

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables using a local `.env` file. See `.env.example` for the required variable names.

5. Start the application:

   ```bash
   streamlit run app.py
   ```

## Configuration

Set the following variables in your local `.env` file:

* `OPENAI_API_KEY` — your Bedrock Mantle API key
* `OPENAI_BASE_URL` — your Bedrock Mantle endpoint
* `BEDROCK_MODEL_ID` — the model ID
* `AWS_REGION` — the AWS region

Never commit real API keys, passwords, or secret configuration files to GitHub.

## Project Status

This is a learning-focused prototype. AI-generated explanations and questions should be reviewed for accuracy.

## Author

Ayaz Ahmad

GitHub: https://github.com/Ayazahmad01
