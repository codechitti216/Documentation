import streamlit as st
import glob
import os
import frontmatter

# Page layout
st.set_page_config(page_title="ML Documentation", layout="wide")

# locate docs folder
BASE_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "docs"))

def load_docs():
    pattern = os.path.join(DOCS_DIR, "**", "*.md")
    doc_files = sorted(glob.glob(pattern, recursive=True))
    docs = []
    for path in doc_files:
        with open(path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
        docs.append({
            "path": path,
            "title": post.get("title", "No Title"),
            "tags":  post.get("tags", []),
            "body":  post.content
        })
    return docs

docs = load_docs()
all_tags = sorted({t for d in docs for t in d["tags"]})

# multi-tag selector
st.sidebar.title("📚 Topics")
selected_tags = st.sidebar.multiselect("Filter by Tags", options=all_tags)

if not selected_tags:
    filtered = docs
else:
    and_matches = [d for d in docs if all(tag in d["tags"] for tag in selected_tags)]
    or_matches  = [d for d in docs
                   if any(tag in d["tags"] for tag in selected_tags)
                      and d not in and_matches]
    filtered = and_matches + or_matches

# post selector
st.sidebar.title("📄 Posts")
titles = [d["title"] for d in filtered]
chosen = st.sidebar.selectbox("Select a Post", titles)

doc = next(d for d in filtered if d["title"] == chosen)
if doc:
    # single H1
    st.title(doc["title"])
    # strip leading "# " from Markdown to avoid duplicate H1
    lines = doc["body"].split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    clean = "\n".join(lines)
    # render Markdown + KaTeX math
    st.markdown(clean, unsafe_allow_html=False)  # math works again 
else:
    st.info("Please select a document.")
