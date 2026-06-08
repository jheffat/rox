#!/usr/bin/env python3
"""
ROX - XOR Header Key Analyzer

Author: Jheff AT
Version: 1.0.0

Educational cryptanalysis utility that attempts to recover
simple XOR key patterns by comparing encrypted file bytes
against known binary file signatures such as JPEG, PNG, PDF,
ZIP, EXE and more headers.

<<Dict.bin>> should contain potential XOR keys to test against the file's header bytes. 
The script identifies repeated patterns in the decrypted output
to suggest likely keys and their corresponding decrypted headers. 
This can be useful for analyzing files that have been obfuscated
with a single-byte XOR cipher, especially when the original file 
type is unknown.        

"""
import string
from glob import glob
from sys import argv
from base64 import b64encode

__author__ = "Jheff AT"
__version__ = "1.0.0"
__email__ = "jheff.at@gmail.com"

def banner():
    print("""        ╔════════════════════════════╗
        ║  ██████╗  ██████╗ ██╗  ██╗ ║
        ║  ██╔══██╗██╔═══██╗╚██╗██╔╝ ║
        ║  ██████╔╝██║   ██║ ╚███╔╝  ║
        ║  ██╔══██╗██║   ██║ ██╔██╗  ║
        ║  ██║  ██║╚██████╔╝██╔╝ ██╗ ║
        ║  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ║
        ║                            ║
        ║  XOR Header Key Analyzer   ║
        ╚════════════════════════════╝""")
    print("\nAuthor: Jheff AT" + " | Version: " + __version__ + " Copyright (c) 2026 | Contact: " + __email__  + "\n")
    print("This tool attempts to recover XOR keys by analyzing the first 50")
    print("bytes of files against a dictionary of potential keys." )
    print("\nUsage: rox <file_pattern>")
    print("""Example: 
                rox *.jpg
                rox *.*
                rox videoclip.mp4\n""")
def rox(filename):
    keys=[] 
    encrypted_headers=open(filename,"rb").read(50)
    datadict=open("dict.bin","rb") 
    # Read the dictionary file in chunks of 50 bytes to match the length of the encrypted header
    for know_header in datadict:
        # Generate a candidate key by XORing each byte of the encrypted header with the corresponding byte of the known header   
        candidate_key=bytes(e^d for e,d in zip(encrypted_headers,know_header))   
        # Check if all bytes in the candidate key are printable ASCII characters  
        if all(chr(b).isprintable() for b in candidate_key) and len(candidate_key) > 0:
            # Look for repeated patterns in the candidate key to identify potential keys
            needle=candidate_key[0:5]
            if candidate_key.count(needle) > 1:
                pos= []
                start = 0
                while True:
                    idx = candidate_key.find(needle, start)
                    if idx == -1:
                        break
                    pos.append(idx)
                    start = idx + 1         
                gotkey=candidate_key[0:pos[1]]    
                # XOR the encrypted header with the candidate key to see if it matches the known header
                if bytes(e^k for e,k in zip(encrypted_headers,gotkey))==know_header[0:len(gotkey)]:
                    # Format the candidate key in hexadecimal, base64, and ASCII representations for output
                    hex_key=" ".join(f"{b:02X}" for b in gotkey)
                    keys.append({"base64": str(b64encode(gotkey)),"ascii": gotkey,"hex": hex_key,"len": len(gotkey)})   
    return keys
def main():
    # Check if 'dict.bin' exists in the current directory before proceeding
    if glob("dict.bin")==0:
        print("\n❌Error: 'dict.bin' not found. Please ensure it is in the same directory as this script.")
        exit(1)
    getarg=argv
    if len(getarg)==2:
        l=glob(getarg[1])# Use glob to find files matching the provided pattern
        if len(l)==0:
            banner()
            exit("\n❌Error: No files found matching the pattern.")
        banner()
        # Analyze each file found and print the results in a formatted manner
        for i in l:
            print("-"*80)
            print(f" 🔍Analyzing encrypted file {i.upper()}...")
            result=rox(i)             
            # Print the candidate keys found for the current file in a structured format, or indicate if no matches were found
            print(
            "\n".join(
                        f"     {i}.Candidate Key\n         HEX    : {item['hex']} \n         Base64 : {item['base64']}\n         ASCII  : {item['ascii'].decode('utf-8')} \n         Length : {item['len']} Bytes"
                        for i, item in enumerate(result, 1)
                         )
                        if result
                        else "       - No matches found.")
                    
            print("-"*80 + "\n")
        print("[📄] Analysis completed.\n")
    else:
        banner()                                 

        

if __name__ == "__main__":   
    main()
    
if __name__ == "__main__":    
    main()
    
