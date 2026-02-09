import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Ensure GEMINI_API_KEY in your .env file
client = genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
# "gemini-1.5-flash" is great for speed and chat interactions.
model = genai.GenerativeModel('gemini-2.0-flash-lite')

# THE SYSTEM PROMPT
# This is where we define the AI's personality and rules.
SYSTEM_PROMPT = """
You are the "TalentScout" Hiring Assistant. Your goal is to screen candidates for technology roles.
Maintain a professional, friendly, and encouraging tone.

YOUR PROCESS:
1. GREETING: Briefly greet the candidate and explain you are here to gather their details and assess their technical skills.

2. INFO GATHERING: You must collect the following details. Do NOT ask for all of them at once. Ask for 1 or 2 items at a time to keep the conversation natural:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Desired Position
   - Current Location
   - Tech Stack (Languages, Frameworks, Tools)

3. TECH SCREENING: Once the user provides their Tech Stack:
   - Generate 3-5 conceptual technical questions based *specifically* on the tools they listed.
   - Do not ask for code snippets, just conceptual understanding.
   - Wait for their answer before moving to the next question or topic.

4. CLOSING: If the user says "Goodbye" or indicates they are done:
   - Thank them for their time.
   - Inform them that a human recruiter will review their profile and contact them.
   - Stop asking questions.

CONSTRAINTS:
- If the user asks irrelevant questions (e.g., "What is the weather?"), politely steer them back to the interview.
- Keep responses concise.
"""

def get_ai_response(message_history):
    """
    Sends the message history to the LLM and gets a response.
    messages_history format: [{"role": "user", "content": "hi"}, ...]
    """

    try:
        # 1. Start a chat session
        chat = model.start_chat(history=[])

        # 2. Send the System Prompt first to set context
        # Gemini handles system instructions differently, but sending it as the first user message works well for simple implementation.
        chat.send_message(SYSTEM_PROMPT)

        # 3. Replay history to get the model up to speed
        # We skip the very first message in messages_history if it was the initial "Hello" from the bot
        # because we need to establish the flow correctly.
        for msg in message_history:
            if msg["role"] == "user":
                chat.send_message(msg["content"])
            elif msg["role"] == "assistant":
                # In a real chat object, we can't easily force the assistant's previous replies 
                # into the history object manually without using the history param in start_chat.
                # HOWEVER, for a simple stateless call, we can just feed the last user message 
                # combined with context.
                pass 
        
        # IMPROVED APPROACH FOR GEMINI:
        # Instead of replaying the whole chat object every time (which can get complex with Gemini's specific object types),
        # we can construct a single prompt chain or use the history properly.
        
        # Let's use the simplest reliable method: Construct the history list for Gemini
        gemini_history = []
        
        # Add system prompt as the first "user" turn, followed by an "acknowledged" model turn
        gemini_history.append({"role": "user", "parts": [SYSTEM_PROMPT]})
        gemini_history.append({"role": "model", "parts": ["Understood. I am ready to act as the TalentScout Hiring Assistant."]})

        # Add the rest of the conversation
        for msg in message_history[:-1]: # Exclude the very last user message (we send that next)
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        # Initialize chat with history
        chat_session = model.start_chat(history=gemini_history)
        
        # Send the latest user message
        last_user_message = message_history[-1]["content"]
        response = chat_session.send_message(last_user_message)
        
        return response.text
    
    except Exception as e:
        return f"Error: {str(e)}"