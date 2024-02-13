import json
import fitz  # PyMuPDF for reading PDF
from openai import AzureOpenAI

import logging

class OpenAIResumeParser:
    def __init__(self, openai_config, log=logging.getLogger()):
        self.log = log
        self.openai_config = openai_config

        # Configure OpenAI API
        # TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url=self.openai_config["OPENAI_API_BASE"])'
        # openai.api_base = self.openai_config["OPENAI_API_BASE"]
        self.client = AzureOpenAI(api_version=self.openai_config["OPENAI_API_VERSION"],
        api_key=self.openai_config["OPENAI_API_KEY"],azure_endpoint=self.openai_config["OPENAI_API_BASE"] )

    def pdf_to_text(self, pdf_path):
        """Reads the PDF file and returns the text in the PDF file."""
        text = ""
        try:
            doc = fitz.open(pdf_path)
            text = "".join([page.get_text() for page in doc])
            doc.close()
            return text
        except Exception as e:
            self.log.error(f"Failed to read PDF file at {pdf_path} with exception: {e}")
            return text

    def extract_details(self, text):
        """Takes the text from the PDF and returns key details in a JSON format."""
        
        if not text:
            self.log.error("No text found. Please read a PDF file first.")
            return None
        
        system_prompt = "You are an expert assistant designed to extract details from a resume. Users will paste in a string of text and you will respond with entities you've extracted from the text as a JSON object"
        user_prompt = "Summarize the text below into a JSON with exactly the following structure {education: [{school, degree, major, studied_from, studied_till,  gpa}], work_experience: [{job_title, company, location, duration, job_summary}], skills: [skill], total_years_of_experience}" + "\n" + text
        message_text = [{"role":"system","content":system_prompt},
                        {"role":"user","content":user_prompt}]

        completion = self.client.chat.completions.create(model=self.openai_config["OPENAI_API_ENGINE"],
        messages = message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

        assistant_response = completion.choices[0].message.content.strip()

        return self.parse_assistant_response(assistant_response)
    

    def parse_assistant_response(self, assistant_response):
        """Parses the assistant response and returns the JSON data."""
        try:
            json_data= json.loads(assistant_response)
            return json_data
        except Exception as e:
            self.log.error(f"Failed to save details to JSON file: {e}")
            return None
        
    def save_details_to_json(self, output_path, details):
        """Saves the extracted details in a JSON file."""
        try:
            with open(output_path, 'w') as json_file:
                json.dump(details, json_file, indent=4)
            return True
        except Exception as e:
            self.log.error(f"Failed to save details to JSON file: {e}")
            return False
