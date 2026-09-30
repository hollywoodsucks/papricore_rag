import numpy as np
from foundry_local_sdk import Configuration, FoundryLocalManager

# 1. READ KNOWLEDGE BASE
try:
    with open("guidelines.txt", "r", encoding="utf-8") as file:
        content = file.read()
        # Split text into paragraphs
        documents = [para.strip() for para in content.split('\n\n') if para.strip()]
    print(f"Successfully loaded {len(documents)} guidelines from guidelines.txt!")
except FileNotFoundError:
    print("Error: guidelines.txt file not found!")
    exit()

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def main():
    print("\nStarting PapriCore System...")
    
    config = Configuration(app_name="papricore_rag")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # 2. LOAD MODELS AND VECTORIZE
    print("Loading embedding model (qwen3-embedding-0.6b)...")
    emb_model = manager.catalog.get_model("qwen3-embedding-0.6b")
    emb_model.download()
    emb_model.load()
    emb_client = emb_model.get_embedding_client()

    print("Vectorizing greenhouse guidelines...")
    doc_response = emb_client.generate_embeddings(documents)
    doc_embeddings = [item.embedding for item in doc_response.data]

    print("Loading AI model (qwen2.5-0.5b)...")
    chat_model = manager.catalog.get_model("qwen2.5-0.5b")
    chat_model.download()
    chat_model.load()
    chat_client = chat_model.get_chat_client()

    print("\n--- PAPRICORE RAG SYSTEM READY ---")
    
    # 3. USER CHAT LOOP
    while True:
        query = input("\nAsk a question (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            print("Shutting down PapriCore. Goodbye!")
            break
        
        # Retrieval phase
        query_emb = emb_client.generate_embeddings([query]).data[0].embedding
        similarities = [cosine_similarity(query_emb, doc_emb) for doc_emb in doc_embeddings]
        best_match_idx = np.argmax(similarities)
        retrieved_context = documents[best_match_idx]
        
        # Generation phase
        system_prompt = (
            "You are PapriCore, a professional greenhouse operations and packaging assistant. "
            "Answer the user's questions clearly and strictly based on the provided 'Context' only."
        )
        user_prompt = f"Context: {retrieved_context}\n\nQuestion: {query}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = chat_client.complete_chat(messages)
        
        if hasattr(response, 'choices') and len(response.choices) > 0:
            print(f"\nPapriCore: {response.choices[0].message.content}")
        else:
            print("\nPapriCore:", response)

if __name__ == "__main__":
    main()