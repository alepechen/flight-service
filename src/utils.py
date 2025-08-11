import os
import xmltodict

def parse_xml_files(folder: str = "data") -> dict:
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Folder '{folder}' not found.")

    parsed_files = {}

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)

        # Only process XML files
        if os.path.isfile(file_path) and file_name.lower().endswith(".xml"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    xml_data = f.read()
                    parsed_data = xmltodict.parse(xml_data)
                    parsed_files[file_name] = parsed_data
            except Exception as e:
                print(f"Failed to parse '{file_name}': {e}")

    return parsed_files

