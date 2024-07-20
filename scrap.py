import requests
from bs4 import BeautifulSoup 

def extract_data(url, class_name=None, data_attr=None):
   
    response = requests.get(url)
    
   
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    
    soup = BeautifulSoup(response.content, 'html.parser')

    
    if class_name:
        elements = soup.find_all(class_=class_name)
    
    elif data_attr:
        elements = soup.find_all(attrs={data_attr: "true"})
    else:
        print("Either class_name or data_attr must be provided.")
        return

   
    for element in elements:
        print(element.get_text(strip=True))


url = "https://genius.com/Lana-del-rey-brooklyn-baby-lyrics"  
class_name = "Lyrics__Container-sc-1ynbvzw-1 kUgSbL"  
data_attr = "data-lyrics-container"  

extract_data(url, class_name=class_name, data_attr=data_attr)
