import os
import re


def clean_text(text):
   
    text = re.sub(r'\(.*?\)', '', text, flags=re.DOTALL)  
    text = re.sub(r'\[.*?\]', '', text, flags=re.DOTALL)  
   
    text = text.replace('!', '').replace('?', '').replace('"', '').replace("'", '')
    return text


folder_path = 'testclean'


if not os.path.isdir(folder_path):
    print(f"The folder {folder_path} does not exist.")
    exit()


for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        print(f"Original content of {filename}:")
        print(text)
       
        cleaned_text = clean_text(text)
        
        print(f"Cleaned content of {filename}:")
        print(cleaned_text)
       
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

print("All text files have been cleaned.")
