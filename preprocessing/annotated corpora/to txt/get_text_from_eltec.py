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


def parse_xml_file(file_path):
    """Parse an XML file and extract the text, title, and author of a book"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

        # Extract title and author from the header
        title_stmt = root.find('.//tei:titleStmt', ns)
        title = title_stmt.find('tei:title', ns).text if title_stmt is not None else "Unknown Title"
        author = title_stmt.find('tei:author', ns).text if title_stmt is not None else "Unknown Author"

        clean_title = clean_filename(title.split(':')[0]) # first part only
        clean_author = clean_filename(author)  

        # Find all paragraphs
        paragraphs = []
        for p in root.findall('.//tei:body//tei:p', ns):
            # Get all text content, including from child elements
            text = ''.join(p.itertext()).strip()
            if text:
                # Normalize whitespace (replace any whitespace sequence with single space)
                text = ' '.join(text.split())
                paragraphs.append(text)

        # Join paragraphs with consistent double newlines
        book_text = '\n\n'.join(paragraphs)

        return book_text, clean_title, clean_author

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except ET.ParseError as e:
        print(f"Error parsing XML file {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error processing {file_path}: {e}")
    return None, None, None


def iterate_files(input_folder, output_folder=None):
    """Process all files in a folder and save as .txt files with correct filename"""
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):
            file_path = os.path.join(input_folder, filename)
            book_text, title, author = parse_xml_file(file_path)

            if book_text is not None:
                output_filename = f"{title} ({author}).txt"
                output_path = os.path.join(output_folder or input_folder, output_filename)

                # For potential duplicate filenames
                counter = 1
                while os.path.exists(output_path):
                    output_filename = f"{title} ({author})_{counter}.txt"
                    output_path = os.path.join(output_folder or input_folder, output_filename)
                    counter += 1

                try:
                    with open(output_path, "w", encoding='utf-8') as f:
                        f.write(book_text)
                    print(f"Successfully saved: {output_path}")
                except IOError as e:
                    print(f"Error writing to {output_path}: {e}")


iterate_files('ELTeC-slv-2.0.0/level1', 'ELTeC-txt-2')