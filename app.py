from langchain_core.runnables import RunnablePassthrough
# from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
from PIL import Image
from pathlib import Path
import os, uuid


base_path = Path(__file__).parent
img_path = base_path / "images" 

# Load images
assistant_crs = Image.open(img_path/"assistant_crs.png")
user_crs = Image.open(img_path/"user_crs.png")


def llm_model(model="moonshotai/kimi-k2-instruct-0905"):
    _ = load_dotenv(find_dotenv())
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key :
        try: 
            groq_api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            groq_api_key= None
    
    llm = ChatGroq(model=model, groq_api_key=groq_api_key)
    return llm

# --- CONFIGURATION CONSTANTS ---
HISTORY_STORE_KEY = "chat_history_store"    # Dict: session_id -> {name, history, is_placeholder_name}
CURRENT_SESSION_ID_KEY = "current_session_id"   # Tracks the ID of the active session
HISTORY_PLACEHOLDER_KEY = "history"     # Should match "input_history_key" parameterin RunnableWithMessageHistory

# --- 1. PERSISTENCE AND SESSION MANAGEMENT LOGIC

def initialize_session_state():
    """Initializes the required session state variables if they don't exist."""
    # 1. Dictionary to hold all sessions (key: session_id, value: InMemoryChatMessageHistory)
    if HISTORY_STORE_KEY not in st.session_state:
        st.session_state[HISTORY_STORE_KEY] = {}
        # Create a default initial session
        create_new_session("Chat 1")


def create_new_session(session_name: str):
    """Creates a new session and sets it as the active session."""
    new_id = str(uuid.uuid4())
    # Store the new history object and map it to a readable name
    st.session_state[HISTORY_STORE_KEY][new_id] = {
        "name" : session_name,
        "history" : InMemoryChatMessageHistory()
        # "placeholder_name" : 
    }
    st.session_state[CURRENT_SESSION_ID_KEY] = new_id
    # Reset the display buffer to show the new, empty chat
    st.session_state.display_messages = []


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Retrieves the history object for the given session_ID"""
    if session_id in st.session_state[HISTORY_STORE_KEY]:
        return st.session_state[HISTORY_STORE_KEY][session_id]["history"]
    else:
        # Fallback case, should not hif with proper initialization
        return InMemoryChatMessageHistory()


def delete_session(session_id: str):
    """Deletes the sesson ID from the session state"""
    # 1. Remove the history entry
    if session_id in st.session_state[HISTORY_STORE_KEY]:
        del st.session_state[HISTORY_STORE_KEY][session_id]
    # 2. check if the store is empty
    if not st.session_state[HISTORY_STORE_KEY]:
        # create a new session with default name
        create_new_session("Chat 1")
    else:
        # 3. Current Active session is the first one remaining
        st.session_state[CURRENT_SESSION_ID_KEY] = next(iter(st.session_state[HISTORY_STORE_KEY].keys()))
    # 4. Force rerun to update UI and load the new active chat
    st.rerun()


# --- 2. LANGCHAIN Setup ---
@st.cache_resource
def llm_chain():
    """ Initializes LLM and returns a RunnableWithMessageHistory instance.
    The @st.cache_resource decorator ensures this complex object is only created once.
    """
    # LLM  
    llm = llm_model()

    # prompt
    instruction = """ 
    IDENTITY & OWNERSHIP:
    - NAME: ChatAI 
    - OWNER/CREATOR: Co2fi-crs Rodolphe Segbedji
    - ROLE: You are a sophisticated, high-context Conversational Thought Partner. 
    You are not a static search engine; you are a proactive assistant designed to 
    engage in deep, meaningful, and fluid dialogue. 

    ANTI-HALLUCINATION & INTELLECTUAL HONESTY:
    - If a query is outside your training data or context window, state "I don't have 
   enough information to answer that accurately" rather than guessing.
   - Never fabricate facts, URLs, dates, or technical documentation.
   - If the user provides a premise that is factually incorrect, politely correct 
   the underlying assumption before answering.

