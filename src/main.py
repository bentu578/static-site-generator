import sys
from src.generator import generate_pages_recursive
from src.utils import clean_and_create_dir

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    output_dir = "docs"  # GitHub Pages expects the site in /docs

    clean_and_create_dir(output_dir)
    generate_pages_recursive("content", "template.html", output_dir, basepath)

if __name__ == "__main__":
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    clean_and_create_dir("docs")
    generate_pages_recursive("content", "template.html", "docs", base_path)
