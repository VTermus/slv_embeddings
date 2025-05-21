import os
import xml.etree.ElementTree as ET
import re


def clean_filename(text):
    """Clean text to be safe for filenames"""
    # Remove invalid characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text).strip()
    # Shorten if too long
    return text[:100]


def extract_metadata(file_path):
    """Parse an XML file and extract the title and author of a book"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

        # Extract title and author from the header
        title_stmt = root.find('.//tei:titleStmt', ns)
        title = title_stmt.find('tei:title', ns).text if title_stmt is not None else "Unknown Title"
        author = title_stmt.find('tei:author', ns).text if title_stmt is not None else "Unknown Author"

        clean_title = clean_filename(title.split(':')[0])  # first part only
        clean_author = clean_filename(author)  

        return clean_title, clean_author

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except ET.ParseError as e:
        print(f"Error parsing XML file {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error processing {file_path}: {e}")
    return None, None


def rename_xml_files(input_folder):
    """Rename all XML files in a folder using title and author"""
    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):
            file_path = os.path.join(input_folder, filename)
            title, author = extract_metadata(file_path)

            if title is not None and author is not None:
                new_filename = f"{title} ({author}).xml"
                new_path = os.path.join(input_folder, new_filename)

                # For potential duplicate filenames
                counter = 1
                while os.path.exists(new_path):
                    new_filename = f"{title} ({author})_{counter}.xml"
                    new_path = os.path.join(input_folder, new_filename)
                    counter += 1

                try:
                    os.rename(file_path, new_path)
                    print(f"Successfully renamed: {filename} -> {new_filename}")
                except IOError as e:
                    print(f"Error renaming {filename}: {e}")


rename_xml_files('ELTeC-slv-2.0.0/level2')