"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", instruction),
            MessagesPlaceholder(variable_name = HISTORY_PLACEHOLDER_KEY),
            ("human", "{input}"),
        ])
    # parser
    parser = StrOutputParser()
    # chain
    chain = prompt | llm | parser

    # chain_with_message_history
    chain_with_memory = RunnableWithMessageHistory(
        runnable = chain,
        get_session_history = get_session_history,
        input_messages_key = "input",
        history_messages_key = HISTORY_PLACEHOLDER_KEY
    )

    return chain_with_memory

    
# --- 3. STREAMLIT UI AND EXECUTION ---

def main():

    # App title
    st.markdown("# 🧠 ChatAI 💡")
   
    # Initialize all required session state variables
    initialize_session_state()

    # Initialize the state-aware chain (chain with memory)
    chain = llm_chain()

    # Get the active session ID 
    current_session_id = st.session_state[CURRENT_SESSION_ID_KEY]
    current_session_data = st.session_state[HISTORY_STORE_KEY][current_session_id]
    current_session_name = current_session_data["name"] 
    current_history = get_session_history(current_session_id)

    # SideBar UI for Session Management
    with st.sidebar:
        st.header("Chat Sessions")
        # Map of ID to Name for the selectbox
        session_options = {
            k: v["name"] for k, v in st.session_state[HISTORY_STORE_KEY].items()
        }
        # Session selector
        selected_id = st.selectbox(
            "Select a Chat",
            options = list(session_options.keys()),
            format_func = lambda id: session_options[id],
            key = "session_select_box"
        )
        # Logic to switch a session if a different one is selected
        if selected_id != current_session_id:
            st.session_state[CURRENT_SESSION_ID_KEY] = selected_id
            # Force a rerun to load the new chat history
            st.rerun()

        # 2. New session Creator
        new_session_name = st.text_input("➕ New Session")
        if new_session_name and (new_session_name not in [v["name"] for v in st.session_state[HISTORY_STORE_KEY].values()]):
            create_new_session(new_session_name)
            st.rerun()
        if st.button("🗑️ Delete Session"):
            if len(st.session_state[HISTORY_STORE_KEY].keys()) > 1 :
                delete_session(current_session_id)
                st.rerun()
            else:
                st.error("Can't delete the only chat remaining. Create a new chat before deleting it. ")

    # --- MAIN CHAT DISPLAY---
    # Display messages from the current session's history object


    # Display current session messages 
    for message in current_history.messages:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        avatar=user_crs if role == "user" else assistant_crs
        with st.chat_message(role, avatar=avatar):
            st.markdown(message.content)

    # Handle user input
    user_input = st.chat_input(
        # "Type, or attach files, or record audio",
        "Converse with ChatAI",
        accept_file = "multiple",
        file_type = None,    # allow any file type. You can restrict if you want using a list of file type
        accept_audio = True,
    )

    if user_input:
        text = user_input.text or ""
        files = getattr(user_input, "files", [])
        audio = getattr(user_input, "audio", None)

        # show user message immedialtely
        with st.chat_message("user", avatar=user_crs):
            # Handle text input
            if text:
                st.markdown(text)

            # Handle file upload and show info about files and route by type
            for f in files:
                st.write(f"Uploaded: {f.name} ({f.type})")
                # Document-like types: call your RAG pipeline
                if f.type in ["application/pdf", "text/plain"]:
                    st.write("→ Calling RAG function for document")
                    # e.g. rag_answer = call_rag(f)
                elif f.type.startswith("image/"):
                    st.write("-> Calling image handler")
                    st.image(f)
                    # e.g. img_answer = handle_image(f)
                else:
                    st.write("-> Unsupported file type for special handling")
                
            # Handle audio
            if audio:
                st.write("Recorded audio")
                st.audio(audio)
                # e.g. text = transcribe(audio)
                # st.write(text)

        # Invoke the chain-aware to get AI response
        with st.chat_message("assistant", avatar= assistant_crs):
            with st.spinner("Thinking..."):
                # invoke the chain, passing the current session ID in the config
                ai_response = chain.invoke(
                    {"input": user_input.text},
                    config={"configurable": {"session_id": current_session_id}}
                )
                st.markdown(ai_response)


if __name__ == "__main__" :
    main() 
