from mdparser import markdown_to_html


def main():
    print(
        markdown_to_html(
            """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        )
    )


if __name__ == "__main__":
    main()
