# 🚚 TruckSaathi

> An end-to-end AI voice logistics assistant that enables truck booking through natural voice conversations on Telegram, powered by a real-time observability dashboard.

TruckSaathi allows users to book trucks simply by sending a voice message. The system automatically downloads the audio, converts it into text, extracts structured booking information using an LLM, validates the booking, generates follow-up questions when information is missing, synthesizes a spoken response, and sends it back to the user—all while streaming live pipeline events to an observability dashboard.

---

# Demo

> *(Add GIF here)*

```
Telegram Voice
      │
      ▼
AI Processing Pipeline
      │
      ▼
Real-Time Dashboard
      │
      ▼
Telegram Voice Reply
```

---

# Features

- 🎤 Voice-first truck booking through Telegram
- 🧠 Multi-turn conversational booking
- 📝 LLM-powered structured information extraction
- 🔄 Incremental booking merge engine
- ✅ Booking validation
- 🔊 Text-to-Speech voice replies
- ⚡ Live WebSocket event streaming
- 📊 Real-time observability dashboard
- 📈 Stage-level latency tracking
- 💾 Persistent dashboard event storage with SQLite

---

# System Architecture

> *(Replace with Excalidraw diagram)*

```
                Telegram Voice Message
                         │
                         ▼
                 Voice Handler (Bot)
                         │
                Download Voice Note
                         │
                         ▼
                  FFmpeg (OGG → WAV)
                         │
                         ▼
              Conversation Manager
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
   Session Store    Dashboard Events   Booking Store
                         │
                         ▼
                 Speech-to-Text
                         │
                         ▼
                    Transcript
                         │
                         ▼
               Information Extraction
                         │
                         ▼
                  Merge Engine
                         │
                         ▼
                    Validation
                  ┌────────────┐
                  │            │
                  ▼            ▼
            Booking Done   Follow-up
                  │            │
                  └──────┬─────┘
                         ▼
                        TTS
                         │
                         ▼
                 Telegram Voice Reply
```

---

# Observability Architecture

Every stage of the AI pipeline emits events that are persisted and streamed to the dashboard in real time.

```
Pipeline Stage
      │
      ▼
Dashboard Event
      │
      ▼
SQLite Event Store
      │
      ▼
FastAPI WebSocket
      │
      ▼
React Dashboard

        ┌──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼
     Pipeline       Logs        Conversation
        │
        ▼
 Booking State   Performance Metrics
```

---

# AI Pipeline

Every user request passes through the following stages.

| Stage | Description |
|--------|-------------|
| Telegram | Receives voice message |
| FFmpeg | Converts Telegram Opus audio into WAV |
| STT | Transcribes speech into text |
| Extraction | Extracts structured booking fields using an LLM |
| Merge | Merges newly extracted fields with existing conversation state |
| Validation | Determines whether all required booking information has been collected |
| Follow-up | Generates the next conversational question if required |
| TTS | Synthesizes spoken response |
| Telegram Reply | Sends generated audio back to the user |

---

# Dashboard

TruckSaathi includes a live observability dashboard inspired by production monitoring systems.

### Live Pipeline

Visualizes every stage of request execution.

### Live Logs

Streams structured logs in real time.

### Booking State

Displays the progressively completed booking information.

### Conversation Timeline

Shows both user transcripts and assistant responses.

### Performance Metrics

Measures latency for every stage of the pipeline.

---

# Tech Stack

## Backend

- Python
- FastAPI
- SQLite
- python-telegram-bot
- FFmpeg
- WebSockets

## Frontend

- React
- TypeScript
- Tailwind CSS
- Vite

## AI

- Speech-to-Text
- LLM-based Information Extraction
- Text-to-Speech

---

# Repository Structure

```
trucksaathi/

├── api/
├── booking/
├── conversation/
├── dashboard/
├── frontend/
├── schemas/
├── telegram_bot/
├── tests/
└── README.md
```

---

# Running Locally

## Backend

```bash
git clone <repo>

cd trucksaathi

uv sync

uvicorn api.app:app --reload
```

Start the Telegram bot

```bash
python -m telegram_bot.main
```

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Screenshots

### Dashboard

*(Add screenshot)*

### Pipeline

*(Add screenshot)*

### Booking State

*(Add screenshot)*

### Live Logs

*(Add screenshot)*

### Performance

*(Add screenshot)*

---

# Future Improvements

- Redis Pub/Sub for distributed event streaming
- Historical request replay
- OpenTelemetry integration
- Docker deployment
- Kubernetes support
- Multi-user dashboard
- Analytics and request history

---

# Why TruckSaathi?

Most conversational AI projects stop after generating a response.

TruckSaathi focuses on **operational visibility** by treating every stage of the AI pipeline as an observable event. This makes latency bottlenecks, failures, and conversation state easy to inspect in real time, providing a production-style monitoring experience for AI workflows.

---

# License

MIT License