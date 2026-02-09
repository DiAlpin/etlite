
import re

from markdown_it import MarkdownIt



def get_section_content(md_file, target_section):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    md = MarkdownIt()
    tokens = md.parse(content)
    
    capturing = False
    section_tokens = []
    current_level = None
    skip_next_inline = False
    
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            level = int(token.tag[1])
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None
            
            if next_token and next_token.type == 'inline' and next_token.content == target_section:
                capturing = True
                current_level = level
                skip_next_inline = True  # Skip the heading text itself
                continue
            elif capturing and level <= current_level:
                break
        
        if capturing:
            if skip_next_inline and token.type == 'inline':
                skip_next_inline = False
                continue
            
            section_tokens.append(token)
    
    text_parts = []
    for token in section_tokens:
        if token.type == 'inline':
            text_parts.append(token.content)
        elif token.type == 'paragraph_close':
            text_parts.append('\n')
        elif token.type in ['code_block', 'fence']:
            text_parts.append('\n' + token.content + '\n')
    
    return ''.join(text_parts).strip()



def get_filename(content):
    match = re.search(r"###\s*(.*?)\.py", content)
    if match:
        result = match.group(1)
        return f'{result}.py'
    else:
        raise ValueError("No file name in content to match patter '### *.py'")



def generate_filename_and_content(path, sections):
    for sec in sections:
        content = get_section_content(path, sec)
        filename = get_filename(content)
        yield filename, content
        