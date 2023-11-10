import os
import argparse
import logging
import stanza
from stanza.utils.conll import CoNLL
import pandas as pd


class CorpusCreator:
    def __init__(self, corpus_dir, output_dir):
        self.corpus_dir = corpus_dir
        self.output_dir = output_dir
        self.nlp = stanza.Pipeline('ru', processors='tokenize, pos')
        self.errors = []

    def openfile(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError as e:
            logging.warning(f"File {filepath} has an encoding error: {e}")
            self.errors.append(filepath)
            return None
        except FileNotFoundError as e:
            logging.error(f"File {filepath} not found: {e}")
            self.errors.append(filepath)
            return None

    def parse(self, text):
        if text is None:
            return None
        else:
            doc = self.nlp(text)
            dicts = doc.to_dict()
            conllu = CoNLL.convert_dict(dicts)
            #conllu = ConllFormatter(doc, ext_names={'conll_pd': 'pandas'},
                 #               conversion_maps={'lemma': {'-PRON-': 'PRON'}})
            #nlp.add_pipe(conllformatter, after='parser')
            return conllu

    def writefile(self, filepath, conllu):
        output_filepath = os.path.join(self.output_dir, filepath)
        with open(output_filepath, 'w') as f:
            f.write(str(conllu))

    def process(self):
        if not os.path.exists(self.corpus_dir):
            logging.error(f"Corpus directory not found: {self.corpus_dir}")
            return

        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

        for root, dirs, files in os.walk(self.corpus_dir):
            for file in files:
                if ':' in file or '?' in file:
                    logging.warning(f"Invalid filename: {file}")
                    self.errors.append(os.path.join(root, file))
                    continue

                file_path = os.path.join(root, file)
                text = self.openfile(file_path)
                conllu = self.parse(text)
                
                if conllu is not None:
                    self.writefile(file, conllu)

        if self.errors:
            with open('errors.txt', 'w') as f:
                for error in self.errors:
                    f.write(f"{error}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process raw corpus files.')
    parser.add_argument('corpus_dir', type=str, help='Path to the corpus directory')
    parser.add_argument('output_dir', type=str, help='Name of the output directory')
    args = parser.parse_args()

    creator = CorpusCreator(args.corpus_dir, args.output_dir)
    creator.process()
