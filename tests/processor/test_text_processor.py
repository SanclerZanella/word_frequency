import unittest
from collections import Counter
from unittest.mock import mock_open, MagicMock

from app.processor.text_processor import TextProcessor


class MockTextProcessorDAO:
    def save_entry(self, entry_id, source, text):
        pass

    def save_words_frequency(self, entry_id, word_freq):
        pass


class TestTextProcessor(unittest.TestCase):

    def test_retrieve_csv_content_file_found(self):
        file_content = "id,source,text\n1,source1,hello world\n2,source2,another text"
        mock_open_func = mock_open(read_data=file_content)
        with unittest.mock.patch('builtins.open', mock_open_func):
            processor = TextProcessor()
            content = processor.retrieve_csv_content('test.csv')
            self.assertEqual(content, file_content)

    def test_retrieve_csv_content_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            processor = TextProcessor()
            processor.retrieve_csv_content('nonexistent.csv')

    def test_retrieve_csv_content_io_error(self):
        with unittest.mock.patch('builtins.open', side_effect=IOError):
            with self.assertRaises(IOError):
                processor = TextProcessor()
                processor.retrieve_csv_content('test.csv')

    def test_process_text_basic(self):
        processor = TextProcessor()
        text = "Hello world! This is a test text. Hello again."
        expected_counter = Counter({'hello': 2, 'world': 1, 'test': 1, 'text': 1})
        result_counter = processor.process_text(text)
        self.assertEqual(result_counter, expected_counter)


if __name__ == '__main__':
    unittest.main()
