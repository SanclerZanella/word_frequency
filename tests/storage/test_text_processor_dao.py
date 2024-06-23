import unittest
from unittest.mock import Mock, patch
from collections import Counter
from sqlite3 import Error as SQLiteError
from app.storage.text_processor_dao import TextProcessorDAO


class TestTextProcessorDAO(unittest.TestCase):

    def setUp(self):
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.dao = TextProcessorDAO(self.mock_connection)

    def test_save_entry_success(self):
        entry_id = "test_id"
        source = "test_source"
        text = "test text"

        self.dao.save_entry(entry_id, source, text)

        self.mock_cursor.execute.assert_called_once_with(
            "INSERT OR REPLACE INTO entries VALUES (?, ?, ?)",
            (entry_id, source, text)
        )
        self.mock_connection.commit.assert_called_once()
        self.mock_cursor.close.assert_called_once()

    def test_save_entry_error(self):
        self.mock_cursor.execute.side_effect = SQLiteError("Test error")

        with self.assertRaises(SQLiteError) as context:
            self.dao.save_entry("test_id", "test_source", "test text")

        self.assertIn("Error saving entry", str(context.exception))
        self.mock_connection.rollback.assert_called_once()
        self.mock_cursor.close.assert_called_once()

    def test_save_words_frequency_success(self):
        entry_id = "test_id"
        word_freq = Counter({"word1": 2, "word2": 1})

        self.dao.save_words_frequency(entry_id, word_freq)

        self.assertEqual(self.mock_cursor.execute.call_count, 2)
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO word_frequencies VALUES (?, ?, ?)",
            ("test_id", "word1", 2)
        )
        self.mock_cursor.execute.assert_any_call(
            "INSERT INTO word_frequencies VALUES (?, ?, ?)",
            ("test_id", "word2", 1)
        )
        self.mock_connection.commit.assert_called_once()
        self.mock_cursor.close.assert_called_once()

    def test_save_words_frequency_error(self):
        self.mock_cursor.execute.side_effect = SQLiteError("Test error")

        with self.assertRaises(SQLiteError) as context:
            self.dao.save_words_frequency("test_id", Counter({"word": 1}))

        self.assertIn("Error saving word frequencies", str(context.exception))
        self.mock_connection.rollback.assert_called_once()
        self.mock_cursor.close.assert_called_once()
