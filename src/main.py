import sys
from src.generator import generate_pages_recursive
from src.utils import clean_and_create_dir, copy_static

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    output_dir = "docs"  # GitHub Pages expects the site in /docs

    clean_and_create_dir(output_dir)
    copy_static("static", output_dir)
    generate_pages_recursive("content", "template.html", output_dir, basepath)

if __name__ == "__main__":
    main()
