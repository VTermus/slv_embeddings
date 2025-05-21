import os
import glob
import time
from tqdm import tqdm
import classla
import chardet
import re

# Initialize classla once
classla.download('sl', verbose=False) 
# Pipeline configs with batched processing 
nlp = classla.Pipeline('sl', processors='tokenize,lemma,pos', 
                      use_gpu=False,
                      tokenize_batch_size=1000,
                      lemma_batch_size=1000,
                      pos_batch_size=1000)


def read_slovenian_file(file_path):
    """Optimized file reader with encoding detection"""
    # Encodings used for Slovenian
    encodings = ['utf-8', 'windows-1250', 'latin-1']
    try:
        # Detect encoding
        with open(file_path, 'rb') as f:
            raw = f.read(50000) # Check first 50KB
            detected = chardet.detect(raw)['encoding']
            if detected: encodings.insert(0, detected)
            
        for enc in encodings:
            # Read with detected encoding
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    text = f.read()
                return re.sub(r'[\x00-\x08\x0B-\x1F\x7F-\x9F]', ' ', text).strip()
            except:
                continue
        return raw.decode('ascii', errors='replace').strip()
    
    except Exception as e:
        print(f"Read error {file_path}: {str(e)}")
        return ""


def process_file(input_file, output_folder):
    """Process single file using global nlp pipeline"""
    try:
        text = read_slovenian_file(input_file)
        if not text.strip():
            return False
            
        doc = nlp(text)
        lemmas = []
        
        # Get lemma and pos within sentence context
        for sentence in doc.sentences:
            for word in sentence.words:
                pos = word.upos
                lemma = word.lemma

                # Apply rules
                if pos in {"PUNCT", "SYM", "X"}: continue
                lemma = {
                    "PRON": "person1",
                    "PROPN": "proper1",
                    "NUM": "number1"
                }.get(pos, lemma)
                lemmas.append(lemma)
        
        output_file = os.path.join(output_folder, f"PREPROCESSED_{os.path.basename(input_file)}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(" ".join(lemmas))
            
        return True
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")
        return False


def process_files_sequential(files, output_folder):
    """Process files sequentially with progress bar"""
    success = 0
    for file in tqdm(files, desc="Processing"):
        if process_file(file, output_folder):
            success += 1
            os.remove(file)  # Only remove if successful
    return success


def prepare_slv_texts_from_folder(input_folder, output_folder):
    """Main processing function"""
    os.makedirs(output_folder, exist_ok=True)
    files = sorted(glob.glob(os.path.join(input_folder, '*.txt'))) # Only .txt files
    print(f"Found {len(files)} files to process")
    
    start_time = time.time()
    success = process_files_sequential(files, output_folder)
    
    print(f"\nProcessed {success}/{len(files)} files successfully")
    print(f"Time taken: {(time.time()-start_time)/60:.1f} minutes")


prepare_slv_texts_from_folder("texts", "lemmatized")