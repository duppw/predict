import csv
from collections import defaultdict
import random
from pathlib import Path
from typing import Dict, List
import logging
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
import argparse
import sys


class MarkovChainGenerator:
    def __init__(self, epub_path: str, output_path: str):

        self.epub_path = Path(epub_path)
        self.output_path = Path(output_path)
        self.word_pairs: Dict[str, List[str]] = defaultdict(list)
        self.setup_logging()

    def setup_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('markov_chain.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def clean_text(self, text: str) -> str:
        punctuation = '".,()?!:“;[]{}\'\"'
        return text.translate(str.maketrans('', '', punctuation)).lower().strip()

    def process_epub(self) -> None:
        try:
            book = epub.read_epub(self.epub_path)
            logging.info(f"Processing EPUB file: {self.epub_path}")

            for item in book.get_items_of_type(ITEM_DOCUMENT):
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                for p in soup.find_all('p'):
                    text = self.clean_text(p.get_text())
                    words = text.split()

                    for i in range(len(words) - 1):
                        self.word_pairs[words[i]].append(words[i + 1])

            logging.info(f"Processed {len(self.word_pairs)} unique words.")

        except Exception as e:
            logging.error(f"Error processing EPUB: {e}")
            raise

    def save_word_pairs(self) -> None:
        try:
            with open(self.output_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['first', 'last'])
                for first_word, second_words in self.word_pairs.items():
                    for second_word in second_words:
                        writer.writerow([first_word, second_word])

            logging.info(f"Word pairs saved to: {self.output_path}")

        except Exception as e:
            logging.error(f"Error saving word pairs: {e}")
            raise

    def generate_text(self, start_word: str, length: int = 50) -> str:
        if start_word not in self.word_pairs:
            raise ValueError(f"Start word '{start_word}' not found in the word pairs")

        generated_words = [start_word]
        current_word = start_word

        try:
            for _ in range(length - 1):
                if current_word not in self.word_pairs:
                    break
                next_word = random.choice(self.word_pairs[current_word])
                generated_words.append(next_word)
                current_word = next_word

            return ' '.join(generated_words)

        except Exception as e:
            logging.error(f"Error generating text: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(description='Generate text using Markov chains from EPUB books.')
    parser.add_argument('epub_path', help='Path to the EPUB file.')
    parser.add_argument('output_path', help='Path to save the word pairs CSV.')
    parser.add_argument('--start-word', default='o', help='Word to start generation with.')
    parser.add_argument('--length', type=int, default=50, help='Number of words to generate.')

    args = parser.parse_args()

    try:
        generator = MarkovChainGenerator(args.epub_path, args.output_path)
        generator.process_epub()
        generator.save_word_pairs()

        generated_text = generator.generate_text(args.start_word, args.length)
        print("\nGenerated text:")
        print(generated_text)

    except Exception as e:
        logging.error(f"Program failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
