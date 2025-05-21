import os
import xml.etree.ElementTree as ET
from pathlib import Path

def process_xml_files(input_folder, output_folder):
    """Process all files extracting lemmas and POS tags"""
    processed_files = 0
    total_lemmas = 0
    # Store unique POS tags
    pos_tags = set()

    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    for xml_file in Path(input_folder).rglob('*.xml'):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            lemmas = []
            
            for elem in root.iter():
                tag = elem.tag.split('}')[-1]  # Remove namespace if present
            
            # Get all <w> elements
                if tag == 'w':
                    lemma = elem.get('lemma', '').strip()
                    pos = elem.get('pos', '').strip()
                    
                    if lemma and pos:
                        lemmas.append(f"{lemma}\t{pos}")
                        pos_tags.add(pos)
            
            if lemmas:
                output_file = output_path / f"{xml_file.stem}_lemma_pos.tsv"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("Lemma\tPOS\n" + "\n".join(lemmas))
                
                processed_files += 1
                total_lemmas += len(lemmas)
                print(f"✓ Processed {xml_file.name} ({len(lemmas)} lemmas)")
                
        except Exception as e:
            print(f"✗ Error processing {xml_file.name}: {str(e)}")


    print(f"Processed {processed_files} files")
    print("Unique POS tags found:", ", ".join(sorted(pos_tags)))
    print(f"Total lemmas extracted: {total_lemmas}")


input_folder = "ELTeC-slv-2.0.0/level2"
output_folder = "ELTeC-lemma-pos"
process_xml_files(input_folder, output_folder)

