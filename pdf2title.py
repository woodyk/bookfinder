#!/usr/bin/env python3
#
# tt.py

import os
import re
import sys
import textract
import magic
import shutil

def is_pdf(file_path):
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)
    return mime_type == 'application/pdf'

def rename_pdf(pdf_file_path):
    # Rename the file to /tmp/tmp.pdf
    tmp_file_path = '/tmp/tmp.pdf'
    shutil.move(pdf_file_path, tmp_file_path)

    try:
        # Extract the first two lines of the PDF file
        text = textract.process(tmp_file_path).decode('utf-8')
        first_two_lines = text.split('\n')[:2]

        # Replace non-alphanumeric characters with nothing and join the two lines
        new_name = '_'.join(re.sub(r'\W+', '', line) for line in first_two_lines)
        # Add .pdf extension
        new_name += '.pdf'

        # Get the directory of the original file
        directory = os.path.dirname(pdf_file_path)
        # Create the new file path
        new_file_path = os.path.join(directory, new_name)

        # Rename the file
        shutil.move(tmp_file_path, new_file_path)

        print(f"{pdf_file_path}, {new_file_path}")
    except Exception as e:
        print(f"{pdf_file_path} failed")
        # Move the failed file to a 'failed' directory
        failed_dir = os.path.join(os.path.dirname(pdf_file_path), 'failed')
        os.makedirs(failed_dir, exist_ok=True)
        shutil.move(pdf_file_path, os.path.join(failed_dir, os.path.basename(pdf_file_path)))

def crawl_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_pdf(file_path):
                rename_pdf(file_path)

# Usage
if len(sys.argv) != 2:
    print("Usage: python script.py <directory_path>")
else:
    crawl_directory(sys.argv[1])
