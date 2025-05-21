import xml.etree.ElementTree as ET
from pathlib import Path

def extract_pos(msd):
    """Extract the UPosTag value from msd attribute"""
    if not msd:
        return ''
    parts = msd.split('|')
    for part in parts:
        if part.startswith('UPosTag='):
            return part[8:]  # Get text after 'UPosTag='
    return ''

def process_file(xml_file, output_file):
    """Process a single file"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        lemmas = []
        # Store unique POS tags
        pos_tags = set()

        for w in root.findall('.//{http://www.tei-c.org/ns/1.0}w'):
            lemma = w.get('lemma')
            pos = extract_pos(w.get('msd', ''))
            if lemma and pos:
                lemmas.append(f"{lemma}\t{pos}")
                pos_tags.add(pos)

        if lemmas:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Lemma\tPOS\n" + "\n".join(lemmas))
            print(f"✓ Processed {xml_file.name} ({len(lemmas)} lemmas)")
            return pos_tags
        return set()

    except Exception as e:
        print(f"Error in {xml_file.name}: {str(e)}")
        return set()

def process_corpus(input_dir, output_dir):
    """Process all files of the corpus"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    pos_tags = set()
    processed = 0

    for xml_file in input_path.glob('*.xml'):
        out_file = output_path / f"{xml_file.stem}_lemma_pos.tsv"
        file_pos = process_file(xml_file, out_file)
        pos_tags.update(file_pos)
        if file_pos:
            processed += 1

    print(f"\nProcessed {processed} files")
    print("Unique POS tags:", ", ".join(sorted(pos_tags)))


input_folder = "KDSP.TEI.ana"
output_folder = "KDSP-lemma-pos"
process_corpus(input_folder, output_folder)

input_folder = "maj68.TEI.ana"
output_folder = "maj68-lemma-pos"
process_corpus(input_folder, output_folder)