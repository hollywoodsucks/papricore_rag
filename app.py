import streamlit as st
import numpy as np
import sqlite3
from foundry_local_sdk import Configuration, FoundryLocalManager

# 1. DATABASE SETUP
def init_db():
    # Connect to SQLite (creates chat_history.db if it doesn't exist)
    conn = sqlite3.connect('chat_history.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)')
    conn.commit()
    return conn

conn = init_db()
c = conn.cursor()

# Load history from Database
def load_chat_history():
    c.execute('SELECT role, content FROM messages ORDER BY id ASC')
    return [{"role": row[0], "content": row[1]} for row in c.fetchall()]

# Save a message to Database
def save_message(role, content):
    c.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
    conn.commit()

# 2. PAGE CONFIGURATION
st.set_page_config(page_title="PapriCore AI", page_icon="🌱")
st.title("🌱 PapriCore Web Assistant")
st.write("Greenhouse Operations & Packaging AI")

@st.cache_resource
def setup_system():
    try:
        with open("guidelines.txt", "r", encoding="utf-8") as file:
            content = file.read()
            documents = [para.strip() for para in content.split('\n\n') if para.strip()]
    except FileNotFoundError:
        st.error("Error: guidelines.txt not found!")
        return None, None, None, None

    # HATA ÇÖZÜMÜ: Eğer sistem zaten başlatılmışsa (Streamlit yenilemesi yüzünden), hatayı yoksay.
    config = Configuration(app_name="papricore_rag")
    try:
        FoundryLocalManager.initialize(config)
    except Exception as e:
        if "already been initialized" not in str(e):
            raise e
            
    manager = FoundryLocalManager.instance

    emb_model = manager.catalog.get_model("qwen3-embedding-0.6b")
    emb_model.download()
    emb_model.load()
    emb_client = emb_model.get_embedding_client()

    doc_response = emb_client.generate_embeddings(documents)
    doc_embeddings = [item.embedding for item in doc_response.data]

    chat_model = manager.catalog.get_model("qwen2.5-0.5b")
    chat_model.download()
    chat_model.load()
    chat_client = chat_model.get_chat_client()

    return emb_client, chat_client, documents, doc_embeddings

with st.spinner("Loading AI Models... This might take a moment."):
    emb_client, chat_client, documents, doc_embeddings = setup_system()

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 3. CHAT HISTORY MANAGEMENT (Linked to SQLite)
if "messages" not in st.session_state:
    # Initial load from SQLite database
    st.session_state.messages = load_chat_history()

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    c.execute('DELETE FROM messages')
    conn.commit()
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. USER INPUT & RESPONSE
if user_query := st.chat_input("Ask a question about greenhouse rules..."):
    
    # Save and show user query
    st.session_state.messages.append({"role": "user", "content": user_query})
    save_message("user", user_query)
    
    with st.chat_message("user"):
        st.markdown(user_query)

    # Retrieval & Generation
    query_emb = emb_client.generate_embeddings([user_query]).data[0].embedding
    similarities = [cosine_similarity(query_emb, doc_emb) for doc_emb in doc_embeddings]
    best_match_idx = np.argmax(similarities)
    retrieved_context = documents[best_match_idx]

    system_prompt = (
        "You are PapriCore, a professional greenhouse operations and packaging assistant. "
        "Answer the user's questions clearly and strictly based on the provided 'Context' only."
    )
    llm_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context: {retrieved_context}\n\nQuestion: {user_query}"}
    ]

    response = chat_client.complete_chat(llm_messages)
    bot_reply = response.choices[0].message.content if hasattr(response, 'choices') else str(response)

    # Save and show AI response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    save_message("assistant", bot_reply)
    
    with st.chat_message("assistant"):
        st.markdown(bot_reply)