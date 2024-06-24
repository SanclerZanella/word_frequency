from abc import ABC, abstractmethod
from collections import Counter
from sqlite3 import Connection
import re
from app.storage.text_processor_dao import TextProcessorDAO
from app.utils.constants import COMMON_WORDS


class TextProcessorInterface(ABC):
    """Abstract base class defining the interface for text processing operations."""
    @abstractmethod
    def retrieve_csv_content(self, file_path: str) -> str:
        pass

    @abstractmethod
    def process_text(self, text: str) -> Counter:
        pass

    @abstractmethod
    def process_csv_file(self, file_path: str, conn: Connection) -> None:
        pass


class TextProcessor(TextProcessorInterface):
    """Concrete implementation of TextProcessorInterface."""
    def retrieve_csv_content(self, file_path: str) -> str:
        """
            Retrieve content from a CSV file.

            Args:
                file_path (str): Path to the CSV file.

            Returns:
                str: Content of the CSV file.

            Raises:
                FileNotFoundError: If the file is not found.
                IOError: If there's an error reading the file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        except IOError as e:
            raise IOError(f"Error reading CSV file: {e}")

    def process_text(self, text: str) -> Counter:
        """
            Process text to count word frequencies, excluding common words.

            Args:
                text (str): Text to process.

            Returns:
                Counter: Word frequencies.
        """
        # Remove numbers and emojis using regex
        text = re.sub(r'\d+(?:\.\d+)?', '', text)
        text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', '',
                      text)

        # Tokenize the text into words and count frequencies, excluding common words
        words = re.findall(r'\b\w+\b', text.lower())
        return Counter(word for word in words if word not in COMMON_WORDS)

    def process_csv_file(self, file_path: str, db_dao: TextProcessorDAO) -> None:
        """
            Process a CSV file and store its content in the database.

            Args:
                file_path (str): Path to the CSV file.
                db_dao (TextProcessorDAO): Data Access Object for database operations.

            Raises:
                FileNotFoundError: If the file is not found.
                IOError: If there's an error reading the file.
                ValueError: If there's an error processing the file content.
        """
        try:
            content = self.retrieve_csv_content(file_path)

            # Split the content into individual entries
            entries = re.split(r'\n(?=\d{7},)', content.strip())

            processed_entries = 0
            for entry in entries:
                try:
                    # Split each entry into its components: id, source, and text
                    parts = entry.split(',', 2)
                    if len(parts) != 3:
                        raise ValueError(f"Invalid entry format: {entry}")

                    entry_id, source, text = parts

                    # Remove extra whitespace and quotes
                    entry_id = entry_id.strip()
                    source = source.strip().strip('"')
                    text = text.strip().strip('"')

                    # Process the text and get word frequencies
                    word_freq = self.process_text(text)

                    # Insert or replace the entry in the 'entries' table
                    db_dao.save_entry(entry_id, source, text)

                    # Insert word frequencies into the 'word_frequencies' table
                    db_dao.save_words_frequency(entry_id, word_freq)

                    processed_entries += 1
                except ValueError as e:
                    print(f"Skipping invalid entry: {e}")
                except Exception as e:
                    print(f"Error processing entry: {e}")

            print(f"Successfully processed {processed_entries} out of {len(entries)} entries.")
        except (FileNotFoundError, IOError) as e:
            print(f"Error accessing file: {e}")
        except Exception as e:
            print(f"Unexpected error during CSV processing: {e}")

