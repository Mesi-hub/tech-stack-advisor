from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

import os
import streamlit as st


def build_chain():
    # Load environment variables from .env
    load_dotenv()

    # Gemini API key is read from GOOGLE_API_KEY env var
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment/.env")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4,
        #google_api_key=api_key,  # optional if it's already in env, but explicit is clear
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a senior software architect helping developers make "
                    "good technical decisions. Be concise, practical, and specific. "
                    "Focus on architecture, tools, trade-offs, and best practices."
                ),
            ),
            (
                "human",
                (
                    "Developer question:\n"
                    "{question}\n\n"
                    "Answer for an experienced tech audience. "
                    "Use short paragraphs and bullets when helpful."
                ),
            ),
        ]
    )

    # LangChain Expression Language: prompt -> model
    chain = prompt | llm
    return chain


# =====================================================================
# EXISTING CODE: TERMINAL INTERFACE (COMMENTED OUT FOR REFERENCE)
# =====================================================================
# def main():
#     chain = build_chain()
#
#     print("Tech Stack Advisor (Gemini 2.5 Flash + LangChain)")
#     print("Ask architecture / tooling questions (type 'exit' to quit).\n")
#
#     while True:
#         user_input = input("You: ")
#         if user_input.strip().lower() in {"exit", "quit", "q"}:
#             print("Goodbye")
#             break
#
#         if not user_input.strip():
#             continue
#
#         try:
#             response = chain.invoke({"question": user_input})
#             print("\nAI:\n" + response.content + "\n")
#         except Exception as e:
#             print(f"Error while calling the model: {e}\n")
#
#
# if __name__ == "__main__":
#     main()
# =====================================================================


# =====================================================================
# NEW CODE: STREAMLIT WEB INTERFACE
# =====================================================================
def run_web_app():
    st.set_page_config(page_title="Tech Stack Advisor", page_icon="💻", layout="centered")
    st.title("Tech Stack Advisor 💻")
    st.caption("Ask architecture / tooling questions dynamically.")

    # Safely initialize the chain in the session state
    if "chain" not in st.session_state:
        try:
            st.session_state.chain = build_chain()
        except Exception as e:
            st.error(f"Initialization Error: {e}")
            st.stop()

    # Initialize chat history array
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages from history on redraw
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Capture live user inputs from the text UI box
    if user_input := st.chat_input("Ask a question..."):
        # Append user question to UI and storage
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate assistant response
        with st.chat_message("assistant"):
            try:
                response = st.session_state.chain.invoke({"question": user_input})
                st.markdown(response.content)
                st.session_state.messages.append({"role": "assistant", "content": response.content})
            except Exception as e:
                st.error(f"Error while calling the model: {e}")


if __name__ == "__main__":
    run_web_app()