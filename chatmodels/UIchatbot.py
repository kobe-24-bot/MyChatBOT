
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    HumanMessage
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
}

.block-container {
    max-width: 850px;
    padding-top: 3rem;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    color: white;
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 16px;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# MODEL
# ============================================================

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.9,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🤖 AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Choose your AI personality and start chatting</div>',
    unsafe_allow_html=True
)


# ============================================================
# MODE SELECTION
# ============================================================

choice = st.radio(
    "🎭 Choose your AI mode",
    [
        "😢 Sad AI",
        "😂 Funny AI",
        "😐 Normal AI"
    ],
    horizontal=True
)


# ============================================================
# SET MODE
# ============================================================

if choice == "😢 Sad AI":

    mode = "You are a Sad AI agent"

elif choice == "😂 Funny AI":

    mode = "You are a Funny AI agent"

else:

    mode = "You are a Normal AI agent"


# ============================================================
# INITIALIZE MESSAGE HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        SystemMessage(content=mode)
    ]


# ============================================================
# UPDATE SYSTEM MESSAGE WHEN MODE CHANGES
# ============================================================

if st.session_state.messages[0].content != mode:

    st.session_state.messages = [
        SystemMessage(content=mode)
    ]


# ============================================================
# RESET CHAT
# ============================================================

if st.button(
    "🔄 Reset Chat",
    use_container_width=True
):

    st.session_state.messages = [
        SystemMessage(content=mode)
    ]

    st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):

        with st.chat_message(
            "user",
            avatar="👤"
        ):

            st.write(message.content)


    elif isinstance(message, AIMessage):

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            st.write(message.content)


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "💬 Type your message here..."
)


# ============================================================
# HANDLE USER INPUT
# ============================================================

if prompt:

    # Add user message
    st.session_state.messages.append(
        HumanMessage(
            content=prompt
        )
    )


    # Display user message
    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.write(prompt)


    # Get response
    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner("Thinking..."):

            response = model.invoke(
                st.session_state.messages
            )

        st.write(response.content)


    # Save AI response
    st.session_state.messages.append(
        AIMessage(
            content=response.content
        )
    )
