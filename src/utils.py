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




def copy_static(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"📁 Created directory: {dest_dir}")

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), source_dir)
            dest_path = os.path.join(dest_dir, rel_path)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(os.path.join(root, file), dest_path)
            print(f"📄 Copied: {rel_path} → {dest_path}")

