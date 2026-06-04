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
    chars=string.ascii_letters+string.digits+"!@#$%^&*()_+-=~`[]{}|;:'\",.<>/? "
    key="";keys=[] 
    data=open(filename,"rb").read(50)
    datadict=open("dict.bin","rb") 
    
    for header in datadict:
        keymatched=''
        for e,d in zip(data,header):
            key=chr(e^d)
            if key in chars:
                keymatched+=key    
        
        needle=keymatched[0:5]
        if keymatched.count(needle) > 1:
            pos= []
            start = 0
            while True:
                idx = keymatched.find(needle, start)
                if idx == -1:
                    break
                pos.append(idx)
                start = idx + 1          
            keys.append(f"🔑Encryption Key Recovered--->  {keymatched[0:pos[1]]}" )     
    return keys
def main():
    if glob("dict.bin")==0:
        print("\n❌Error: 'dict.bin' not found. Please ensure it is in the same directory as this script.")
        exit(1)
    getarg=argv
    if len(getarg)==2:
        l=glob(getarg[1])
        if len(l)==0:
            banner()
            exit("\n❌Error: No files found matching the pattern.")
        banner()
        for i in l:
            print("\n" + "-"*80 + "\n")
            print(f" 🔍Analyzing encrypted file {i.upper()}...")
            result=rox(i)       
            print("\n".join(f"     {i}. {item}" for i, item in enumerate(result, 1)) if result else "       -No matches found.")
            print("\n" + "-"*80 + "\n")
        print("[📄] Analysis complete.\n")
    else:
        banner()

        

if __name__ == "__main__":    
    main()
    
