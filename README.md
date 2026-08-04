# 🚛 TruckSaathi

AI-powered logistics booking from Hindi/Hinglish voice notes.

## Features

- 🎤 Speech-to-Text (Sarvam AI)
- 🧠 Structured booking extraction using LLMs
- 📊 Confidence scoring
- ✅ Validation
- ❓ Intelligent follow-up questions
- 🔊 Optional voice confirmation

## Architecture

```text
Voice Note
    ↓
Speech-to-Text
    ↓
Transcript
    ↓
LLM Extraction
    ↓
Structured JSON
    ↓
Validation
    ↓
Follow-up Question
```

## Run

```bash
pip install -r requirements.txt

python main.py
```