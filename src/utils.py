import os
import shutil
import markdown

def clean_and_create_dir(path):
    """Deletes a directory if it exists and recreates it."""
    if os.path.exists(path):
        print(f"🧹 Removing existing directory: {path}")
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)
    print(f"📁 Created directory: {path}")

def extract_title(md_content):
    """Extract the title from the markdown content"""
    for line in md_content.split('\n'):
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"

def markdown_to_html(md_content):
    """Convert markdown content to HTML"""
    return markdown.markdown(md_content)






