import csv

def load_rare_words(rare_words_file):
    """Get rare words from TSV file"""
    rare_words = set()
    with open(rare_words_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)  # Skip header 
        for row in reader:
            rare_words.add(row[0])  # Add the lemma (first column)
    return rare_words


def filter_corpus(input_file, output_file, rare_words):
    """Filter rare words from the corpus"""
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            words = line.strip().split()
            # Keep lemma only if not in rare
            filtered_words = [word for word in words if word not in rare_words]
            outfile.write(' '.join(filtered_words) + '\n')


def process_corpus(rare_words_file, input_corpus_file, output_corpus_file):
    rare_words = load_rare_words(rare_words_file)
    print(f"Loaded {len(rare_words)} rare words")
    
    filter_corpus(input_corpus_file, output_corpus_file, rare_words)
    


process_corpus('rare_words.tsv', 'slovenian_corpus.txt', 'filtered_slovenian_corpus.txt')