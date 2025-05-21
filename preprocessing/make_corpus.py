import os


allowed_tokens = {"person1", "proper1", "number1"}
slovenian_chars = set("abcčdefghijklmnoprsštuvzžABCČDEFGHIJKLMNOPRSŠTUVZŽ")  # Slovenian alphabet only


def is_valid_lemma(lemma):
    """Check if lemma is allowed token or Slovenian"""
    # Check for allowed special tokens
    if lemma in allowed_tokens:
        return True
    
    # Must contain only slovenian letters
    if not all(c in slovenian_chars for c in lemma.lower()):
        return False
    
    return True


def clean_file_content(content):
    """Remove invalid lemmas"""
    lemmas = content.split()
    cleaned_lemmas = [lemma for lemma in lemmas if is_valid_lemma(lemma)]
    return ' '.join(cleaned_lemmas)


def process_files(source_folder, corpus_file):
    """Process all files and build corpus with cleaned"""
    valid_files = 0
    cleaned_files = 0

    
    with open(corpus_file, 'w', encoding='utf-8') as corpus:
        for filename in os.listdir(source_folder):
            if not filename.endswith('.txt'):
                continue
                
            filepath = os.path.join(source_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read().strip()
            
            cleaned_content = clean_file_content(original_content)
            
            if cleaned_content:  # To be safe
                corpus.write(cleaned_content + '\n')
                if len(cleaned_content.split()) == len(original_content.split()):
                    valid_files += 1
                else:
                    cleaned_files += 1
                    print(f"Cleaned: {filename} (some lemmas removed)")
    

    print(f"{valid_files} completely valid files")
    print(f"{cleaned_files} files with some lemmas removed")
    print(f"Total: {valid_files + cleaned_files}")


process_files("annotated corpora + dglib", "slovenian_corpus.txt")


#Final corpus includes:
 #   - 663 completely valid files
  #  - 3660 files with some lemmas removed
   # Total lines in corpus: 4323