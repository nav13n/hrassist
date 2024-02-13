import unittest
from unittest.mock import patch, MagicMock
from hrassist.openai_resume_parser import OpenAIResumeParser
import json

class TestOpenAIResumeParser(unittest.TestCase):

    def setUp(self):
        self.openai_config = {
            "OPENAI_API_TYPE": "api",
            "OPENAI_API_BASE": "https://api.openai.com",
            "OPENAI_API_VERSION": "v1",
            "OPENAI_API_KEY": "test_api_key",
            "OPENAI_API_ENGINE": "text-davinci-003"
        }
        self.parser = OpenAIResumeParser(self.openai_config)

    @patch('fitz.open')  # Mocking fitz.open to avoid actual file IO
    def test_pdf_to_text(self, mock_fitz_open):
        mock_doc = MagicMock()
        mock_doc.__enter__.return_value.get_text.return_value = "Sample text"
        mock_fitz_open.return_value = mock_doc
        result = self.parser.pdf_to_text('dummy_path.pdf')
        self.assertEqual(result, "Sample text")
        mock_fitz_open.assert_called_once_with('dummy_path.pdf')

    @patch('openai.resources.chat.Completions.create')  # Mocking OpenAI API call
    def test_extract_details(self, mock_openai_chat_completion):
        mock_openai_response = {
            'choices': [{
                'message': {"content": json.dumps({"education": [], "work_experience": [], "skills": [], "total_years_of_experience": 0})}
            }]
        }
        mock_openai_chat_completion.return_value = mock_openai_response
        result = self.parser.extract_details("Sample text")
        self.assertIsInstance(result, dict)
        self.assertIn("education", result)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)  # Mocking built-in open function
    @patch('json.dump')  # Mocking json.dump to avoid actual file IO
    def test_save_details_to_json(self, mock_json_dump, mock_open):
        details = {"education": [], "work_experience": [], "skills": [], "total_years_of_experience": 0}
        result = self.parser.save_details_to_json('details.json', details)
        self.assertTrue(result)
        mock_open.assert_called_once_with('details.json', 'w')
        mock_json_dump.assert_called_once()

if __name__ == '__main__':
    unittest.main()
