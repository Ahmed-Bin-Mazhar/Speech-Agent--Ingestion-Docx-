RAG + TTS AI Project
Overview
A voice-enabled AI assistant that combines Retrieval-Augmented Generation (RAG) with Text-to-Speech capabilities. The system processes documents, stores them in a vector database, and provides intelligent responses through voice interaction.

Architecture
User Voice Input → Speech-to-Text → RAG Query → LLM Processing → Text-to-Speech → Audio Response

Components
RAG_API.py - FastAPI server for document ingestion and chatbot functionality
tts_llm.py - Client application for voice recording, transcription, and audio response
Prerequisites
Python Version
Python 3.13 or higher
Required Accounts & API Keys
Pinecone - Vector database
HuggingFace - Embeddings and models
Groq - LLM inference
ElevenLabs - Speech-to-Text and Text-to-Speech
Installation
1. Clone the Repository
git clone <your-repository-url>
cd rag-tts-project



## Create Virtual Environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


### Install Dependencies
bash
pip install fastapi uvicorn pinecone-client langchain langchain-groq langchain-community werkzeug elevenlabs pygame sounddevice numpy requests python-dotenv

Environment Setup
Create a .env file in the project root:

bash
# RAG_API.py required keys
HUGGINGFACEHUB_API_TOKEN="your_huggingface_token"
PINECONE_API_KEY="your_pinecone_api_key"
PINECONE_ENV="your_pinecone_environment"
INDEX_NAME="genai"  # or your preferred index name
GROQ_API_KEY="your_groq_api_key"

# tts_llm.py required keys
ELEVENLABS_API_KEY="your_elevenlabs_api_key"
Setup Instructions
Pinecone Setup
Create a Pinecone account at pinecone.io

Create a new project and index

Note your API key and environment

Update the .env file with your credentials

Groq Setup
Sign up at groq.com

Generate an API key from the dashboard

Add to your .env file

ElevenLabs Setup
Create an account at elevenlabs.io

Generate an API key

Add to your .env file

HuggingFace Setup
Create an account at huggingface.co

Generate an access token from settings

Add to your .env file

Running the Application
Step 1: Start the FastAPI Server
bash
uvicorn RAG_API:app --reload --host 0.0.0.0 --port 8000
The server will start at http://127.0.0.1:8000

Step 2: Test the Server
Open your browser or use curl to test:

bash
curl http://127.0.0.1:8000/test
Expected response: "Deployment Response"

Step 3: Ingest Documents
Use a tool like Postman or curl to upload documents:

bash
curl -X POST "http://127.0.0.1:8000/ingestion-pipeline" \
  -F "file=@your_document.pdf" \
  -F "file=@another_document.docx"
Supported formats: PDF, DOCX

Step 4: Run the Voice Client
bash
python tts_llm.py
Usage
Voice Interaction
The client will record 5 seconds of audio

Speak your question clearly

The system will:

Transcribe your speech to text

Query the RAG system

Generate a response using Groq LLM

Convert the response to speech using ElevenLabs

The response will be played through your speakers

The process repeats until you say "exit"

API Endpoints
GET /test
Purpose: Test server connectivity

Response: "Deployment Response"

POST /ingestion-pipeline
Purpose: Upload and process documents

Parameters: file (multipart form-data)

Supported formats: PDF, DOCX

POST /chatbot
Purpose: Query the RAG system

Parameters: query (form-data)

Response: JSON with AI response

Configuration
Modifying Pinecone Index
Edit in RAG_API.py:

python
INDEX_NAME = "your-custom-index-name"
Changing TTS Voice
Edit in tts_llm.py:

python
voice_id = "your-preferred-voice-id"  # ElevenLabs voice ID
Adjusting Recording Duration
Edit in tts_llm.py:

python
duration = 10  # Change from 5 to 10 seconds
Troubleshooting
Common Issues
API Key Errors

Verify all API keys in .env file

Ensure keys have sufficient permissions

Pinecone Connection Issues

Check Pinecone environment and index name

Verify index exists in your Pinecone project

Audio Recording Problems

Check microphone permissions

Verify sounddevice installation

Document Processing Failures

Ensure documents are not password protected

Check document format compatibility

Debug Mode
Enable debug logging by setting:

python
# In both files, add:
import logging
logging.basicConfig(level=logging.DEBUG)
File Structure
text
project/
├── RAG_API.py          # FastAPI server
├── tts_llm.py          # Voice client
├── .env               # Environment variables
├── requirements.txt   # Dependencies
└── README.md         # This file
Dependencies Details
fastapi/uvicorn: Web server framework

pinecone-client: Vector database client

langchain: LLM framework

elevenlabs: Speech-to-Text and TTS

sounddevice/pygame: Audio recording and playback

python-dotenv: Environment variable management

Support
For issues and questions:

Check the troubleshooting section

Verify API keys and permissions

Ensure all dependencies are installed

Check Python version compatibility

License
[Add your license information here]

Contributing
[Add contribution guidelines here]

text

This comprehensive README.md includes:
- Clear setup instructions for each service
- Step-by-step running guide
- Configuration options
- Troubleshooting section
- API endpoint documentation
- File structure overview

The markdown format is optimized for GitHub readability with proper code blocks, headers, and organization.
New chat
