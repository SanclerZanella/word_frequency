import os
import shutil
import sqlite3
from typing import List, Tuple

from app.processor.text_processor import TextProcessor
from app.storage.database_client import DatabaseClient
from app.storage.text_processor_dao import TextProcessorDAO
from app.utils.constants import OUTPUT_FOLDER, INPUT_FOLDER


class App:
    """
    Main application class for orchestrating CSV processing and database operations.
    """

    def start(self) -> None:
        """
        Main function to orchestrate the CSV processing and database operations.
        This function handles the entire process flow, including database setup,
        file processing, and result display.
        """
        conn = None
        try:
            # Create the database and establish a connection
            db = DatabaseClient()
            conn = db.create_database()
            dao = TextProcessorDAO(conn)
            text_processor = TextProcessor()

            self._setup_output_folder()
            self._process_csv_files(text_processor, dao)
            self._display_database_contents(conn)

        except Exception as e:
            print(f"An error occurred during processing: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
            print("Processing complete.")

    def _setup_output_folder(self) -> None:
        """
        Create the output folder if it doesn't exist.
        """
        try:
            if not os.path.exists(OUTPUT_FOLDER):
                os.makedirs(OUTPUT_FOLDER)
        except OSError as e:
            print(f"Error creating output folder: {e}")
            raise

    def _process_csv_files(self, text_processor: TextProcessor, dao: TextProcessorDAO) -> None:
        """
        Process each CSV file in the input folder and move processed files to the output folder.

        Args:
            text_processor (TextProcessor): Instance of TextProcessor for processing CSV files.
            dao (TextProcessorDAO): Data Access Object for database operations.
        """
        for filename in os.listdir(os.path.abspath(INPUT_FOLDER)):
            if filename.endswith('.csv'):
                file_path = os.path.join(os.path.abspath(INPUT_FOLDER), filename)
                try:
                    text_processor.process_csv_file(file_path, dao)
                    # Move processed file to the output folder
                    shutil.move(file_path, os.path.join(os.path.abspath(OUTPUT_FOLDER), filename))
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")

    def _display_database_contents(self, conn: sqlite3.Connection) -> None:
        """
        Display the contents of all tables in the database.

        Args:
            conn (sqlite3.Connection): Database connection object.
        """
        try:
            cursor = conn.cursor()
            tables = self._get_table_names(cursor)

            for table_name in tables:
                print(f"Items in table '{table_name}':")
                rows = self._get_table_contents(cursor, table_name)
                for row in rows:
                    print(row)
                print()  # Empty line for separation between tables

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    def _get_table_names(self, cursor: sqlite3.Cursor) -> List[str]:
        """
        Get names of all tables in the database.

        Args:
            cursor (sqlite3.Cursor): Database cursor object.

        Returns:
            List[str]: List of table names.
        """
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in cursor.fetchall()]

    def _get_table_contents(self, cursor: sqlite3.Cursor, table_name: str) -> List[Tuple]:
        """
        Get all rows from a specified table.

        Args:
            cursor (sqlite3.Cursor): Database cursor object.
            table_name (str): Name of the table to query.

        Returns:
            List[Tuple]: List of rows in the table.
        """
        cursor.execute(f"SELECT * FROM {table_name};")
        return cursor.fetchall()
