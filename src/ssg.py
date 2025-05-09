import os
import shutil

from mdparser import extract_title, markdown_to_html_node

SSG_TITLE = "<!--SSG_TITLE-->"
SSG_TARGET = "<!--SSG_TARGET-->"


def generate_pages(template_path: str, src_dir: str, dest_root: str, **kwargs):
    ls = os.listdir(src_dir)

    for f in ls:
        if os.path.isfile(os.path.join(src_dir, f)):
            generate_page(
                template_path,
                os.path.join(src_dir, f),
                os.path.join(dest_root, f"{f.rstrip(".md")}.html"),
                **kwargs,
            )
        else:
            generate_pages(
                template_path,
                os.path.join(src_dir, f),
                os.path.join(dest_root, f),
                **kwargs,
            )


def generate_page(template_path: str, md_path: str, dest_path: str, **kwargs):
    template = ""
    md = ""
    base_path = kwargs.get("base_path", "/")

    with open(template_path) as tmpl, open(md_path) as mdf:
        template = tmpl.read()
        md = mdf.read()

    os.makedirs(os.path.dirname(dest_path), 0o755, True)

    with open(dest_path, "w") as html_file:
        print(f"Generating page {dest_path} from {md_path} using {template_path}")
        html_tree = markdown_to_html_node(md)
        title = extract_title(html_tree)
        template = template.replace(SSG_TITLE, title).replace(
            SSG_TARGET,
            html_tree.to_html()
            .replace('href="/', 'href="' + base_path)
            .replace('src="/', 'src="' + base_path),
        )
        html_file.write(template)


def copy_dir(src: str, dest: str):
    if not os.path.exists(src) or os.path.isfile(src):
        raise ValueError(f"src must be a directory: {src}")
    if os.path.isfile(dest):
        raise ValueError(f"dest must be a directory: {dest}")

    if not os.path.exists(dest):
        os.makedirs(dest, 0o755, True)

    _clear_dir(dest)
    contents = os.scandir(src)
    for file in contents:
        if file.is_file():
            shutil.copy(file.path, dest + os.path.sep + file.name)
        else:
            copy_dir(file.path, dest + os.path.sep + file.name)


def _clear_dir(path: str):
    for f in os.listdir(path):
        _delete(f"{path}{os.path.sep}{f}")


def _delete(path: str):
    if os.path.isfile(path):
        os.remove(path)
    else:
        try:
            os.rmdir(path)
        except OSError:
            _clear_dir(path)
            _delete(path)
