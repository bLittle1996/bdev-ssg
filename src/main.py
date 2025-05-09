from ssg import copy_dir, generate_pages
import sys


def main():
    _script, *args = sys.argv
    base_path = args[0] if len(args) > 0 else "/"
    target_dir = args[1] if len(args) > 1 else "./public"
    print("Base path: ", base_path)
    print("Generated: ", target_dir)
    copy_dir("./static", target_dir)
    generate_pages("./template.html", "./content", target_dir, base_path=base_path)


if __name__ == "__main__":
    main()
