import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st
from retriever import load_chunks, build_chroma_index
from generate import retrieve_and_answer

st.set_page_config(page_title="ADHD Psychoeducation Assistant", page_icon="🧠")
st.title("ADHD Psychoeducation Assistant")
st.caption("Answers are grounded only in CDC/CHADD source material — not general knowledge.")

@st.cache_resource
def load_index():
    chunks = load_chunks()
    collection = build_chroma_index(chunks)
    return collection

collection = load_index()

if "history" not in st.session_state:
    st.session_state.history = []

# Replay previous turns
for q, a, sources in st.session_state.history:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(a)
        with st.expander("Sources used"):
            for s in sources:
                st.write(f"- {s['source']}")

query = st.chat_input("Ask a question about ADHD...")

if query:
    with st.chat_message("user"):
        st.write(query)
    with st.spinner("Retrieving and generating answer..."):
        answer, sources = retrieve_and_answer(query, collection)
    with st.chat_message("assistant"):
        st.write(answer)
        with st.expander("Sources used"):
            for s in sources:
                st.write(f"- {s['source']}")
    st.session_state.history.append((query, answer, sources))