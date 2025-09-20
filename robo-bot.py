import streamlit as st
import wikipedia
import requests
from io import BytesIO
from PIL import Image
import random

# Set page configuration
st.set_page_config(
    page_title="Robo Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* General App Styling */
    body {
        font-family: "Segoe UI", Roboto, sans-serif;
    }
    .main-header {
        font-size: 3rem;
        color: #0d6efd;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .chat-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        height: 600px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        font-size: 1rem;
        line-height: 1.5;
    }
    .user-message {
        background: linear-gradient(135deg, #e6f7ff, #d0ebff);
        padding: 12px 16px;
        border-radius: 12px;
        margin: 12px 0;
        text-align: right;
        font-size: 1rem;
        word-wrap: break-word;
    }
    .bot-message {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 12px 16px;
        border-radius: 12px;
        margin: 12px 0;
        text-align: left;
        font-size: 1rem;
        word-wrap: break-word;
    }
    .wikipedia-image {
        max-width: 100%;
        border-radius: 10px;
        margin-top: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold;
        font-size: 1rem;
        padding: 8px;
        margin-top: 5px;
    }
    .stButton button:hover {
        background-color: #45a049 !important;
        transform: scale(1.02);
        transition: 0.2s;
    }
    /* Scrollbar Styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background: #bbb;
        border-radius: 4px;
    }
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #888;
    }
</style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown('<h1 class="main-header">🤖 Robo Chatbot</h1>', unsafe_allow_html=True)
st.markdown("### Your intelligent assistant with Wikipedia knowledge")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4711/4711984.png", width=100)
    st.title("About Robo Chatbot")
    st.info("""
    I'm your friendly AI assistant powered by:
    - Streamlit for the interface
    - Wikipedia API for knowledge
    - Advanced NLP for conversations
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

# Session state for conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get Wikipedia image
def get_wikipedia_image(page_title):
    try:
        # Get page and check for images
        page = wikipedia.page(page_title, auto_suggest=False)
        if page.images:
            # Try to get a relevant image (often the first image is the most relevant)
            image_url = page.images[0]
            
            # Filter out non-image files and logos
            if any(ext in image_url for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg']):
                # Avoid Wikipedia logos and icons
                if not any(word in image_url for word in ['logo', 'icon', 'Wiki', 'svg']):
                    response = requests.get(image_url)
                    img = Image.open(BytesIO(response.content))
                    return img, image_url
            
            # If first image didn't work, try others
            for img_url in page.images[1:5]:
                if any(ext in img_url for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    if not any(word in img_url for word in ['logo', 'icon', 'Wiki']):
                        response = requests.get(img_url)
                        img = Image.open(BytesIO(response.content))
                        return img, img_url
    except:
        pass
    return None, None

# Define your bot's logic
def chatbot_response(user_input):
    user_input_lower = user_input.lower()
    
    # Basic rule-based responses
    greeting_responses = [
        "Hello! I'm Robo Chatbot. How can I assist you today?",
        "Hi there! What would you like to know?",
        "Greetings! I'm here to help with your questions."
    ]
    
    if any(word in user_input_lower for word in ["hello", "hi", "hey", "greetings"]):
        return random.choice(greeting_responses), None
    elif "your name" in user_input_lower:
        return "I'm Robo Chatbot, your friendly AI assistant!", None
    elif any(word in user_input_lower for word in ["bye", "goodbye", "see you"]):
        return "Goodbye! Feel free to come back if you have more questions.", None
    elif "thank" in user_input_lower:
        return "You're welcome! Is there anything else you'd like to know?", None
    else:
        # Try Wikipedia if no rule-based response
        try:
            # Get Wikipedia summary with 5 sentences
            summary = wikipedia.summary(user_input, sentences=5)
            
            # Try to get an image
            img, img_url = get_wikipedia_image(user_input)
            
            return f"📖 According to Wikipedia:\n\n{summary}", img
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:5]
            return f"⚠️ That query is too broad. Did you mean: {', '.join(options)}?", None
        except wikipedia.exceptions.PageError:
            return "❌ Sorry, I couldn't find anything on Wikipedia for that. Could you try a different query?", None
        except Exception as e:
            return f"⚠️ An error occurred: {str(e)}", None

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Conversation")
    
    # Chat container
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

    # User input
    user_input = st.chat_input("Type your message here...")

with col2:
    st.markdown("### ℹ️ Information Panel")
    
    # Display fun facts or tips
    tips = [
        "💡 Tip: Ask about historical events, scientific concepts, or famous people!",
        "🔍 Did you know? Wikipedia has over 6 million articles in English.",
        "🌐 Robo Chatbot can fetch information from Wikipedia in seconds.",
        "🤖 I'm constantly learning! The more you ask, the smarter I become."
    ]
    
    st.info(random.choice(tips))
    
    # Display some statistics
    if st.session_state.messages:
        user_msgs = sum(1 for msg in st.session_state.messages if msg["role"] == "user")
        bot_msgs = sum(1 for msg in st.session_state.messages if msg["role"] == "bot")
        st.metric("Conversation Length", f"{len(st.session_state.messages)} messages")
        st.metric("Your Messages", user_msgs)
        st.metric("My Responses", bot_msgs)

# Process user input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    response, image = chatbot_response(user_input)
    message_data = {"role": "bot", "content": response}
    if image:
        message_data["image"] = image
    st.session_state.messages.append(message_data)
    
    # Rerun to update the conversation
    st.rerun()
