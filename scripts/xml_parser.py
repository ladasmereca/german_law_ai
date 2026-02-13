from bs4 import BeautifulSoup

def parse_xml(file_path):
    # 1. Open and read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    # 2. Initialize BeautifulSoup with the 'xml' parser
    soup = BeautifulSoup(file_content, 'xml')
    
    law_chunks = []

    # 3. Find all <norm> tags
    norms = soup.find_all('norm')
    
    for norm in norms:
        # Extract Paragraph Number (§) - located in <enbez>
        enbez = norm.find('enbez')
        
        # Extract Title - located in <titel>
        titel = norm.find('titel')
        
        # Extract the actual Text content - located in <Content>
        content = norm.find('Content')

        # Only process if it has a paragraph number and text
        if enbez and content:
            paragraph_id = enbez.get_text(strip=True)
            
            # Filter out non-law headers, only keep the ones starting with §
            if not paragraph_id.startswith('§'):
                continue
            
            paragraph_text = content.get_text(separator=" ", strip=True)
            
            # Skip empty or repeated paragraphs
            if "weggefallen" in paragraph_text.lower() and len(paragraph_text) < 50:
                continue

            title_text = titel.get_text(strip=True) if titel else "No Title"

            # Create the dictionary
            chunk = {
                "id": enbez.get_text(strip=True),
                "title": title_text,
                "text": paragraph_text,
                "source": "BGB"
            }

            law_chunks.append(chunk)

    return law_chunks

# Sanity check  
try:
    chunks = parse_xml('data/BGB.xml')
    print(f"Successfully parsed {len(chunks)} law sections.")
    print(f"Sample chunk: {chunks[123]}")
except FileNotFoundError:
    print("Error: Could not find the file at 'data/BGB.xml'. Check your folder structure!")
except Exception as e:
    print(f"An error occurred: {e}")