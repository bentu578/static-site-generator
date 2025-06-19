import os
import shutil

# Paths to be created
new_md_files = [
    "content/blog/glorfindel/index.md",
    "content/blog/tom/index.md",
    "content/blog/majesty/index.md",
    "content/contact/index.md",
]

new_image_files = [
    "static/images/glorfindel.png",
    "static/images/tom.png",
    "static/images/rivendell.png",
]

# Check if all paths exist
md_exists = [os.path.exists(path) for path in new_md_files]
img_exists = [os.path.exists(path) for path in new_image_files]

md_check = all(md_exists)
img_check = all(img_exists)

md_status = list(zip(new_md_files, md_exists))
img_status = list(zip(new_image_files, img_exists))

md_check, img_check, md_status, img_status
