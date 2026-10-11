def read_text_file(file_path: str) -> str:

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    if not content.strip():
        raise ValueError("The input file is empty.")

    return content