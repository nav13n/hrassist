import glob, os
from openai_resume_parser import OpenAIResumeParser
from dotenv import dotenv_values
import logging

def main(data_dir="./data"):

    openai_config = {
        **dotenv_values(".env"), 
        **os.environ,  # override loaded values with environment variables
    }

    #Example usage
    parser = OpenAIResumeParser(openai_config)

    glob_string = f"{data_dir}/**/*.pdf"
    print(glob_string)
    for filepath in glob.glob(glob_string, recursive=True):
        print(filepath)
        logging.info(f"Processing file: {filepath}")
        text = parser.pdf_to_text(pdf_path=filepath)
        details = parser.extract_details(text)
        output_path = os.path.splitext(filepath)[0] + ".json"
        parser.save_details_to_json(output_path, details)


__name__ = "__main__"


main()



