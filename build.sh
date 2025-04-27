#!/bin/bash
mkdir -p build/html

# Loop through the .tex files directly in the repo root
for file in *.tex; do
    filename=$(basename "$file" .tex)
    pandoc "$file" -s --mathjax --toc -o "build/html/${filename}.html"
done

# Create manifest.json
echo "{" > build/manifest.json
for file in build/html/*.html; do
    filename=$(basename "$file" .html)
    echo "  \"$filename\": {\"title\": \"$filename\", \"slug\": \"$filename\", \"path\": \"build/html/$filename.html\" }," >> build/manifest.json
done
sed -i '$ s/,$//' build/manifest.json
echo "}" >> build/manifest.json

echo "Build complete!"
