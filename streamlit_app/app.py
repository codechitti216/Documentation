import streamlit as st
import glob
import os
import frontmatter

st.set_page_config(page_title="ML Documentation", layout="wide")

import streamlit as st
import glob, os, frontmatter

# make glob absolute, regardless of where we run `streamlit run`
BASE_DIR = os.path.dirname(__file__)               # …/streamlit_app
DOCS_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "docs"))

def load_docs():
    pattern = os.path.join(DOCS_DIR, "**", "*.md")
    doc_files = sorted(glob.glob(pattern, recursive=True))
    docs = []
    for path in doc_files:
        with open(path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
        # now metadata is detected, because `---` was un-indented
        title = post.get("title", ...)
        tags  = post.get("tags", [])
        docs.append({ "title": title, "tags": tags, ... })
    return docs


docs = load_docs()

all_tags = sorted({tag for doc in docs for tag in doc["tags"]})

st.sidebar.title("📚 Topics")
selected_tag = st.sidebar.selectbox("Filter by Tag", ["All"] + all_tags)

if selected_tag == "All":
    filtered_docs = docs
else:
    filtered_docs = [doc for doc in docs if selected_tag in doc["tags"]]

doc_titles = [doc["title"] for doc in filtered_docs]
selected_doc_title = st.sidebar.selectbox("Select a Post", doc_titles)

selected_doc = next((doc for doc in filtered_docs if doc["title"] == selected_doc_title), None)

if selected_doc:
    st.title(selected_doc["title"])

    if selected_doc["tags"]:
        st.markdown("**Tags:** " + ", ".join(f"`{tag}`" for tag in selected_doc["tags"]))

    st.markdown("---")

    st.markdown(selected_doc["body"], unsafe_allow_html=True)
    st.latex("")  # Load MathJax
else:
    st.info("Please select a document from the sidebar.")
