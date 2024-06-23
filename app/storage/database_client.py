import sqlite3
from abc import abstractmethod, ABC
from sqlite3 import Connection
from app.utils.constants import DATABASE_NAME


# Abstract base class defining the interface for database operations
class DatabaseClientInterface(ABC):
    @abstractmethod
    def create_database(self) -> Connection:
        pass


class DatabaseClient(DatabaseClientInterface):
    """ Concrete implementation of the DatabaseClientInterface """
    def create_database(self) -> Connection:
        """
            Create and set up the SQLite database with necessary tables.

            Returns:
            sqlite3.Connection: A connection object to the created database.

            Raises:
            sqlite3.Error: If there's an error in database operations.
        """
        conn = None
        try:
            # Establish a connection to the SQLite database
            conn = sqlite3.connect(DATABASE_NAME)

            # Create a cursor object to execute SQL commands
            c = conn.cursor()

            # Create 'entries' table to store original text entries
            # This table will have the following columns:
            # - id: TEXT, primary key for unique identification
            # - source: TEXT, to store the source of the entry
            # - original_text: TEXT, to store the original text content
            c.execute('''CREATE TABLE IF NOT EXISTS entries
                             (id TEXT PRIMARY KEY, source TEXT, original_text TEXT)''')

            # Create 'word_frequencies' table to store word frequency data
            # This table will have the following columns:
            # - id: TEXT, foreign key referencing entries(id)
            # - word: TEXT, to store individual words
            # - frequency: INTEGER, to store the frequency count of each word
            c.execute('''CREATE TABLE IF NOT EXISTS word_frequencies
                             (id TEXT, word TEXT, frequency INTEGER)''')

            # Commit the changes to the database and return the database connection
            conn.commit()
            return conn

        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise sqlite3.Error(f"An error occurred: {e}")
