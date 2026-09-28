import warnings
import logging

# Hide warnings and library logs
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# Gemini Model
# -----------------------------
model = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash"
)


# -----------------------------
# UI
# -----------------------------
st.title("🤖 AI Chatbot")
st.caption("Choose your AI personality and start chatting.")


# -----------------------------
# AI Mode Selection
# -----------------------------
choice = st.radio(
    "Choose your AI mode",
    options=[
        "😡 Angry Mode",
        "😂 Funny Mode",
        "😢 Sad Mode"
    ]
)

# ----------------------------- # AI Personality Modes # ----------------------------- 
MODES = {
    "😡 Angry Mode": ( "You are an angry AI agent. "
                       "You respond aggressively and   impatiently, "
                        "but remain helpful and do not use abusive language." ), 
    "😂 Funny Mode": ( "You are a very funny AI agent. " 
                      "Give helpful answers with appropriate humor." ),
    "😢 Sad Mode": ( "You are a sad AI agent. " 
                    "Respond in a slightly sad and emotional tone, " 
                    "while still being helpful." )

}

# -----------------------------
# Initialize Messages
# -----------------------------
if "messages" not in st.session_state: 
    st.session_state.messages = []
if "current_mode" not in st.session_state: 
    st.session_state.current_mode = "😂 Funny Mode"


# ----------------------------- 
# Sidebar
# ----------------------------- 
with st.sidebar: 
    st.header("⚙️ Settings") 
    choice = st.radio( 
        "Choose your AI personality", 
        options=list(MODES.keys()), 
        index=list(MODES.keys()).index( st.session_state.current_mode ) ) 
    # Clear chat 
    if st.button("🗑️ Clear Chat"): 
        st.session_state.messages = [] 
        st.rerun()


# ----------------------------- 
# Handle Mode Change 
# ----------------------------- 
if choice != st.session_state.current_mode:
    st.session_state.current_mode = choice 
    st.session_state.messages = [] 

    st.rerun() 
    
mode = MODES[st.session_state.current_mode]


# ----------------------------- 
# Page UI 
# ----------------------------- 
st.title("🤖 Gemini AI Chatbot") 
st.caption( f"Currently using: **{st.session_state.current_mode}**" )


# ----------------------------- 
# Display Chat History 
# ----------------------------- 
for message in st.session_state.messages: 
    if isinstance(message, HumanMessage): 
        with st.chat_message("user"): 
            st.write(message.content) 
    elif isinstance(message, AIMessage): 
        with st.chat_message("assistant"): 
            st.write(message.content)

# ----------------------------- 
# Chat Input 
# ----------------------------- 
prompt = st.chat_input( "Type your message..." )



# ----------------------------- 
# Generate Response 
# -----------------------------
if prompt: 
    #Display user message 
    with st.chat_message("user"): 
        st.write(prompt) 
    # Create messages for Gemini 
    conversation = [ SystemMessage(content=mode) ] 
    conversation.extend( 
        st.session_state.messages
    ) 
    conversation.append( HumanMessage(content=prompt) )



# Save user message
st.session_state.messages.append(
     HumanMessage(content=prompt) )

try: 
    with st.chat_message("assistant"): 
        with st.spinner("Thinking..."): 
            result = model.invoke( conversation ) 
            if isinstance(result.content, str): 
                response = result.content 
            else: 
                response = result.content[0]["text"] 
            st.write(response)

            # Save AI response
            st.session_state.messages.append( AIMessage(content=response) )
except Exception as e: 
    error_text = str(e) 
    if ( "429" in error_text or "RESOURCE_EXHAUSTED" in error_text ):
        error_message = ( "⚠️ API quota exceeded. " "Please try again later." )

    else: error_message = ( 
        "❌ Something went wrong. " "Please check your API key and configuration." ) 
    with st.chat_message("assistant"): 
        st.error(error_message)












# If user changes mode, update system message
if (
    len(st.session_state.messages) == 1
    or st.session_state.messages[0].content != mode
):
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]


# -----------------------------
# Display Previous Messages
# -----------------------------
for message in st.session_state.messages:

    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)


# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Type your message...")


if prompt:

    # User message
    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message("user"):
        st.write(prompt)

    try:

        # Gemini response
        result = model.invoke(
            st.session_state.messages
        )

        # Keep your original response handling
        response = result.content[0]["text"]

        # Store AI response
        st.session_state.messages.append(
            AIMessage(content=response)
        )

        # Display AI response
        with st.chat_message("assistant"):
            st.write(response)

    except Exception as e:

        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            error_message = (
                "API quota exceeded. Please try again later."
            )

        else:
            error_message = "Something went wrong."

        with st.chat_message("assistant"):
            st.write(error_message)