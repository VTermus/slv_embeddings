import os
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_pos(msd_attr):
    """Extract POS tag from msd attribute (UposTag value)"""
    if not msd_attr:
        return ''
    # Get the UposTag value (e.g., "NOUN" from "UposTag=NOUN|Case=Nom...")
    for part in msd_attr.split('|'):
        if part.startswith('UposTag='):
            return part[8:]  # Return everything after 'UposTag='
    return ''

def process_mte_file(xml_file, output_file):
    """Process a single file"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        lemmas = []
        # Store unique POS tags
        pos_tags = set()

        # Process all word elements
        for w in root.findall('.//{http://www.tei-c.org/ns/1.0}w'):
            lemma = w.get('lemma')
            msd = w.get('msd', '')
            pos = extract_pos(msd)
            
            if lemma and pos:
                lemmas.append(f"{lemma}\t{pos}")
                pos_tags.add(pos)

        if lemmas:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Lemma\tPOS\n" + "\n".join(lemmas))
            print(f"✓ Processed {xml_file.name} ({len(lemmas)} lemmas)")
            return pos_tags
        else:
            print(f"No lemmas in {xml_file.name}")
            return set()
            
    except Exception as e:
        print(f"Error processing {xml_file.name}: {str(e)}")
        return set()

def process_mte_corpus(input_dir, output_dir):
    """Process all files of the corpus"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    pos_tags = set()
    processed = 0

    for xml_file in input_path.glob('*.xml'):
        out_file = output_path / f"{xml_file.stem}_lemma_pos.tsv"
        file_pos = process_mte_file(xml_file, out_file)
        pos_tags.update(file_pos)
        if file_pos:
            processed += 1

    print(f"\nProcessed {processed} files")
    print("Unique POS tags found:", ", ".join(sorted(pos_tags)))


input_folder = "Prilit.ana"
output_folder = "Prilit-lemma-pos"
process_mte_corpus(input_folder, output_folder)

