import re
from collections import OrderedDict
import json
import os

def extract_last_word_with_special_chars(line):
    
    match = re.search(r'([\[\(\{<][^\]\)\}\]>]*\w*[^\[\(\{<]*[\)\}\]>])$', line)
    if match:
        return match.group(1)
    return ''

def get_special_characters(segment):
    
    return ''.join(c for c in segment if not c.isalnum())

def process_block(lines):
    last_segments = [extract_last_word_with_special_chars(line) for line in lines if line.strip()]
    special_chars = [get_special_characters(segment) for segment in last_segments]
    
  
    unique_special_chars = list(OrderedDict.fromkeys(special_chars))
    char_to_letter = {char: chr(65 + i) for i, char in enumerate(unique_special_chars)}
    
    
    pattern = ''.join(char_to_letter.get(char, '?') for char in special_chars)
    
    return pattern

def seqIdent(input_file):
    print(input_file)
    with open(input_file, 'r') as file:
        content = file.read()
    
    # Split content into blocks based on empty lines
    raw_blocks = content.strip().split('\n\n')
    blocks = [block.splitlines() for block in raw_blocks if block.strip()]
    
    results = [process_block(block) for block in blocks]
    
    return results

