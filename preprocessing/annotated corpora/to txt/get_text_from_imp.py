import os
import xml.etree.ElementTree as ET
import re

def clean_filename(text):
    """Clean text to be safe for filenames"""
    # Remove invalid characters (including brackets and slashes)
    text = re.sub(r'[<>:"/\\|?*\[\]]', '', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text).strip()
    # Shorten if too long (Windows max path is 260 chars)
    return text[:100]


def parse_xml_file(file_path):
    """Parse an XML file and extract the text, title, and author of a book"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

        title_stmt = root.find('.//tei:titleStmt', ns)
        title = title_stmt.find('tei:title', ns).text.split(': ')[1] if title_stmt else "Unknown Title"
        author = title_stmt.find('tei:title', ns).text.split(': ')[0] if title_stmt else "Unknown Author"

        # Extract text with smart space handling
        text_parts = []
        
        for s in root.findall('.//tei:body//tei:s', ns):
            sentence_parts = []
            prev_was_punct = False
            
            for elem in s:
                # Get text content
                if elem.tag.endswith('choice'):
                    orig = elem.find('.//tei:orig/tei:w', ns)
                    text = orig.text if orig is not None else ""
                elif elem.tag.endswith('w'):
                    text = elem.text
                elif elem.tag.endswith('pc'):
                    text = elem.text
                    # Skip space if it's after/before punctuation
                    if prev_was_punct and text in ('«', '»', '"', "'"):
                        continue
                    prev_was_punct = True
                elif elem.tag.endswith('c') and elem.text == ' ':
                    # Only add space if not adjacent to punctuation
                    if not prev_was_punct:
                        text = ' '
                    else:
                        text = ''
                    prev_was_punct = False
                else:
                    text = ''
                
                if text:
                    sentence_parts.append(text)
            
            if sentence_parts:
                sentence = ''.join(sentence_parts).strip()
                text_parts.append(sentence)
        
        book_text = '\n\n'.join(text_parts)
        return book_text, title, author

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None, None


def iterate_files(input_folder, output_folder=None):
    """Process all files in a folder and save as .txt files with correct filename"""
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)  # exist_ok prevents race condition

    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):
            file_path = os.path.join(input_folder, filename)
            book_text, title, author = parse_xml_file(file_path)

            if book_text is not None:
                # Create safe filename
                output_filename = f"{title} ({author}).txt"
                output_filename = clean_filename(output_filename)  # Double-check cleaning
                output_path = os.path.join(output_folder or input_folder, output_filename)

                # Handle duplicates
                counter = 1
                while os.path.exists(output_path):
                    output_filename = f"{title} ({author})_{counter}.txt"
                    output_filename = clean_filename(output_filename)
                    output_path = os.path.join(output_folder or input_folder, output_filename)
                    counter += 1

                try:
                    with open(output_path, "w", encoding='utf-8') as f:
                        f.write(book_text)
                    print(f"Successfully saved: {output_filename}")
                except IOError as e:
                    print(f"Error writing to {output_filename}: {e}")

iterate_files('IMP-corpus-tei', 'IMP-txt')