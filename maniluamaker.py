import sys
import re
import os
from tkinter import simpledialog, Tk

def extract_ids_from_manifest(filename):
    numbers = re.findall(r'\d+', filename)
    if len(numbers) >= 2:
        return numbers[0], numbers[1]  # ID2, ID4
    else:
        raise ValueError("Manifest filename must contain at least two numeric IDs.")

def extract_id3_from_vdf(vdf_path, id2):
    with open(vdf_path, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = rf'{re.escape(id2)}.*?"DecryptionKey"\s*"(.*?)"'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Could not find DecryptionKey for ID2: {id2}")

def main():
    if len(sys.argv) != 3:
        print("Please drag and drop exactly 2 files: config.vdf and a .manifest file.")
        input("Press Enter to exit...")
        return

    vdf_file = ''
    manifest_file = ''
    for path in sys.argv[1:]:
        if path.endswith('.vdf'):
            vdf_file = path
        elif path.endswith('.manifest'):
            manifest_file = path

    if not vdf_file or not manifest_file:
        print("Both a .vdf and a .manifest file are required.")
        input("Press Enter to exit...")
        return

    # Get ID1 from user
    root = Tk()
    root.withdraw()
    id1 = simpledialog.askstring("Enter ID", "Enter the required ID (ID1):")
    if not id1:
        print("No ID entered. Exiting.")
        return

    try:
        id2, id4 = extract_ids_from_manifest(os.path.basename(manifest_file))
        id3 = extract_id3_from_vdf(vdf_file, id2)

        output = f"""addappid({id1})
addappid({id2},1,"{id3}")
setManifestid(({id2},"{id4}",0)"""

        output_filename = f"{id1}.lua"
        with open(output_filename, 'w', encoding='utf-8') as out_file:
            out_file.write(output)

        print(f"File '{output_filename}' has been created successfully.")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
