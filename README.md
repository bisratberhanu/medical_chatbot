# Medical Chatbot

## Introduction

This is a medical chatbot that can answer questions about various medical topics. It uses the Gemini open model to generate responses based on user input.

The chatbot uses meTTa langauge to perform context fetching and pattern mining. It integrates AI with hypergraph-based data representation to provide accurate and context-aware responses.

If you are not familiar with MeTTa programming langauge check the [documentation](https://metta-lang.dev/)

## Features

- Answer questions about medical topics
- Can answer user-specific questions using a meTTa hypergraph
- An interactive UI for seamless user experience

## Technologies used

- AI : Gemini
- BackEnd : Django
- FrontEnd: HTML, CSS, Javascript 
- Context fetching: MeTTa

## How to Run

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd medical_chatbot
   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

## Important Files

- `views.py` - This file holds all the major logic functionalities of the backend.
- `data.metta` - This file holds the data in a meTTa data representation format and the functions that are used to mine complex relations from the data and give to the AI as a context.
- `utils.py` - Holds the integration between meTTa and Python.
