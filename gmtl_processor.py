from gmtl_tokenizer import compile_file
import re
import argparse

parser = argparse.ArgumentParser(description="GMTL Processor")
parser.add_argument("-i","--input", required=True, help="Add input GMTL file path")
parser.add_argument("-o","--output", required=True, help="Write output file name")
args = parser.parse_args()

macro_regex = r'(?<!\\)\$.+?(?<!\\)\$'
commas_regex = r'"[^"\\]*(?:\\.[^"\\]*)*"'

def process(file_path, new_file):
    print("--> Starting compilation...")
    result = compile_file(file_path)
    
    if result is None:
        print("CRITICAL: Tokenizer failed or returned None. Output file will not be generated.")
        return
        
    macroArray, startLine = result
    print(f"--> Tokenizer Success! Found macros: {macroArray}")
    print(f"--> Template header ends at line: {startLine}")
    
    lines_written = 0
    with open(file_path, "r", encoding="utf-8") as infile, open(new_file, "w", encoding="utf-8") as outfile:
        # We start enumerate at 1 to align with line tracking
        for line_num, line in enumerate(infile, 1): 
            
            # If the current line is part of the <%GMTL ... %> header, skip writing it to the output
            if line_num <= startLine:
                continue
                
            matches = re.findall(macro_regex, line)
            if matches:
                modified_line = line
                for match in matches:
                    macro_name = match[1:-1] # Strip $ markers
                    
                    for assigns in macroArray:
                        if assigns[0] == macro_name:
                            string_match = re.search(commas_regex, assigns[1])
                            if string_match:
                                # Strip outer quotes and replace macro
                                raw_value = string_match.group()[1:-1]
                                # Unescape the backslashes so \" becomes " in the final file
                                raw_value = raw_value.replace('\\"', '"').replace('\\\\', '\\')
                                modified_line = modified_line.replace(match, raw_value)
                outfile.write(modified_line)
                lines_written += 1
            else:
                outfile.write(line)
                lines_written += 1

    print(f"--> Complete! Successfully wrote {lines_written} lines to {new_file}")

process(args.input, args.output)
