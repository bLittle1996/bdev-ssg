from ssg import copy_dir, generate_pages


def main():
    copy_dir("./static", "./public")
    generate_pages("./template.html", "./content", "./public")


if __name__ == "__main__":
    main()
