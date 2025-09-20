import streamlit as st
import wikipedia
import requests
from io import BytesIO
from PIL import Image
import random
import pdfplumber
with pdfplumber.open(uploaded_file) as pdf:
    content = "\n".join([page.extract_text() for page in pdf.pages])
import docx
import speech_recognition as sr
import tempfile
import os

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Robo Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# CUSTOM CSS (Red, Black, Neutral Theme)
# ---------------------------
st.markdown("""
<style>
    body {
        font-family: "Segoe UI", Roboto, sans-serif;
        background-color: #121212;
        color: #f5f5f5;
    }
    .main-header {
        font-size: 3rem;
        color: #ff4d4d;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }
    .chat-container {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 20px;
        height: 600px;
        overflow-y: auto;
        border: 1px solid #333;
        font-size: 1rem;
        line-height: 1.5;
    }
    .user-message {
        background: linear-gradient(135deg, #ffcccc, #ff4d4d);
        padding: 12px 16px;
        border-radius: 12px;
        margin: 12px 0;
        text-align: right;
        font-size: 1rem;
        word-wrap: break-word;
        color: black;
        font-weight: bold;
    }
    .bot-message {
        background: linear-gradient(135deg, #2c2c2c, #444);
        padding: 12px 16px;
        border-radius: 12px;
        margin: 12px 0;
        text-align: left;
        font-size: 1rem;
        word-wrap: break-word;
        color: #f5f5f5;
    }
    .wikipedia-image {
        max-width: 100%;
        border-radius: 10px;
        margin-top: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .stButton button {
        width: 100%;
        background-color: #ff4d4d !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold;
        font-size: 1rem;
        padding: 8px;
        margin-top: 5px;
    }
    .stButton button:hover {
        background-color: #e60000 !important;
        transform: scale(1.02);
        transition: 0.2s;
    }
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background: #ff4d4d;
        border-radius: 4px;
    }
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #cc0000;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown('<h1 class="main-header">🤖 Robo Chatbot</h1>', unsafe_allow_html=True)
st.markdown("### Your assistant with Wikipedia knowledge, voice, and file understanding")

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4711/4711984.png", width=100)
    st.title("About Robo Chatbot")
    st.info("""
    I can:
    - Answer questions using Wikipedia
    - Read and analyze files
    - Understand uploaded images
    - Support voice input
    """)
    
    st.subheader("Settings")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.success("Conversation cleared!")
    
    st.subheader("Example Queries")
    example_queries = ["Tell me about artificial intelligence", 
                      "What is machine learning?", 
                      "Explain quantum computing"]
    for query in example_queries:
        if st.button(f"'{query}'"):
            st.session_state.user_input = query

# ---------------------------
# SESSION MEMORY
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def get_wikipedia_image(page_title):
    try:
        page = wikipedia.page(page_title, auto_suggest=False)
        for img_url in page.images[:5]:
            if any(ext in img_url for ext in ['.jpg', '.jpeg', '.png']):
                if not any(word in img_url for word in ['logo', 'icon', 'Wiki']):
                    response = requests.get(img_url)
                    img = Image.open(BytesIO(response.content))
                    return img, img_url
    except:
        pass
    return None, None

def read_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    return "❌ Unsupported file type."

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except:
            return "❌ Sorry, I couldn't understand the audio."

def chatbot_response(user_input, file_content=None):
    user_input_lower = user_input.lower()
    
    greeting_responses = [
        "Hello! I'm Robo Chatbot. How can I assist you today?",
        "Hi there! What would you like to know?",
        "Greetings! I'm here to help with your questions."
    ]
    
    if any(word in user_input_lower for word in ["hello", "hi", "hey", "greetings"]):
        return random.choice(greeting_responses), None, ["What is AI?", "Tell me about robots"]
    elif "your name" in user_input_lower:
        return "I'm Robo Chatbot, your friendly AI assistant!", None, ["Who created you?", "What can you do?"]
    elif any(word in user_input_lower for word in ["bye", "goodbye", "see you"]):
        return "Goodbye! Feel free to come back if you have more questions.", None, []
    elif "thank" in user_input_lower:
        return "You're welcome! Is there anything else you'd like to know?", None, ["Tell me a fact", "What is deep learning?"]
    elif file_content:
        return f"📄 I analyzed your file and here’s what I found:\n\n{file_content[:800]}...", None, ["Summarize this file", "What’s the main topic?"]
    else:
        try:
            summary = wikipedia.summary(user_input, sentences=5)
            img, img_url = get_wikipedia_image(user_input)
            suggestions = [f"History of {user_input}", f"Applications of {user_input}", f"Future of {user_input}"]
            return f"📖 According to Wikipedia:\n\n{summary}", img, suggestions
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:5]
            return f"⚠️ Too broad. Did you mean: {', '.join(options)}?", None, []
        except wikipedia.exceptions.PageError:
            return "❌ Sorry, I couldn't find anything on Wikipedia for that.", None, []
        except Exception as e:
            return f"⚠️ Error: {str(e)}", None, []

# ---------------------------
# LAYOUT
# ---------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Conversation")
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message"><b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message"><b>Robo:</b> {msg["content"]}</div>', unsafe_allow_html=True)
                if msg.get("image"):
                    st.image(msg["image"], caption="Related image", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Voice input
    if st.button("🎤 Speak"):
        spoken_text = recognize_voice()
        if spoken_text and "❌" not in spoken_text:
            st.session_state.messages.append({"role": "user", "content": spoken_text})
            response, image, suggestions = chatbot_response(spoken_text)
            bot_msg = {"role": "bot", "content": response}
            if image:
                bot_msg["image"] = image
            st.session_state.messages.append(bot_msg)
            st.session_state.suggestions = suggestions
            st.rerun()

    # User input
    user_input = st.chat_input("Type your message here...")

with col2:
    st.markdown("### 📂 Upload Files or Images")
    uploaded_file = st.file_uploader("Upload a file (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        content = read_file(uploaded_file)
        st.session_state.messages.append({"role": "user", "content": f"Uploaded {uploaded_file.name}"})
        response, image, suggestions = chatbot_response("file", file_content=content)
        st.session_state.messages.append({"role": "bot", "content": response})
        st.session_state.suggestions = suggestions
        st.rerun()

    if uploaded_image:
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        st.session_state.messages.append({"role": "user", "content": "I uploaded an image"})
        st.session_state.messages.append({"role": "bot", "content": "📷 Nice image! I can't fully analyze images yet but it's uploaded successfully."})
        st.rerun()
    
    # Tips + suggestions
    if "suggestions" in st.session_state and st.session_state.suggestions:
        st.subheader("🤔 Suggested Questions")
        for s in st.session_state.suggestions:
            if st.button(s):
                st.session_state.messages.append({"role": "user", "content": s})
                response, image, suggestions = chatbot_response(s)
                msg = {"role": "bot", "content": response}
                if image:
                    msg["image"] = image
                st.session_state.messages.append(msg)
                st.session_state.suggestions = suggestions
                st.rerun()

# ---------------------------
# PROCESS USER INPUT
# ---------------------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response, image, suggestions = chatbot_response(user_input)
    msg = {"role": "bot", "content": response}
    if image:
        msg["image"] = image
    st.session_state.messages.append(msg)
    st.session_state.suggestions = suggestions
    st.rerun()

