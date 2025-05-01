import json
from bs4 import BeautifulSoup
import os

def inject_code(html_file):
    # Load the translated HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Load the code to inject
    with open("before_head.json", 'r', encoding='utf-8') as f:
        head_code = json.load(f)

    with open("before_body.json", 'r', encoding='utf-8') as f:
        body_code = json.load(f)

    # Inject code into <head>
    if soup.head:
        for code in head_code:
            injected = BeautifulSoup(code, 'html.parser')
            soup.head.append(injected)

    # Inject code before </body>
    if soup.body:
        for code in body_code:
            injected = BeautifulSoup(code, 'html.parser')
            soup.body.append(injected)

    # Update internal links (no external or anchored references)
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

    # Save to originalname-fr.html
    base_name = os.path.splitext(os.path.basename(html_file))[0]
    if base_name.startswith("translated_output"):
        base_name = "index"
    output_file = f"{base_name}-fr.html"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"✅ Step 4 complete: injected code and updated internal links. Saved as {output_file}.")

# Run if script is called directly (GitHub Actions)
if __name__ == "__main__":
    inject_code("translated_output.html")
