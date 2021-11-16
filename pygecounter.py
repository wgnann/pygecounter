import argparse
import os
import pikepdf
import subprocess
import sys

def ps(documento):
    grep = '/bin/grep'
    gs = '/usr/bin/gs'

    # grep ou gs
    try:
        output = subprocess.check_output([
            grep, '-a', '%%Pages', documento
        ])

    except subprocess.CalledProcessError:
        output = subprocess.check_output([
            gs, '-o', '/dev/null', '-sDEVICE=bbox', documento
        ], stderr=subprocess.STDOUT)

        # [...]%%HiResBoundingBox:
        return output.decode().count('%%HiResBoundingBox')

    else:
        # b'%%Pages: 10\n'
        return output.decode().split()[1] 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('caminho', metavar='caminho', type=str, help='caminho para o arquivo')
    args = parser.parse_args()

    try:
        pdf = pikepdf.Pdf.open(args.caminho)
    except pikepdf._qpdf.PdfError:
        print(ps(args.caminho))
    else:
        print(len(pdf.pages))

if __name__ == "__main__":
    main()
