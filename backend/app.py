from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
import re
import os

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

app = Flask(
    __name__,
    template_folder="../frontend"
)
CORS(app)

# safer than global variable
app.config["RETRIEVER"] = None


# -----------------------------
# Extract YouTube video ID
# -----------------------------
def extract_video_id(url):
    patterns = [
        r"(?:v=)([0-9A-Za-z_-]{11})",
        r"(?:youtu\.be/)([0-9A-Za-z_-]{11})",
        r"(?:embed/)([0-9A-Za-z_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Process YouTube Video
# -----------------------------
def format_duration(seconds):
    if not seconds:
        return "Unknown duration"

    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"


@app.route("/process", methods=["POST"])
def process_video():
    try:
        data = request.json
        url = data.get("url")

        if not url:
            return jsonify({"error": "YouTube URL is required"}), 400

        video_id = extract_video_id(url)

        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        # =============================
        # Transcript (UNCHANGED)
        # =============================
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id)

        transcript = " ".join(item.text for item in transcript_list)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = splitter.create_documents([transcript])

        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        vector_store = FAISS.from_documents(chunks, embeddings)

        app.config["RETRIEVER"] = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 2}
        )

        # =============================
        # Metadata (NEW)
        # =============================
        clean_url = f"https://www.youtube.com/watch?v={video_id}"

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(clean_url, download=False)

        title = (
            info.get("title")
            or info.get("fulltitle")
            or "Loaded YouTube Video"
        )

        channel = (
            info.get("uploader")
            or info.get("channel")
            or info.get("creator")
            or "Unknown Channel"
        )

        raw_duration = info.get("duration", 0)
        duration = format_duration(raw_duration)

        thumbnail = (
            info.get("thumbnail")
            or f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        )

        # =============================
        # FINAL RESPONSE
        # =============================
        return jsonify({
            "message": " Transcript loaded",
            "title": title,
            "channel": channel,
            "duration": duration,
            "thumbnail": thumbnail,
            "transcript": transcript
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Ask Question
# -----------------------------
@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        retriever = app.config.get("RETRIEVER")

        if retriever is None:
            return jsonify({"error": "Load a video first"}), 400

        data = request.json
        question = data.get("question")

        if not question:
            return jsonify({"error": "Question is required"}), 400

        llm = ChatOpenAI(
           model="gpt-4.1",
            temperature=0.2
        )

        prompt = PromptTemplate(
template = """
You are a helpful YouTube video assistant.

Answer ONLY from transcript context.

Whenever possible, include timestamps in mm:ss format
based on transcript moments.

Example:
The creator explains monetization at 4:32.

Context:
{context}

Question:
{question}
""",
            input_variables=["context", "question"]
        )

        retrieved_docs = retriever.invoke(question)

        def format_docs(retrieved_docs):
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
            return context_text
        
        parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
})
        parser = StrOutputParser()
        main_chain = parallel_chain | prompt | llm | parser
        answer = main_chain.invoke(question)

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)