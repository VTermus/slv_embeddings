import os
from collections import Counter
import matplotlib.pyplot as plt


def analyze_corpus(corpus_path, output_dir, rare_threshold=2):
    """Analyze corpus with 4,323 texts, optimized for medium-sized collections"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Load and count all words
    with open(corpus_path, 'r', encoding='utf-8') as f:
        texts = [line.strip().split() for line in f]
    
    word_counts = Counter()
    doc_frequency = Counter()  # How many texts contain each word
    
    for words in texts:
        word_counts.update(words)
        doc_frequency.update(set(words))  # once per text
    
    total_words = sum(word_counts.values())
    unique_words = len(word_counts)
    
    print(f"Analyzed {len(texts):,} texts")
    print(f"Total words: {total_words:,}")
    print(f"Unique words: {unique_words:,}")
    
    # Save complete frequencies
    with open(os.path.join(output_dir, 'word_stats.tsv'), 'w', encoding='utf-8') as f:
        f.write("word\tcount\tdocument_frequency\n")
        for word, count in word_counts.most_common():
            f.write(f"{word}\t{count}\t{doc_frequency[word]}\n")
    
    # Identify rare words (appearing in <= rare_threshold texts)
    rare_words = {word: (count, doc_frequency[word]) 
                 for word, count in word_counts.items() 
                 if doc_frequency[word] <= rare_threshold}
    
    print(f"Found {len(rare_words):,} rare words (in <= {rare_threshold} texts)")
    

    with open(os.path.join(output_dir, 'rare_words_1.tsv'), 'w', encoding='utf-8') as f:
        f.write("word\tcount\tdocument_frequency\n")
        for word, (count, df) in sorted(rare_words.items(), key=lambda x: (x[1][1], x[1][0])):
            f.write(f"{word}\t{count}\t{df}\n")
    

    # Frequency distribution plot
    plt.figure(figsize=(12, 6))
    plt.hist(word_counts.values(), bins=50, log=True)
    plt.title('Word Frequency Distribution (Log Scale)')
    plt.xlabel('Frequency')
    plt.ylabel('Number of Words')
    plt.savefig(os.path.join(output_dir, 'frequency_distribution.png'))
    plt.close()

    return word_counts, doc_frequency


word_counts, doc_freq = analyze_corpus("slovenian_corpus.txt", "corpus_analysis", rare_threshold=2)
