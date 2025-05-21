import os
import xml.etree.ElementTree as ET
from pathlib import Path
import re

def clean_filename(text):
    """Clean text to make it safe for filenames"""
    # Remove special characters 
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text).strip()
    # Shorten if too long
    return text[:100]


def extract_metadata(xml_file):
    """Parse an XML file and extract the title and author of a book"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
        
        # Extract title and author
        title = root.find('.//tei:titleStmt/tei:title', ns).text
        author = root.find('.//tei:titleStmt/tei:author', ns).text
        
        # Clean the [KDSP.ana] suffix
        title = re.sub(r'\s*\[.*\]\s*', '', title)
        
        return title, author
    except Exception as e:
        print(f"Error processing {xml_file}: {e}")
        return None, None


def find_available_filename(base_path, ext, counter=1):
    """Find the first available filename by appending numbers"""
    candidate = f"{base_path}{ext}"
    if not Path(candidate).exists():
        return candidate
    return find_available_filename(f"{base_path}_{counter}", ext, counter + 1)


def rename_xml_files(xml_dir, txt_dir, file_pattern):
    """Rename all XML files in a folder using title and author"""
    if file_pattern == "KDSP":
        xml_files = sorted(f for f in Path(xml_dir).glob('*.ana.xml') 
                       if f.name.startswith('KDSP') and f.name.endswith('.ana.xml'))
        txt_ext = ".txt"
        xml_ext = ".ana.xml"
    elif file_pattern == "maj68":
        xml_files = sorted(f for f in Path(xml_dir).glob('maj68-*.xml') 
                       if f.name.startswith('maj68-') and f.name.endswith('.xml'))
        txt_ext = ".txt" 
        xml_ext = ".xml"
    else:
        raise ValueError("Unknown file pattern")
    
    
    for xml_file in xml_files:
        # Extract the base ID
        file_id = xml_file.stem  # for both patterns
        
        # Find matching txt file
        txt_file = Path(txt_dir) / f"{file_id}{txt_ext}"
 
        title, author = extract_metadata(xml_file)
        if not title and not author:
            continue
        
        # Create new filename
        clean_title = clean_filename(title)
        clean_author = clean_filename(author)
        base_name = f"{clean_title}_({clean_author})"

        new_xml_path = find_available_filename(Path(xml_dir) / base_name, xml_ext)
        new_txt_path = find_available_filename(Path(txt_dir) / base_name, txt_ext)
        
        # Rename files
        try:
            os.rename(xml_file, new_xml_path)
            os.rename(txt_file, new_txt_path)
            print(f"Renamed: {file_id} -> {Path(new_xml_path).stem}")
        except Exception as e:
            print(f"Error renaming {file_id}: {e}")


rename_xml_files("KDSP.TEI.ana", "KDSP.txt", file_pattern="KDSP")
rename_xml_files("maj68.TEI.ana", "maj68.txt", file_pattern="maj68")
