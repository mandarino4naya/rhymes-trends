from rhyme import Poem_func
import os
from keras.models import load_model
from network import Corpus, Network
from changeToABC import seqIdent
import json
if __name__ == '__main__':
    language = 'english'
    input_folder = 'testfolder/' 
    output_folder = 'result/'    
    output_file = 'seqdata.txt' 

   
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            name=os.path.splitext(filename)[0]
            

            poem = Poem_func(language, input_folder+filename, output_folder)
            patterns = seqIdent(poem)
            
            if os.path.exists(output_file):
                with open(output_file, 'r') as file:
                    try:
                        existing_data = json.load(file)
                    except json.JSONDecodeError:
                        existing_data = {}
            else:
                existing_data = {}
            if name in existing_data:
                existing_data[name].extend(patterns)
                
            else:
                existing_data[name] = patterns
            with open(output_file, 'w') as file:
                file.write(json.dumps(existing_data, indent=4))
            print(f"Results have been saved to {output_file}")

                         
                    

           
