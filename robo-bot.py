import streamlit as st
import wikipedia
import requests
from io import BytesIO
from PIL import Image
import random
import time
from datetime import datetime
import base64

# Set page configuration
st.set_page_config(
    page_title="Robo Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with the provided color scheme
st.markdown(f"""
<style>
    /* Global styles */
    .stApp {{
        background-color: #F9FAFB;
    }}
    .main-header {{
        font-size: 3rem;
        color: #2563EB;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }}
    .sub-header {{
        color: #2563EB;
        font-weight: 600;
    }}
    /* Chat container */
    .chat-container {{
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        height: 600px;
        overflow-y: auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #E5E7EB;
    }}
    /* Message styles */
    .user-message {{
        background-color: #2563EB;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 0 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .bot-message {{
        background-color: #F3F4F6;
        color: #111827;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 0;
        margin: 10px 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    .message-time {{
        font-size: 0.7rem;
        color: #6B7280;
        text-align: right;
        margin-top: 5px;
    }}
    /* Button styles */
    .stButton button {{
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        transition: all 0.3s;
    }}
    .stButton button:hover {{
        background-color: #3B82F6;
        color: white;
    }}
    /* Suggestion chips */
    .suggestion-chip {{
        display: inline-block;
        background-color: #EFF6FF;
        color: #2563EB;
        padding: 8px 16px;
        border-radius: 20px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid #BFDBFE;
        font-size: 0.9rem;
    }}
    .suggestion-chip:hover {{
        background-color: #DBEAFE;
        color: #1E40AF;
    }}
    /* File upload area */
    .uploaded-file {{
        background-color: #F0FDF4;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #16A34A;
    }}
    /* Voice recording button */
    .voice-recorder {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 15px 0;
    }}
    /* Sidebar */
    .sidebar .sidebar-content {{
        background-color: #FFFFFF;
    }}
    /* Metrics */
    .stMetric {{
        background-color: #FFFFFF;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #2563EB;
    }}
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #F3F4F6;
        border-radius: 8px 8px 0 0;
        padding: 10px 16px;
        font-weight: 500;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #2563EB;
        color: white;
    }}
    /* Success, Error, Warning */
    .success-box {{
        background-color: #F0FDF4;
        color: #166534;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #16A34A;
        margin: 10px 0;
    }}
    .error-box {{
        background-color: #FEF2F2;
        color: #991B1B;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #DC2626;
        margin: 10px 0;
    }}
    .warning-box {{
        background-color: #FFFBEB;
        color: #92400E;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #F59E0B;
        margin: 10px 0;
    }}
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
    - Voice interaction capabilities
    - File upload features
    """)
    
    st.markdown("---")
    st.subheader("Settings")
    
    # Voice settings
    st.markdown("**Voice Settings**")
    voice_enabled = st.checkbox("Enable Text-to-Speech", value=False)
    
    # Clear conversation button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.success("Conversation cleared!")
    
    st.markdown("---")
    st.subheader("File Upload")
    uploaded_file = st.file_uploader("Upload a file or image", type=['txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx'])
    
    if uploaded_file is not None:
        file_details = {
            "FileName": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": uploaded_file.size
        }
        st.write(file_details)
        
        # Read and display file content based on type
        if uploaded_file.type == "text/plain":
            text_content = str(uploaded_file.read(), "utf-8")
            st.text_area("File Content", text_content, height=200)
        elif uploaded_file.type.startswith("image"):
            st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)
    
    st.markdown("---")
    st.subheader("Example Queries")
    example_queries = [
        "Tell me about artificial intelligence", 
        "What is machine learning?", 
        "Explain quantum computing",
        "Who is Albert Einstein?",
        "What is the history of the internet?"
    ]
    
    for query in example_queries:
        if st.button(f"🔍 {query}", key=f"example_{query}"):
            st.session_state.user_input = query
            st.rerun()

