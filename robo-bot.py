import streamlit as st
import wikipedia
import requests
from io import BytesIO
from PIL import Image
import random
import time
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Robo Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with the provided color scheme
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        background-color: #F9FAFB;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #111827;
    }
    /* Main header */
    .main-header {
        font-size: 3.2rem;
        color: #2563EB;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        user-select: none;
    }
    /* Sub headers */
    .sub-header {
        color: #2563EB;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    /* Chat container */
    .chat-container {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 24px 28px;
        height: 620px;
        overflow-y: auto;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.15);
        border: 1.5px solid #E0E7FF;
        scroll-behavior: smooth;
    }
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    .chat-container::-webkit-scrollbar-track {
        background: #F9FAFB;
        border-radius: 10px;
    }
    .chat-container::-webkit-scrollbar-thumb {
        background-color: #2563EB;
        border-radius: 10px;
    }
    /* Message styles */
    .user-message {
        background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%);
        color: white;
        padding: 14px 20px;
        border-radius: 24px 24px 0 24px;
        margin: 12px 0;
        max-width: 75%;
        margin-left: auto;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 极速赛车开奖直播历史记录+极速赛车开奖结果|澳洲10开奖官网 0.3);
        word-wrap: break-word;
        user-select: text;
        transition: background 0.3s ease;
    }
    .user-message:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%);
        cursor: text;
    }
    .bot-message {
        background-color: #F3F4F6;
        color: #1F2937;
        padding: 14px 20px;
        border-radius: 24px 24px 24px 0;
        margin: 12px 0;
        max-width: 75%;
        margin-right: auto;
        font-size: 1rem;
        box-shadow: 0 4极速赛车开奖直播历史记录+极速赛车开奖结果|澳洲10开奖官网 px 12px rgba(156, 163, 175, 0.3);
        word-wrap: break-word;
        user-select: text;
        white-space: pre-line;
    }
    /* Message timestamp */
    .message-time {
        font-size: 0.75rem;
        color: #6B7280;
        text-align: right;
        margin-top: 6px;
        user-select: none;
        font-style: italic;
    }
    /* Image in bot message */
    .bot-message img {
        margin-top: 12px;
        border-radius: 16px;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.2);
        max-height: 300px;
        object-fit: contain;
        user-select: none;
    }
    /* Button styles */
    .stButton button {
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.3) !important;
        transition: background-color 0.3s ease, box-shadow 0.3s ease !important;
        user-select: none;
    }
    .stButton button:hover {
        background-color: #3B82F6 !important;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.5) !important;
        color: white !important;
        cursor: pointer !important;
    }
    .stButton button:focus {
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.6) !important;
    }
    /* Suggestion chips */
    .suggestion-chip {
        display: inline-block;
        background-color: #EFF6FF;
        color: #2563EB;
        padding: 10极速赛车开奖直播历史记录+极速赛车开奖结果|澳洲10开奖官网 px 22px;
        border-radius: 30px;
        margin: 6px 8px 6px 0;
        cursor: pointer;
        transition: all 0.25s ease;
        border: 2px solid #BFDBFE;
        font-size: 1rem;
        font-weight: 600;
        user-select: none;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.15);
        white-space: nowrap;
    }
    .suggestion-chip:hover {
        background-color: #DBEAFE;
        color: #1E40AF;
        border-color: #3B82F6;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
    }
    /* File upload area */
    .uploaded-file {
        background-color: #F0极速赛车开奖直播历史记录+极速赛车开奖结果|澳洲10开奖官网 FDF4;
        padding: 16px 20px;
        border-radius: 12px;
        margin: 14px 0;
        border-left: 6px solid #16A34A;
        font-weight: 600;
        color: #166534;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.15);
        user-select: text;
    }
    /* Voice recording button container */
    .voice-recorder {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0 30px 0;
        gap: 20px;
    }
    /* Voice buttons */
    .voice-recorder button {
        background-color: #2563EB !important;
        color: white !important;
        border-radius: 50% !important;
        width: 56px !important;
        height: 56px !important;
        font-size: 1.5rem !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4) !important;
        transition: background-color 0.3s ease, box-shadow 0.3s ease !important;
        user-select: none;
    }
    .voice-recorder button:hover {
        background-color: #3B82F6 !important;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.6) !important;
        cursor: pointer !important;
    }
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #FFFFFF;
        padding: 20px 24px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.1);
    }
    /* Metrics */
    .stMetric {
        background-color: #FFFFFF;
        padding: 14px 20px;
        border-radius: 12px;
        border-left: 6px solid #2563EB;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.15);
        font-weight: 700;
        color: #1E40极速赛车开奖直播历史记录+极速赛车开奖结果|澳洲10开奖官网 AF;
        user-select: none;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F3F4F6;
        border-radius: 12px 12px 0 0;
        padding: 14px 22px;
        font-weight: 700;
        font-size: 1rem;
        color: #2563EB;
        user-select: none;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB;
        color: white;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4);
    }
    /* Success, Error, Warning boxes */
    .success-box {
        background-color: #F0FDF4;
        color: #166534;
        padding: 16px 20px;
        border-radius: 12px;
        border-left: 6px solid #16A34A;
        margin: 14px 0;
        font-weight: 600;
        box-shadow: 0 6px 18px rgba(22, 163, 74, 0.2);
        user-select: none;
    }
    .error-box {
        background-color: #FEF2F2;
        color: #991B1B;
        padding: 16px 20px;
        border-radius: 12px;
        border-left: 6px solid #DC2626;
        margin: 14px 0;
        font-weight: 600;
        box-shadow: 0 6px 18px rgba(220, 38, 38, 0.2);
        user-select: none;
    }
    .warning-box {
        background-color: #FFFBEB;
        color: #92400E;
        padding: 16px 20px;
        border-radius: 12px;
        border-left: 6px solid #F59E0B;
        margin: 14px 0;
        font-weight: 600;
        box-shadow: 0 6px 18px rgba(245, 158, 11, 0.2);
        user-select: none;
    }
    /* Chat input box */
    .stChatInput textarea {
        border-radius: 16px !important;
        border: 2px solid #2563EB !important;
        padding: 14px 18px !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #1F2937 !important;
        resize: none !important;
        transition: border-color 0.3s ease !important;
    }
    .stChatInput textarea:focus {
        border-color: #3B82F6 !important;
        outline: none !important;
        box-shadow: 0极速赛车开奖直播极速赛车开奖直播历史记录+极速赛车开奖结果|澳洲10开奖官网 历史记录+极速赛车开奖结果|澳洲10开奖官网 0 0 8px rgba(59, 130, 246, 0.5) !important;
    }
    /* Response done indicator */
    .response-done {
        display: inline-block;
        background-color: #16A34A;
        color: white;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-left: 12px;
        user-select: none;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.4);
        vertical-align: middle;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(22, 163, 74, 0); }
        100% { box-shadow: 0 0 0 0 rgba(22, 163, 74, 0); }
    }
</style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown('<h1 class="main-header">🤖 Robo Chatbot</h1>', unsafe_allow_html=True)
st.markdown("### Your intelligent assistant with Wikipedia knowledge")

# Sidebar
with st.sidebar:
