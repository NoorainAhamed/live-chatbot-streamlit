import streamlit as st
import wikipedia
import requests
from PIL import Image
from io import BytesIO

# Title
st.title("🧠 ROBO chatbot 🤖")

# Session state for conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Define your bot's logic
def chatbot_response(user_input):
    user_input = user_input.lower()
    
    # Basic rule-based responses
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?", None
    elif "your name" in user_input:
        return "I'm a ROBO let's have a chat to explore the world 🤩", None
    elif "bye" in user_input:
        return "Goodbye! Have a great day.", None
    else:
        # Try Wikipedia if no rule-based response
        try:
            # Get Wikipedia summary with 5 sentences
            summary = wikipedia.summary(user_input, sentences=5)
            
            # Try to get an image from the Wikipedia page
            try:
                page = wikipedia.page(user_input)
                if page.images:
                    # Get the first image URL
                    image_url = page.images[0]
                    
                    # Download and process the image
                    response = requests.get(image_url)
                    img = Image.open(BytesIO(response.content))
                    
                    return f"📖 From Wikipedia:\n\n{summary}", img
                else:
                    return f"📖 From Wikipedia:\n\n{summary}", None
            except:
                return f"📖 From Wikipedia:\n\n{summary}", None
                
        except wikipedia.exceptions.DisambiguationError as e:
            return f"⚠️ That query is too broad. Did you mean: {', '.join(e.options[:5])}?", None
        except wikipedia.exceptions.PageError:
            return "❌ Sorry, I couldn't find anything on Wikipedia for that.", None
        except Exception as e:
            return f"⚠️ An error occurred: {e}", None

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get bot response
    response, image = chatbot_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": response, "image": image})

# Display conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "image" in msg and msg["image"]:
            st.image(msg["image"], caption="Related image from Wikipedia", use_column_width=True)