# Session state for conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Suggested questions
suggested_questions = [
    "What can you tell me about climate change?",
    "Explain the theory of relativity",
    "Who was Marie Curie?",
    "What are the latest advancements in AI?",
    "Tell me about the solar system"
]

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
    
    # Voice input section
    st.markdown("**Voice Input**")
    voice_col1, voice_col2 = st.columns(2)
    
    with voice_col1:
        if st.button("🎤 Start Recording", use_container_width=True):
            st.info("Voice recording would be implemented here with proper libraries")
            # This would be replaced with actual speech-to-text implementation
            st.session_state.user_input = "Example voice input"
            st.rerun()
    
    with voice_col2:
        if st.button("🔊 Read Last Response", use_container_width=True) and voice_enabled and st.session_state.messages:
            st.info("Text-to-speech would read the last response")
            # This would be replaced with actual text-to-speech implementation
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message"><b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
                if "timestamp" in msg:
                    st.markdown(f'<div class="message-time">{msg["timestamp"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message"><b>Robo:</b> {msg["content"]}</div>', unsafe_allow_html=True)
                if "timestamp" in msg:
                    st.markdown(f'<div class="message-time">{msg["timestamp"]}</div>', unsafe_allow_html=True)
                if msg.get("image"):
                    st.image(msg["image"], caption="Related image", use_column_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Suggested questions
    st.markdown("**💡 Suggested questions:**")
    cols = st.columns(2)
    for i, question in enumerate(suggested_questions):
        with cols[i % 2]:
            if st.button(question, key=f"suggest_{i}"):
                st.session_state.user_input = question
                st.rerun()

    # User input
    user_input = st.chat_input("Type your message here...")

with col2:
    # Use tabs for different information sections
    tab1, tab2, tab3 = st.tabs(["📊 Stats", "📁 Files", "ℹ️ Info"])
    
    with tab1:
        st.markdown("### Conversation Statistics")
        
        # Display some statistics
        if st.session_state.messages:
            user_msgs = sum(1 for msg in st.session_state.messages if msg["role"] == "user")
            bot_msgs = sum(1 for msg in st.session_state.messages if msg["role"] == "bot")
            
            st.metric("Total Messages", len(st.session_state.messages))
            st.metric("Your Messages", user_msgs)
            st.metric("My Responses", bot_msgs)
            st.metric("Conversation Duration", f"{len(st.session_state.messages)*0.5} min")
        else:
            st.info("Start a conversation to see statistics here.")
    
    with tab2:
        st.markdown("### File Management")
        
        if uploaded_file is not None:
            st.markdown("**📁 Uploaded File**")
            st.markdown(f'<div class="uploaded-file">'
                       f'<strong>{uploaded_file.name}</strong><br>'
                       f'Type: {uploaded_file.type}<br>'
                       f'Size: {uploaded_file.size} bytes'
                       f'</div>', unsafe_allow_html=True)
        else:
            st.info("No files uploaded yet. Use the sidebar to upload files.")
    
    with tab3:
        st.markdown("### Tips & Information")
        
        # Display fun facts or tips
        tips = [
            "💡 Tip: Ask about historical events, scientific concepts, or famous people!",
            "🔍 Did you know? Wikipedia has over 6 million articles in English.",
            "🌐 Robo Chatbot can fetch information from Wikipedia in seconds.",
            "🤖 I'm constantly learning! The more you ask, the smarter I become.",
            "🎤 Use the voice feature for hands-free interaction!"
        ]
        
        st.info(random.choice(tips))
        
        st.markdown("---")
        st.markdown("**How to use:**")
        st.markdown("""
        1. Type your question in the chat box
        2. Use voice recording for hands-free interaction
        3. Upload files for additional context
        4. Click suggested questions for quick ideas
        """)

# Process user input
if user_input and user_input.strip():
    # Add user message to chat history with timestamp
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": timestamp})
    
    # Get bot response
    with st.spinner("Robo is thinking..."):
        time.sleep(0.5)  # Simulate thinking time
        response, image = chatbot_response(user_input)
    
    # Add bot response to chat history with timestamp
    timestamp = datetime.now().strftime("%H:%M:%S")
    message_data = {"role": "bot", "content": response, "timestamp": timestamp}
    if image:
        message_data["image"] = image
    st.session_state.messages.append(message_data)
    
    # Rerun to update the conversation
    st.rerun()
