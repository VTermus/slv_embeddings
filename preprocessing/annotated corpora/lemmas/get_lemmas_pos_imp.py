import os
import xml.etree.ElementTree as ET
from pathlib import Path

# POS tag mapping (first letter to standardized tag)
POS_MAPPING = {
    'A': 'ADJ',
    'C': 'CCONJ',
    'I': 'INTJ',
    'M': 'NUM',
    'N': 'NOUN',
    'P': 'PRON',
    'Q': 'PART',
    'R': 'ADV',
    'S': 'ADP',
    'V': 'VERB',
    'X': 'X',
    'Y': 'PROPN'
}

def extract_pos(ana):
    """Extract POS tag from ana attribute and transform it"""
    if not ana:
        return ''
    # Get first character of the tag (before any hyphen or colon)
    first_char = ana.split(':')[-1][0] if ':' in ana else ana[0]
    return POS_MAPPING.get(first_char, 'X')  # Default to X if unknown

def is_inside_orig(elem):
    """Check if element is inside <orig> by manual tree traversal"""
    path = []
    while elem is not None:
        path.append(elem.tag)
        if 'orig' in elem.tag:
            return True
        elem = elem.find('..')  # Parent element alternative
    return False

def process_wikivir_file(xml_path, output_path):
    """Process a single file"""
    try:
        # Remove namespace declarations first
        with open(xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        xml_content = xml_content.replace('xmlns="http://www.tei-c.org/ns/1.0"', '')
        
        root = ET.fromstring(xml_content)
        lemmas = []
        # Store both original and transformed POS tags
        original_pos_tags = set()
        transformed_pos_tags = set()

        # Process all <w> elements
        for w in root.findall('.//w'):
            # Skip if inside <orig> when there's a <reg> alternative
            if is_inside_orig(w):
                continue
                
            lemma = w.get('lemma')
            ana = w.get('ana', '')
            original_pos = ana.split(':')[-1].split('-')[0] if ':' in ana else ana.split('-')[0]
            pos = extract_pos(ana)
            
            if lemma and pos:
                lemmas.append(f"{lemma}\t{pos}")
                original_pos_tags.add(original_pos)
                transformed_pos_tags.add(pos)

        # Process <reg> elements (preferred versions)
        for reg in root.findall('.//reg'):
            for w in reg.findall('w'):
                lemma = w.get('lemma')
                ana = w.get('ana', '')
                original_pos = ana.split(':')[-1].split('-')[0] if ':' in ana else ana.split('-')[0]
                pos = extract_pos(ana)
                
                if lemma and pos:
                    lemmas.append(f"{lemma}\t{pos}")
                    original_pos_tags.add(original_pos)
                    transformed_pos_tags.add(pos)

        # Write output
        if lemmas:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("Lemma\tPOS\n" + "\n".join(lemmas))
            print(f"✓ Processed {xml_path.name} ({len(lemmas)} lemmas)")
            return original_pos_tags, transformed_pos_tags
        else:
            print(f" No lemmas in {xml_path.name}")
            return set(), set()

    except Exception as e:
        print(f"✗ Error in {xml_path.name}: {str(e)}")
        return set(), set()

def process_wikivir_corpus(input_dir, output_dir):
    """Process all files of the corpus"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    all_original_pos = set()
    all_transformed_pos = set()
    processed = 0

    for xml_file in input_path.glob('*.xml'):
        out_file = output_path / f"{xml_file.stem}_lemma_pos.tsv"
        original_pos, transformed_pos = process_wikivir_file(xml_file, out_file)
        all_original_pos.update(original_pos)
        all_transformed_pos.update(transformed_pos)
        if original_pos:  # If we got any tags, count as processed
            processed += 1

    print(f"\nProcessed {processed} files")
    print("Unique original POS tags found:", ", ".join(sorted(all_original_pos)))
    print("Unique transformed POS tags:", ", ".join(sorted(all_transformed_pos)))


input_folder = "IMP-corpus-tei"
output_folder = "IMP-lemma-pos"
process_wikivir_corpus(input_folder, output_folder)

'''
import os
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_pos(ana):
    """Extract POS tag from ana attribute"""
    return ana.split('-')[0] if ana else ''

def is_inside_orig(elem):
    """Check if element is inside <orig> by manual tree traversal"""
    path = []
    while elem is not None:
        path.append(elem.tag)
        if 'orig' in elem.tag:
            return True
        elem = elem.find('..')  # Parent element alternative
    return False

def process_wikivir_file(xml_path, output_path):
    """Process a single file"""
    try:
        # Remove namespace declarations first
        with open(xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        xml_content = xml_content.replace('xmlns="http://www.tei-c.org/ns/1.0"', '')
        
        root = ET.fromstring(xml_content)
        lemmas = []
        # Store unique POS tags
        pos_tags = set()

        # Process all <w> elements
        for w in root.findall('.//w'):
            # Skip if inside <orig> when there's a <reg> alternative
            if is_inside_orig(w):
                continue
                
            lemma = w.get('lemma')
            pos = extract_pos(w.get('ana'))
            if lemma and pos:
                lemmas.append(f"{lemma}\t{pos}")
                pos_tags.add(pos)

        # Process <reg> elements (preferred versions)
        for reg in root.findall('.//reg'):
            for w in reg.findall('w'):
                lemma = w.get('lemma')
                pos = extract_pos(w.get('ana'))
                if lemma and pos:
                    lemmas.append(f"{lemma}\t{pos}")
                    pos_tags.add(pos)

        # Write output
        if lemmas:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("Lemma\tPOS\n" + "\n".join(lemmas))
            print(f"✓ Processed {xml_path.name} ({len(lemmas)} lemmas)")
            return pos_tags
        else:
            print(f" No lemmas in {xml_path.name}")
            return set()

    except Exception as e:
        print(f"✗ Error in {xml_path.name}: {str(e)}")
        return set()

def process_wikivir_corpus(input_dir, output_dir):
    """Process all files of the corpus"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    pos_tags = set()
    processed = 0

    for xml_file in input_path.glob('*.xml'):
        out_file = output_path / f"{xml_file.stem}_lemma_pos.tsv"
        file_pos = process_wikivir_file(xml_file, out_file)
        pos_tags.update(file_pos)
        if file_pos:
            processed += 1

    print(f"\nProcessed {processed} files")
    print("Unique POS tags found:", ", ".join(sorted(pos_tags)))


input_folder = "IMP-corpus-tei"
output_folder = "IMP-lemma-pos"
process_wikivir_corpus(input_folder, output_folder)
'''