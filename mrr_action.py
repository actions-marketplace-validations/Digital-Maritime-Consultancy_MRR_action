import exiftool
import json
import os
import sys

def main(args):
    rootPath = args[1]
    baseUrl = args[2]
    if baseUrl.endswith("/"):
        baseUrl = baseUrl[:-1]

    extensionsToInclude = (".pdf", ".docx", ".odt")
    map = {}

    os.chdir(rootPath)
    with exiftool.ExifTool() as et:
        for root, _, files in os.walk("."):
            for f in files:
                if f.endswith(extensionsToInclude):
                    print(os.path.join(root, f))
                    metadata = et.get_metadata(os.path.join(root, f))
                    if "XMP:Subject" in metadata:
                        mrn = metadata["XMP:Subject"]
                    elif "Subject" in metadata:
                        mrn = metadata["Subject"]
                    elif "PDF:Subject" in metadata:
                        mrn = metadata["PDF:Subject"]
                    if mrn:
                        map[mrn] = f"{baseUrl}{os.path.join(root, f)[1:]}"
                elif f.endswith(".txt"):
                    mrn = f.replace("_", ":").replace(".txt", "")
                    map[mrn] = f"{baseUrl}{os.path.join(root, f)[1:]}"
                mrn = None
    print(json.dumps(map))

if __name__ == "__main__":
    main(sys.argv)