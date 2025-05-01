import json
from bs4 import BeautifulSoup
import os

def inject_code(html_file):
    # Load the translated HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Load the before_head.json and before_body.json
    # If the JSON files don't exist, the script will continue without injecting any code
    try:
        with open("before_head.json", 'r', encoding='utf-8') as f:
            head_code = json.load(f)
    except FileNotFoundError:
        head_code = []

    try:
        with open("before_body.json", 'r', encoding='utf-8') as f:
            body_code = json.load(f)
    except FileNotFoundError:
        body_code = []

    # Inject code into <head>
    head_tag = soup.head
    if head_tag:
        for code in head_code:
            tag = soup.new_tag('script')
            tag.string = code
            head_tag.append(tag)

    # Inject code before </body>
    body_tag = soup.body
    if body_tag:
        for code in body_code:
            tag = soup.new_tag('script')
            tag.string = code
            body_tag.append(tag)

    # Update internal links with "-fr"
for tag in soup.find_all(['a', 'form', 'link', 'script', 'img', 'iframe']):
    for attr in ['href', 'src', 'action']:
        if tag.has_attr(attr):
            url = tag[attr]
            if (
                url.endswith('.html') and
                not url.startswith(('http://', 'https://', 'ftp://', 'mailto:', 'tel:', '/', '#'))
            ):
                name, ext = os.path.splitext(url)
                tag[attr] = f"{name}-fr{ext}"
            elif '.html' in url and '#' in url:
                # Handle cases like "nok-terracottas.html#about-nok"
                base_url, fragment = url.split('#', 1)
                name, ext = os.path.splitext(base_url)
                tag[attr] = f"{name}-fr{ext}#{fragment}"
                
    # Save the modified HTML back to a file
    output_file = html_file.replace('.html', '-translated.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"✅ Step 4 complete: injected code and updated internal links. Saved as {output_file}.")

# Example usage (for testing purposes):
# inject_code('translated_output.html')
