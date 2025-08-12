import os
import xmltodict

def parse_xml_files(folder: str = "data") -> dict:
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Folder '{folder}' not found.")

    parsed_data  = {}

    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)

        # Only process XML files
        if os.path.isfile(file_path) and file_name.lower().endswith(".xml"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    xml_data = f.read()
                    parsed = xmltodict.parse(xml_data)
                    first_key = next(iter(parsed))
                    parsed_data= parsed[first_key]
                    # parsed_data = data.get("AirFareSearchResponse", {})
            except Exception as e:
                print(f"Failed to parse : {e}")

    return parsed_data 

