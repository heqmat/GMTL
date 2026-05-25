#Generic Macro Template Language
import mmap
import re

TOKEN_SPECIFICATION = [
    # Updated to handle trailing white-spaces cleanly without demanding hard newlines
    ('VALUE', rb'"[^"\\]*(?:\\.[^"\\]*)*";\s*'), 
    ('OPEN_TAG', rb'<%GMTL\s+'),
    ('ID', rb'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('CLOSE_TAG', rb'%>'),
    ('ASSIGNMENT', rb'='),
    ('CURLY', rb'"'), 
    ('SKIP', rb'\s+'),
]

# Native byte joining prevents the string-decode escape sequence corruption
master_bytes_regex = b'|'.join(
    b'(?P<' + name.encode() + b'>' + pattern + b')' 
    for name, pattern in TOKEN_SPECIFICATION
)

def compile_file(file_path):
    window = []
    macros = []
    open_tag = 0
    close_tag = 0
    first_meaningful_token = True 

    with open(file_path, "rb") as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as m:
            
            for match in re.finditer(master_bytes_regex, m):
                token_type = match.lastgroup
                token_value = match.group(token_type).decode('utf-8')
                match_start = match.start()
    
                line_start = m.rfind(b'\n', 0, match_start) + 1
                line_end = m.find(b'\n', match_start)
                if line_end == -1:
                    line_end = len(m)

                line_number = m[:match_start].count(b'\n') + 1
                exact_line = m[line_start:line_end].decode('utf-8').rstrip('\r\n')

                if token_type == 'SKIP':
                    continue

                if token_type == 'OPEN_TAG':
                    if not first_meaningful_token:
                        print("ForbiddenUsage: <%GMTL must be placed top of other codes")
                        return None
                    open_tag = 1
                
                if token_type == 'CLOSE_TAG':
                    close_tag = 1

                first_meaningful_token = False
                window.append((token_type, token_value))

                # --- STEP-BY-STEP LOOKAHEAD SYNTAX CHECKER ---
                if len(window) >= 2:
                    t_current = window[-2]
                    t_next = window[-1]

                    if t_current[0] == "OPEN_TAG" and t_next[0] != "ID":
                        print(f"-----> {exact_line}, at line {line_number}")
                        print(f"SyntaxError: '<%GMTL' expected a variable name but got {t_next[1]}")
                        return None
                    elif t_current[0] == "ID" and t_next[0] != "ASSIGNMENT":
                        print(f"-----> {exact_line}, at line {line_number}")
                        print(f"SyntaxError: '{t_current[1]}' expected '=' but got {t_next[1]}")
                        return None
                    elif t_current[0] == "ASSIGNMENT" and t_next[0] != "VALUE":
                        print(f"-----> {exact_line}, at line {line_number}")
                        print(f"SyntaxError: '=' expected an assignment string value but got {t_next[1]}")
                        return None
                    elif t_current[0] == "CURLY" and t_next[0] == "CURLY":
                        print(f"-----> {exact_line}, at line {line_number}")
                        print(f"SyntaxError: Unexpected missing ';'")
                        return None
                    elif t_current[0] == "CURLY" and t_next[0] != "CURLY":
                        print(f"-----> {exact_line}, at line {line_number}")
                        print(f"SyntaxError: Unexpected '{t_next[1]}' missing '\"'")
                        return None

                # --- MACRO & TERMINATION ENGINE ---
                # Check relative alignments using negative index slices 
                if len(window) >= 3:
                    if window[-3][0] == "ID" and window[-2][0] == "ASSIGNMENT" and window[-1][0] == "VALUE":
                        macros.append((window[-3][1], window[-1][1]))

                if token_type == 'CLOSE_TAG':
                    if open_tag == 1:
                        return macros, line_number

                # Safely slide the 3-token memory window forward in RAM
                if len(window) > 3:
                    window.pop(0)

    if open_tag == 0:
        print(f"OpenTagNotFound: Please specify '<%GMTL' open tag")
    elif open_tag == 1 and close_tag == 0:
        print(f"CloseTagNotFound: the GMTL tag opened but never closed")
    
    return None
