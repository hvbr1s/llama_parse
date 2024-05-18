import os
import markdown2
from bs4 import BeautifulSoup

def markdown_to_html(md_content):
    """Convert markdown content to HTML using markdown2."""
    return markdown2.markdown(md_content)

def extract_title(md_content):
    """Simple extraction of the first heading as title."""
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.strip('# ').strip()
    return "No Title Found"

def embed_metadata(html_content, url, title, text):
    """Embed metadata into HTML using BeautifulSoup."""
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup.html is None:
        # Create html and body tags if they don't exist
        html_tag = soup.new_tag('html')
        body_tag = soup.new_tag('body')
        html_tag.append(body_tag)
        soup.append(html_tag)
        # Move the content into the body tag
        body_tag.append(BeautifulSoup(html_content, 'html.parser'))

    head = soup.new_tag('head')
    soup.html.insert(0, head)
    meta_url = soup.new_tag('meta', attrs={"name": "url", "content": url})
    meta_title = soup.new_tag('meta', attrs={"name": "title", "content": title})
    meta_text = soup.new_tag('meta', attrs={"name": "text", "content": text})
    soup.head.append(meta_url)
    soup.head.append(meta_title)
    soup.head.append(meta_text)
    return str(soup)

def process_markdown_files(base_path, output_dir):
    """Process all markdown files found in the directory tree rooted at base_path."""
    os.makedirs(output_dir, exist_ok=True)
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()

                html_content = markdown_to_html(md_content)
                title = extract_title(md_content)
                url = "https://github.com/Certora/Documentation/blob/master/" + os.path.relpath(file_path, start=base_path).replace('\\', '/')
                text = BeautifulSoup(html_content, 'html.parser').get_text()[:200]  # Extract the first 200 characters of text

                final_html = embed_metadata(html_content, url, title, text)
                output_file_path = os.path.join(output_dir, file.replace('.md', '.html'))
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(final_html)

                print(f"Processed {file} to {output_file_path}")

def main():
    base_path = '/home/dan/certorabot/pinecone_pipeline/update_scripts/github_docs/Documentation/docs'
    output_dir = 'html_output'
    process_markdown_files(base_path, output_dir)

if __name__ == "__main__":
    main()
