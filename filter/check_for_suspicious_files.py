import os
import shutil


allowed_tokens = {"person1", "proper1", "number1"}
slovenian_chars = set("abcčdefghijklmnoprsštuvzž")  


def is_valid_lemma(lemma):
    """Check if lemma is either an allowed token or pure Slovenian"""
    # Check for allowed special tokens
    if lemma in allowed_tokens:
        return True
    
    # Must contain only slovenian letters
    if not all(c in slovenian_chars for c in lemma.lower()):
        return False
    
    return True


def check_file(filepath):
    """Check for suspicious lemmas and calculate invalid ratio"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    lemmas = [lem for lem in content.split() if lem]

    total_lemmas = len(lemmas)
    suspicious_lemmas = set()

    for lemma in lemmas:
        if not is_valid_lemma(lemma):
            suspicious_lemmas.add(lemma)
    
    invalid_ratio = len(suspicious_lemmas) / total_lemmas if total_lemmas > 0 else 0
    return suspicious_lemmas, invalid_ratio, total_lemmas


def process_files(source_folder, very_susp_folder, susp_folder, non_susp_folder):
    """Process all files and distribute to folders for further manual cleaning"""
    os.makedirs(very_susp_folder, exist_ok=True)
    os.makedirs(susp_folder, exist_ok=True)
    os.makedirs(non_susp_folder, exist_ok=True)
    
    for filename in os.listdir(source_folder):
        if not filename.endswith('.txt'):
            continue
            
        filepath = os.path.join(source_folder, filename)
        output_name = filename[len("preprocessed_"):] 
        
        suspicious, ratio, total = check_file(filepath)
        
        #print(f"{output_name}: {len(suspicious)}/{total} invalid ({ratio:.1%})")
        
        if ratio > 0.03:  # More than 3% invalid
            dest = os.path.join(very_susp_folder, output_name)
            print(f"very suspicious: {output_name} - {ratio:.1%} invalid")
            shutil.move(filepath, dest)
        
        elif suspicious:
            dest = os.path.join(susp_folder, output_name)
            print(f"suspicious: {output_name} - {', '.join(sorted(suspicious)[:30])}")
            shutil.move(filepath, dest)
        else:
            # For non-suspicious
            dest = os.path.join(non_susp_folder, output_name)
            shutil.move(filepath, dest)
            

process_files("lemmatized", "very suspicious", "suspicious", "non_suspicious")