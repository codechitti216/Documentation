import json
import streamlit as st
from streamlit.components.v1 import html

import os

# Ensure the file exists
if not os.path.exists('build/manifest.json'):
    raise FileNotFoundError("The manifest.json file is missing. Did you run ./build.sh?")

with open('build/manifest.json') as f:
    manifest_data = f.read()

# Load manifest
with open("build/manifest.json") as f:
    pages = json.load(f)

page = list(pages.values())[0]  # Only one page for now

st.title(page["title"])

html_code = open(page["path"], "r").read()

html(f"""
  <head>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async
      src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>
    <style>
      body {{ font-family: Georgia, serif; line-height: 1.6; margin: 2rem; }}
      h1, h2, h3 {{ font-weight: 600; }}
    </style>
  </head>
  <body>
    {html_code}
  </body>
""", height=800)
