# Slovenian Embeddings

This repository contains code for building the  corpus and embedding of literary Slovenian based on two architectures:

- CBOW (word2vec) 
- SVD (tf-idf) 

## Text sources
Embeddings are trained on literary texts from:
1. [Digital Library of Slovenia]([url](https://www.dlib.si)) (dLib)
2. Five linguistically annotated corpora:
   - [ELTeC-slv (100 romanov)]([url](https://doi.org/10.5281/zenodo.4662600))
   - [PriLit (starejša pripovedna proza)]([url](http://hdl.handle.net/11356/1319))
   - [IMP (starejša besedila)]([url](http://hdl.handle.net/11356/1031))
   - [Maj68 (Maj 1968 v literaturi)]([url](http://hdl.handle.net/11356/1491))
   - [KDSP (longer narrative slovenian prose)
]([url](https://www.clarin.si/repository/xmlui/handle/11356/1823))


## Preprocessing

### Annotated corpora

``get_text_from_eltec.py``, ``get_text_from_imp.py`` → get .txt files with plain texts extracted out of TEI formats (for corpora without available .txt version)
``get_titles_from_eltec_imp.py``, ``get_titles_from_imp.py``, ``get_titles_from_kdsp_maj68.py`` → extract title and author from annotated files and rename texts (for corpora with unclear filenames)
``get_lemmas_pos_eltec.py``, ``get_lemmas_pos_imp.py``, ``get_lemmas_pos_prilit.py``, ``get_lemmas_pos_kdsp_maj68.py`` → extract lemmas and POS tags for each token of the text specific to each corpus format to .tsv files
``lemmas_preprocessing.py`` → process all files and get .txt with clean lemmas of specific POS according to our rules for each file

### DLib corpus

``crawler_slovenian.ipynb`` → download texts from digital library
``lemmatize.py`` → preprocess all files an (used for large files)
``lemmatize.optimized.py`` – optimized version with batched sequential processing for better memory management and error handling (used for the rest) 

``make_corpus.py`` → additional checks (after some manual cleaning) and combining all preprocessed files in a single .txt file with each text per line


## Filter

``frequency_analysis.py``, ``filter_corpus_by_frequency.py``, ``check_for_suspicious_files`` → corpus filtration to keep only Slovenian  
``word_stats.tsv``, ``rare_words.tsv``, ``word_stats.tsv`` → statistics for the words of the corpora used for filtration
