import re
import sys
import os

class ModelGenerator:
    def __init__(self, sql_content):
        self.sql_content = sql_content
        self.type_mapping = {
            'INTEGER': 'Integer',
            'TEXT': 'Text',
            'DATETIME': 'DateTime',
            'BIGINT': 'BigInteger',
            'VARCHAR': 'String',
            'BOOLEAN': 'Boolean',
            'FLOAT': 'Float',
            'BLOB': 'LargeBinary'
        }

    def parse(self):
        # Normalize content: remove comments
        content = re.sub(r'/\*.*?\*/', '', self.sql_content, flags=re.DOTALL)
        content = re.sub(r'--.*', '', content)
        
        # Find CREATE TABLE statements
        table_matches = re.finditer(r'CREATE TABLE\s+"?(\w+)"?\s*\((.*?)\);', content, re.DOTALL | re.IGNORECASE)
        
        models = []
        for match in table_matches:
            table_name = match.group(1)
            body = match.group(2)
            model_code = self.generate_model(table_name, body)
            models.append(model_code)
            
        return "\n\n".join(models)

    def generate_model(self, table_name, body):
        class_name = "".join(x.capitalize() for x in table_name.split('_'))
        
        lines = [
            f"class {class_name}(BaseMixin, Base):",
            f"    __tablename__ = '{table_name}'"
        ]
        
        columns = []
        table_args = []
        
        # Split body by lines or commas, respecting parentheses
        definitions = self.split_definitions(body)
        
        for definition in definitions:
            definition = definition.strip()
            if not definition:
                continue
                
            if definition.upper().startswith('FOREIGN KEY'):
                # self.parse_foreign_key(definition, columns) # FKs usually defined inline or at end, SQLAlchemy defines on Column or ForeignKeyConstraint
                # For simplicity in this regex parser, let's try to extract FK info to add to table args or column args
                # But typically "FOREIGN KEY (col) REFERENCES table(col)" map to ForeignKeyConstraint or Column(ForeignKey(...))
                # Let's handle explicit FOREIGN KEY line as table arg or try to attach to column if possible.
                # Simplest for separate line FK: ForeignKeyConstraint
                # Parse: FOREIGN KEY ("account_id") REFERENCES "wechat_accounts" ("account_id")
                fk_match = re.search(r'FOREIGN KEY\s*\("?(\w+)"?\)\s*REFERENCES\s+"?(\w+)"?\s*\("?(\w+)"?\)', definition, re.IGNORECASE)
                if fk_match:
                    local_col, remote_table, remote_col = fk_match.groups()
                    # Find the column definition and add ForeignKey to it, OR add to __table_args__
                    # Adding to __table_args__ is safer for composite or separate definitions
                    # But Pythonic way is often Column(..., ForeignKey('...'))
                    # Let's try to update the column definition if it exists
                    updated = False
                    for i, col in enumerate(columns):
                        if col['name'] == local_col:
                            col['foreign_key'] = f"{remote_table}.{remote_col}"
                            updated = True
                            break
                    if not updated:
                         # Fallback to table args if we can't find column (unlikely)
                         pass

            elif definition.upper().startswith('UNIQUE'):
                # UNIQUE ("account_id" ASC, "name" ASC, ...)
                unique_content = re.search(r'UNIQUE\s*\((.*?)\)', definition, re.IGNORECASE)
                if unique_content:
                    cols = [c.strip().split()[0].replace('"', '') for c in unique_content.group(1).split(',')]
                    quoted_cols = ", ".join(f"'{c}'" for c in cols)
                    table_args.append(f"UniqueConstraint({quoted_cols})")
            
            elif definition.upper().startswith('PRIMARY KEY'):
                 # PRIMARY KEY ("id") - sometimes separate line
                 pk_match = re.search(r'PRIMARY KEY\s*\("?(\w+)"?\)', definition, re.IGNORECASE)
                 if pk_match:
                     pk_col = pk_match.group(1)
                     for col in columns:
                         if col['name'] == pk_col:
                             col['primary_key'] = True

            elif re.match(r'^\(.*\)', definition):
                # Check constraints or other directives starting with (
                pass
            
            else:
                # Column definition
                # "id" INTEGER PRIMARY KEY AUTOINCREMENT
                # "name" TEXT NOT NULL
                col_parts = definition.split()
                col_name = col_parts[0].replace('"', '')
                col_type = col_parts[1].replace('"', '') # Clean up type
                
                # Handle types with length e.g. VARCHAR(1)
                sql_type_match = re.match(r'(\w+)(?:\((\d+)\))?', col_type)
                if sql_type_match:
                    base_type = sql_type_match.group(1).upper()
                    length = sql_type_match.group(2)
                    sa_type = self.type_mapping.get(base_type, 'Text')
                    if length and sa_type == 'String':
                        sa_type = f"String({length})"
                else:
                    sa_type = 'Text'

                col_def = {
                    'name': col_name,
                    'type': sa_type,
                    'primary_key': 'PRIMARY KEY' in definition.upper(),
                    'autoincrement': 'AUTOINCREMENT' in definition.upper(),
                    'nullable': 'NOT NULL' not in definition.upper() and 'PRIMARY KEY' not in definition.upper(),
                    'default': None,
                    'foreign_key': None
                }
                
                # Parse DEFAULT
                default_match = re.search(r'DEFAULT\s+(\S+)', definition, re.IGNORECASE)
                if default_match:
                    default_val = default_match.group(1)
                    if default_val.isdigit():
                        col_def['default'] = default_val
                    else:
                        col_def['default'] = f"'{default_val.strip(chr(39))}'" # Strip quotes if present

                columns.append(col_def)

        # Construct Code
        
        # __table_args__
        if table_args:
            lines.append("    __table_args__ = (")
            for arg in table_args:
                lines.append(f"        {arg},")
            lines.append("    )")
        
        lines.append("")
        
        for col in columns:
            if col['name'] == 'id':
                continue
            
            args = [col['type']]
            if col['foreign_key']:
                args.append(f"ForeignKey('{col['foreign_key']}')")
            if col['primary_key']:
                args.append("primary_key=True")
            if col['autoincrement']:
                args.append("autoincrement=True")
            if not col['nullable']:
                args.append("nullable=False")
            if col['default'] is not None:
                args.append(f"default={col['default']}")
            
            lines.append(f"    {col['name']} = Column({', '.join(args)})")

        return "\n".join(lines)

    def split_definitions(self, body):
        # Simple splitter by comma, ignoring parens
        defs = []
        current = []
        paren_count = 0
        for char in body:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            
            if char == ',' and paren_count == 0:
                defs.append("".join(current))
                current = []
            else:
                current.append(char)
        if current:
            defs.append("".join(current))
        return defs

def generate_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    generator = ModelGenerator(content)
    code = generator.parse()
    
    header = "from sqlalchemy import Column, Integer, Text, String, DateTime, BigInteger, ForeignKey, UniqueConstraint, Boolean, Float, LargeBinary\n"
    header += "from db.database import Base, BaseMixin\n\n"
    
    return header + code

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(generate_from_file(sys.argv[1]))
    else:
        # Default test
        # print(generate_from_file(r'h:\traeworkspace\AiBot\src\backend\data\contacts.sql'))
        pass
