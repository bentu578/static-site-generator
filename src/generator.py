import os
from src.utils import extract_title, markdown_to_html

def generate_page(markdown_path, template_path, dest_path, basepath="/"):
    with open(markdown_path, 'r') as f:
        markdown = f.read()

    title = extract_title(markdown)
    content = markdown_to_html(markdown)

    with open(template_path, 'r') as f:
        template = f.read()

    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    with open(dest_path, 'w') as f:
        f.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                rel_path = os.path.relpath(md_path, dir_path_content)
                rel_html_path = rel_path.replace(".md", ".html")

                output_path = os.path.join(dest_dir_path, rel_html_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                generate_page(md_path, template_path, output_path, basepath)
