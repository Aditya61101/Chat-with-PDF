# Chat with Your PDF

## Overview
"Chat with Your PDF" is an interactive web application built using Streamlit that allows users to upload a PDF document and engage with its content by asking questions. The application utilizes advanced text processing techniques to extract information and provide accurate responses to user queries.

## Features
- Upload PDF documents for processing.
- Extracts text from PDFs and converts it into a knowledge base.
- Allows users to ask questions related to the content of the uploaded PDF.
- Displays conversation history in a user-friendly interface.

## Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python, Langchain, PyPDF2
- **Data Processing**: OpenAI Embeddings, FAISS
- **Environment Management**: dotenv

## Installation

### Prerequisites
- Python 3.9 or higher
- An OpenAI API key

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Aditya61101/Chat-with-PDF.git
   cd Chat-with-PDF
   ```
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
    ```
4. **Set up environment variables**:
    - Create a new file named `.env` in the root directory.
    - Add the following environment variables to the file:
      ```env
      OPENAI_API_KEY=your-api-key
      ```
5. **Run the application**:
    ```bash
    streamlit run app.py
    ```
