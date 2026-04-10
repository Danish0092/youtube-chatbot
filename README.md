# 🎥 AI YouTube Video Chatbot (RAG + LangChain)

An AI-powered YouTube chatbot that allows users to:

- 🎥 load a YouTube video using link
- 📜 read the full transcript
- 💬 ask grounded questions
- ⏱ jump to exact timestamps
- ⚡ experience ChatGPT-style streaming UI
- 📱 use a fully responsive SaaS-style interface

Built with **Flask, LangChain, FAISS, OpenAI, Tailwind CSS, and JavaScript**.

---

## 🚀 Live Frontend Demo

🔗 Add your Vercel frontend link here

---

## ✨ Features

- 🎥 Embedded playable YouTube video
- 📜 Full transcript panel with scrollbar
- 💬 Transcript-grounded Q&A chatbot
- 🧠 LangChain + FAISS retrieval
- ⏱ Clickable timestamps → seek video
- ⚡ Frontend streaming answer effect
- 📱 Fully responsive mobile UI
- 🎨 Tailwind premium SaaS design

---

## 🛠 Tech Stack

### Frontend

- HTML
- Tailwind CSS
- Vanilla JavaScript

### Backend

- Flask
- LangChain
- OpenAI
- FAISS
- youtube-transcript-api
- yt-dlp

---

## 🧠 How It Works

1. User pastes a YouTube URL
2. Transcript is fetched
3. Transcript is split into chunks
4. OpenAI embeddings are created
5. FAISS stores vectors
6. Relevant chunks are retrieved
7. GPT generates grounded answers
8. Frontend renders streamed response + timestamps

---

## 📂 Project Structure

```text
youtube-chatbot/
│
├── backend/
│   └── app.py
│
├── frontend/
│   └── index.html
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Local Setup

Clone repo:

```bash
git clone https://github.com/yourusername/youtube-chatbot.git
cd youtube-chatbot
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate venv:

### Windows

```bash
.venv\\Scripts\\activate
```

### Mac/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Add `.env` file:

```env
OPENAI_API_KEY=your_key_here
```

Run Flask app:

```bash
python backend/app.py
```

Open:

```text
http://127.0.0.1:5000
```

---


## 🔮 Future Improvements

- 🔴 real backend token streaming
- 📚 multi-video comparison mode
- 🌙 dark mode
- 📝 export notes as PDF
- 👥 multi-user sessions
- 🎯 exact chunk-level timestamp grounding

---

## 👨‍💻 Author

Built by **Danish Saleem**
