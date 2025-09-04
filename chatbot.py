# Import required libraries
import re
import random
import datetime
from IPython.display import display, clear_output
import ipywidgets as widgets

# Define the chatbot class
class SimpleChatbot:
    def __init__(self):
        self.name = "ChatBot"
        self.responses = {
            "greeting": [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! Nice to meet you. How can I assist you?"
            ],
            "goodbye": [
                "Goodbye! Have a great day!",
                "See you later!",
                "Bye! Come back anytime you need help."
            ],
            "thanks": [
                "You're welcome!",
                "Happy to help!",
                "Anytime! That's what I'm here for."
            ],
            "default": [
                "I'm not sure I understand. Could you rephrase that?",
                "I'm still learning. Could you try asking in a different way?",
                "That's interesting. Could you tell me more?"
            ]
        }
        
        # Patterns for pattern matching
        self.patterns = {
            r"hello|hi|hey|howdy": "greeting",
            r"bye|goodbye|see ya|see you": "goodbye",
            r"thanks|thank you|appreciate": "thanks",
            r"how are you|how's it going": "how_are_you",
            r"what time|what's the time": "time",
            r"what day|what's the date": "date",
            r"your name|who are you": "name",
            r"weather|temperature": "weather",
            r"joke|funny|make me laugh": "joke"
        }
        
        # Some jokes for the joke response
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "How does a penguin build its house? Igloos it together!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
    
    def get_response(self, user_input):
        # Convert to lowercase for easier matching
        user_input = user_input.lower()
        
        # Check for matches with patterns
        for pattern, category in self.patterns.items():
            if re.search(pattern, user_input):
                if category == "greeting":
                    return random.choice(self.responses["greeting"])
                elif category == "goodbye":
                    return random.choice(self.responses["goodbye"])
                elif category == "thanks":
                    return random.choice(self.responses["thanks"])
                elif category == "how_are_you":
                    return "I'm doing great, thanks for asking! How about you?"
                elif category == "time":
                    return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"
                elif category == "date":
                    return f"Today is {datetime.datetime.now().strftime('%Y-%m-%d')}"
                elif category == "name":
                    return f"I'm {self.name}, your friendly chatbot!"
                elif category == "weather":
                    return "I'm sorry, I don't have access to real-time weather data."
                elif category == "joke":
                    return random.choice(self.jokes)
        
        # If no pattern matches, return a default response
        return random.choice(self.responses["default"])

# Create the chatbot interface
def create_chatbot_interface():
    chatbot = SimpleChatbot()
    
    # Create widgets
    output = widgets.Output()
    text_input = widgets.Text(placeholder='Type your message here...')
    send_button = widgets.Button(description='Send')
    clear_button = widgets.Button(description='Clear Chat')
    
    # Display initial message
    with output:
        print(f"{chatbot.name}: {random.choice(chatbot.responses['greeting'])}")
    
    # Define functions for button clicks
    def on_send_clicked(b):
        user_message = text_input.value.strip()
        if user_message:
            with output:
                print(f"You: {user_message}")
                response = chatbot.get_response(user_message)
                print(f"{chatbot.name}: {response}")
            text_input.value = ''  # Clear the input
    
    def on_clear_clicked(b):
        output.clear_output()
        with output:
            print(f"{chatbot.name}: {random.choice(chatbot.responses['greeting'])}")
    
    def on_text_submit(sender):
        if text_input.value.strip():
            on_send_clicked(sender)
    
    # Link buttons to functions
    send_button.on_click(on_send_clicked)
    clear_button.on_click(on_clear_clicked)
    text_input.on_submit(on_text_submit)
    
    # Arrange widgets
    input_box = widgets.HBox([text_input, send_button, clear_button])
    chat_box = widgets.VBox([output, input_box])
    
    return chat_box

# Create and display the chatbot
chatbot_interface = create_chatbot_interface()
display(chatbot_interface)
