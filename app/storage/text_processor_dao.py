from abc import ABC, abstractmethod
from collections import Counter
from sqlite3 import Connection, Error as SQLiteError


class TextProcessorDAOInterface(ABC):
    """
        Abstract base class defining the interface for text processing data access operations.
    """
    @abstractmethod
    def save_entry(self, entry_id: str, source: str, text: str) -> None:
        pass

    @abstractmethod
    def save_words_frequency(self, entry_id: str, word_freq: Counter) -> None:
        pass


class TextProcessorDAO(TextProcessorDAOInterface):
    """
        Concrete implementation of TextProcessorDAOInterface for SQLite database operations.
    """
    def __init__(self, db_client: Connection):
        """
            Initialize the DAO with a database connection.

            Args:
                db_client (Connection): SQLite database connection object.
        """
        self.__conn = db_client

    def save_entry(self, entry_id: str, source: str, text: str) -> None:
        """
            Save a text entry to the database.

            Args:
                entry_id (str): Unique identifier for the entry.
                source (str): Source of the text entry.
                text (str): The text content to be saved.

            Raises:
                SQLiteError: If there's an error in database operations.
        """
        c = None
        try:
            c = self.__conn.cursor()
            # Insert or replace the entry in the 'entries' table
            c.execute("INSERT OR REPLACE INTO entries VALUES (?, ?, ?)", (entry_id, source, text))
            self.__conn.commit()
        except SQLiteError as e:
            self.__conn.rollback()  # Rollback changes in case of error
            raise SQLiteError(f"Error saving entry: {e}")
        finally:
            if c:
                c.close()

    def save_words_frequency(self, entry_id: str, word_freq: Counter) -> None:
        """
            Save word frequencies for a given entry to the database.

            Args:
                entry_id (str): Unique identifier for the entry.
                word_freq (Counter): Counter object containing word frequencies.

            Raises:
                SQLiteError: If there's an error in database operations.
        """
        c = None
        try:
            c = self.__conn.cursor()
            # Insert word frequencies into the 'word_frequencies' table
            for word, freq in word_freq.items():
                c.execute("INSERT INTO word_frequencies VALUES (?, ?, ?)", (entry_id, word, freq))
            self.__conn.commit()
        except SQLiteError as e:
            self.__conn.rollback()  # Rollback changes in case of error
            raise SQLiteError(f"Error saving word frequencies: {e}")
        finally:
            if c:
                c.close()
