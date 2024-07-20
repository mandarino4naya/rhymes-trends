import requests
from bs4 import BeautifulSoup

def extract_data(url, class_name=None, data_attr=None, output_file='output.txt'):
   
    try:
        response = requests.get(url)
        response.raise_for_status()  
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return

    
    soup = BeautifulSoup(response.content, 'html.parser')

   
    if class_name:
        elements = soup.find_all(class_=class_name)
    
    elif data_attr:
        elements = soup.find_all(attrs={data_attr: "true"})
    else:
        print("Either class_name or data_attr must be provided.")
        return

   
    if not elements:
        print("No elements found with the specified class or data attribute.")
        return


    try:
        with open(output_file, 'w', encoding='utf-8') as file:
           
            for element in elements:
                text = element.get_text(separator='\n', strip=True)
                file.write(text + '\n\n')  
        print(f"Data has been saved to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")


url = "https://genius.com/Lana-del-rey-brooklyn-baby-lyrics"
class_name = "Lyrics__Container-sc-1ynbvzw-1 kUgSbL"  
data_attr = "data-lyrics-container"  
extract_data(url, class_name=class_name)
