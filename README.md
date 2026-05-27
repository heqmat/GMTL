# GMTL(Generic Macro Template Language)

GMTL is completely generic one-file human-readable configuration layer language to modify any kinds of machine data with parameterless macros thanks to its "extreme agnostic" nature. 
The goal of GMTL isn't to invent a new way to swap text, but to provide a self-contained 'dashboard' at the top of complex data files so humans can safely modify them without breaking the underlying syntax. Lexer of GMTL uses regex-based tokenizer.

## Structure of GMTL:

<img width="712" height="440" alt="image" src="https://github.com/user-attachments/assets/e429f56a-5bf2-4314-bea8-0a7e67054fab" />


It's possible to define variables at the top of the code, then insert them into data through processor where output file doesn't include GMTL tag and definitions. This allows any type of data to be easily transferred between users via parameterless macros that can be modified easily.

An example how processor processes it:

<img width="888" height="468" alt="image" src="https://github.com/user-attachments/assets/bee6802e-7921-4cfc-afdd-cd3659e73ff6" />

## Syntax and Documentation
Syntax structure of GMTL is unusually easy and practical. Any variable must be placed inside `<%GMTL ... %>` tag. However, Open tag should be at top of other codes and close tag should be at bottom of defined variables where rest is any data. 
GMTL does not require two different files like Template engines does, it works completely inside one single file.
GMTL has only one kind of data type which is basically string. If one wants to write numbers, boolean values or any other complex data type, they should simply write it inside `"..."` provided that any `"` is escaped properly inside the value. 

For example, a string is defined like this:
```python
<%GMTL
varname = "\"mystring\""; 
%>
```
or an integer:
```python
<%GMTL
varname = "3"; 
%>
```
or boolean values:
```python
<%GMTL
varname = "true"; 
%>
```
GMTL also supports multi-line values like:
```python
<%GMTL
varname = "Multilines are good. Multilines are good.
Multilines are good. Multilines are good.
"; 
%>
```
For the string interpolation part, replaced data should be `$varname$`, so it should not include $ symbols in any way and it should not have new lines, but it can have spaces though. 

## Example usage
`python3.12 .\gmtl_processor.py -i inputfile.txt -o outputfile.txt`

**Input File:**
```python
<%GMTL
VERSION = "v1.2.0";
THEME_COLOR = "#ff5500";
%>
{
  "meta": { "version": "$VERSION$" },
  "styles": { "primary": "$THEME_COLOR$" }
}
```
**Output File:**
```python
{
  "meta": { "version": "v1.2.0" },
  "styles": { "primary": "#ff5500" }
}
```

## Parameterized Macros
GMTL currently doesn't support parameterized macros due to security concerns like "execution of malicious codes inside passive notation or markup languages such as JSON, HTML". But this might be considered and updated in the future.


