import os
import glob
from models_util import ModelGenerator

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
MODELS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/models.py'))

def generate_all():
    sql_files = glob.glob(os.path.join(DATA_DIR, '*.sql'))
    
    new_models_code = []
    
    for sql_file in sql_files:
        with open(sql_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        generator = ModelGenerator(content)
        code = generator.parse()
        if code.strip():
            new_models_code.append(f"# Generated from {os.path.basename(sql_file)}")
            new_models_code.append(code)
            new_models_code.append("")

    if not new_models_code:
        print("No models generated.")
        return

    with open(MODELS_FILE, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Clean up previous generations
    marker = "# --- Generated Models ---"
    if marker in original_content:
        original_content = original_content.split(marker)[0].strip()

    # Update imports
    required_imports = [
        'Column', 'Integer', 'Text', 'String', 'BigInteger', 
        'DateTime', 'ForeignKey', 'UniqueConstraint', 'Boolean', 
        'Float', 'LargeBinary'
    ]
    
    lines = original_content.splitlines()
    import_line_index = -1
    for i, line in enumerate(lines):
        if line.startswith('from sqlalchemy import'):
            import_line_index = i
            break
            
    if import_line_index != -1:
        lines[import_line_index] = f"from sqlalchemy import {', '.join(required_imports)}"
    else:
        lines.insert(0, f"from sqlalchemy import {', '.join(required_imports)}")

    # Check if we need to append or if it's already there?
    # For now, I will append. Users can clean up duplicates if they run it multiple times.
    # To be safer, I could check if "class ClassName" exists.
    
    final_code_lines = lines + ["", "# --- Generated Models ---", ""] + new_models_code
    
    with open(MODELS_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(final_code_lines))
        
    print(f"Updated {MODELS_FILE} with new models.")

if __name__ == '__main__':
    generate_all()
