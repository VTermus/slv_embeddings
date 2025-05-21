import os
import glob
import time
from tqdm import tqdm
import classla
import chardet
import re

# Initialize classla once 
classla.download('sl')  
nlp = classla.Pipeline('sl', processors='tokenize,lemma,pos')


def read_slovenian_file(file_path):
    """Read the file with encoding detection"""
    # Detect encoding
    with open(file_path, 'rb') as f:
        raw_data = f.read(50000)  # Check first 50KB
        encoding = chardet.detect(raw_data)['encoding']

    # Read with detected encoding (fallback to latin-1)
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            text = f.read()
    except:
        with open(file_path, 'r', encoding='latin-1') as f:
            text = f.read()

    # Clean common artifacts
    text = re.sub(r'[\x00-\x08\x0B-\x1F\x7F-\x9F]', ' ', text)  # Remove control chars
    return text.strip()


def prepare_slv_text(input_file, output_file):
    """Process a single Slovenian text file, saving lemmas with rules."""

    text = read_slovenian_file(input_file)
    doc = nlp(text)
    lemmas = []

    # Get lemma and pos within sentence context
    for sentence in doc.sentences:
        for word in sentence.words:
            pos = word.upos
            lemma = word.lemma

            # Apply rules
            if pos in {"PUNCT", "SYM", "X"}:
                continue
            elif pos == "PRON":
                lemma = "person1"
            elif pos == "PROPN":
                lemma = "proper1"
            elif pos == "NUM":
                lemma = "number1"

            lemmas.append(lemma)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(" ".join(lemmas))


def prepare_slv_texts_from_folder(input_folder, output_folder):
    """Process all .txt files in a folder, saving preprocessed versions."""
    os.makedirs(output_folder, exist_ok=True)
    files = sorted(glob.glob(os.path.join(input_folder, '*.txt')))  # Only .txt files

    start_time = time.time()
    for file in tqdm(files, desc="Processing files", unit="file"):
        filename = os.path.basename(file)
        output_file = os.path.join(output_folder, f"PREPROCESSED_{filename}")
        prepare_slv_text(file, output_file)
        # Delete the original file after successful processing
        os.remove(file)

    print(f"\nTotal time: {time.time() - start_time:.2f} seconds")


prepare_slv_texts_from_folder("texts", "lemmatized")