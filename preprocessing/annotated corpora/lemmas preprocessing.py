import os
import csv
from pathlib import Path


def process_tsv_to_txt(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each TSV file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('_lemma_pos.tsv'):
            input_path = os.path.join(input_folder, filename)
            output_filename = filename.replace('_lemma_pos.tsv', '_lemmas.txt')
            output_path = os.path.join(output_folder, output_filename)
            
            lemmas = []
            total_count = 0
            kept_count = 0
            
            with open(input_path, 'r', encoding='utf-8') as tsvfile:
                reader = csv.reader(tsvfile, delimiter='\t')
                next(reader)  # Skip header row
                
                for row in reader:
                    total_count += 1
                    if len(row) < 2:
                        continue  # Skip malformed rows
                    
                    lemma, pos = row[0], row[1]
                    
                    # Apply rules
                    if pos in ['PUNCT', 'SYM', 'X']:
                        continue
                    elif pos == 'PRON':
                        lemmas.append('person1')
                    elif pos == 'PROPN':
                        lemmas.append('proper1')
                    elif pos == 'NUM':
                        lemmas.append('number1')
                    else:
                        lemmas.append(lemma)
                    
                    kept_count += 1
            
            # Save the output
            with open(output_path, 'w', encoding='utf-8') as txtfile:
                txtfile.write(' '.join(lemmas))
            
            print(f"✓ Processed {filename} (total: {total_count}, kept: {kept_count}, filtered: {total_count - kept_count})")


process_tsv_to_txt('ELTeC-lemma-pos', 'annotated corpora (lemmas)')
process_tsv_to_txt('IMP-lemma-pos', 'annotated corpora (lemmas)')
process_tsv_to_txt('Prilit-lemma-pos', 'annotated corpora (lemmas)')
process_tsv_to_txt('KDSP-lemma-pos', 'annotated corpora (lemmas)')
process_tsv_to_txt('maj68-lemma-pos', 'annotated corpora (lemmas)')


# Function to run after the folder is manually cleaned of duplicates
# Rename according to new prefix
def rename_lemma_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('_lemmas.txt'):
            file_path = Path(folder_path) / filename
            
            new_name = f"PREPROCESSED_{filename.replace('_lemmas', '')}"
            new_path = Path(folder_path) / new_name
            
            file_path.rename(new_path)


rename_lemma_files('annotated corpora (lemmas)')
