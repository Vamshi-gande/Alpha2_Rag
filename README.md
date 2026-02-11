# Alpha2_Rag

A Retrieval-Augmented Generation (RAG) system that enables intelligent question-answering using vector databases and Google's Gemini AI.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

Alpha2_Rag is a complete RAG pipeline that:
1. Downloads and processes documents
2. Creates semantic chunks from the data
3. Builds a vector database for efficient retrieval
4. Enables natural language querying using Google Gemini AI

## ✨ Features

- **Document Processing**: Automated data downloading and preprocessing
- **Intelligent Chunking**: Semantic text chunking for better context retention
- **Vector Database**: Efficient similarity search using embeddings
- **AI-Powered Querying**: Natural language question-answering with Gemini
- **Modular Design**: Clean separation of concerns with dedicated scripts

## 📦 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Vamshi-gande/Alpha2_Rag.git
cd Alpha2_Rag
```

### Step 2: Set Up Python Virtual Environment

Using `pyenv` (Recommended):

**Install pyenv** (if not already installed):

For macOS/Linux:
```bash
curl https://pyenv.run | bash
```

For Windows, use [pyenv-win](https://github.com/pyenv-win/pyenv-win#installation).

**Install and set Python version:**
```bash
# Install Python 3.11 (or your preferred version)
pyenv install 3.11.0

# Set local Python version for this project
pyenv local 3.11.0
```

**Create virtual environment:**
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

Alternative using standard venv:
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🔑 Configuration

### Getting a Google Gemini API Key

1. **Visit Google AI Studio**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account

2. **Create API Key**:
   - Click on "Get API Key" or "Create API Key"
   - Click "Create API key in new project" or select an existing project
   - Copy the generated API key

3. **Important Notes**:
   - Keep your API key secure and never share it publicly
   - Free tier has rate limits (check [Gemini API pricing](https://ai.google.dev/pricing) for details)
   - The API key should start with `AIza...`

### Setting Up Environment Variables

1. **Create a `.env` file** in the project root directory:

```bash
# On macOS/Linux:
touch .env

# On Windows:
type nul > .env
```

2. **Add your API key** to the `.env` file:

Open the `.env` file in your preferred text editor and add:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual Gemini API key.

**Example `.env` file:**
```env
GEMINI_API_KEY=AIzaSyABC123def456GHI789jkl012MNO345pqr
```

3. **Verify `.env` is in `.gitignore**:

Make sure `.env` is listed in `.gitignore` to prevent accidentally committing your API key:

```bash
# Check if .env is in .gitignore
cat .gitignore | grep .env
```

If not present, add it:
```bash
echo ".env" >> .gitignore
```

## 💻 Usage

### Step 1: Download Data

Download and prepare the initial dataset:

```bash
python download_data.py
```

### Step 2: Create Chunks

Process the data into semantic chunks:

```bash
python create_chunks.py
```

### Step 3: Build Vector Database

Create the vector database for efficient retrieval:

```bash
python build_vectordb.py
```

### Step 4: Query the System

Ask questions using natural language:

```bash
python query_rag.py
```

Follow the prompts to enter your questions. The system will:
1. Retrieve relevant context from the vector database
2. Generate an answer using Gemini AI
3. Display the response

### Example Usage Flow

```bash
# Activate your virtual environment first
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the complete pipeline
python download_data.py
python create_chunks.py
python build_vectordb.py
python query_rag.py

# When prompted, enter questions like:
# "What is the main topic discussed in the documents?"
# "Can you summarize the key points?"
```

## 📁 Project Structure

```
Alpha2_Rag/
│
├── download_data.py         # Downloads and prepares initial data
├── create_chunks.py         # Creates semantic chunks from documents
├── build_vectordb.py        # Builds vector database for retrieval
├── query_rag.py            # Query interface for the RAG system
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── .env                   # Environment variables (create this)
└── README.md             # Project documentation
```

## 🔧 Troubleshooting

### Common Issues

**Issue 1: `ModuleNotFoundError`**
```
Solution: Make sure you've activated your virtual environment and installed all dependencies:
source venv/bin/activate
pip install -r requirements.txt
```

**Issue 2: API Key Error**
```
Solution: 
1. Verify your .env file exists in the project root
2. Check that GEMINI_API_KEY is correctly set
3. Ensure there are no extra spaces or quotes around the API key
4. Confirm your API key is valid at https://makersuite.google.com/app/apikey
```

**Issue 3: Permission Denied**
```
Solution: On macOS/Linux, you may need to make scripts executable:
chmod +x *.py
```

**Issue 4: Rate Limit Exceeded**
```
Solution: 
1. Wait a few minutes before retrying
2. Check your API quota at Google AI Studio
3. Consider upgrading your API plan if needed
```

### Getting Help

If you encounter issues:
1. Check that all prerequisites are installed
2. Verify your Python version: `python --version`
3. Ensure all dependencies are installed: `pip list`
4. Review the error messages carefully
5. Check the [Issues](https://github.com/Vamshi-gande/Alpha2_Rag/issues) page on GitHub

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Vamshi Gande**
- GitHub: [@Vamshi-gande](https://github.com/Vamshi-gande)

## 🙏 Acknowledgments

- Google Gemini AI for the language model
- The RAG research community for techniques and best practices
- All contributors who help improve this project

---

**Note**: Remember to never commit your `.env` file or share your API keys publicly. Keep your credentials secure!
