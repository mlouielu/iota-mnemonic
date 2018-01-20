# -*- coding: utf-8 -*-

import argparse
from .iotamnemonic import IOTAMnemonic


def main():
    prog = 'iotamenomic'
    description = 'Create and recover IOTA seed from Bitcoin BIP39 mnemonic'
    parser = argparse.ArgumentParser(prog=prog, description=description)

    parser.add_argument('-s', '--strength', nargs='?',
                     choices=[128, 160, 192, 224, 256],
                     type=int, default=256)
    parser.add_argument('-l', '--language', nargs='?', default='english')
    parser.add_argument('-m', '--mnemonic', nargs='?')
    parser.add_argument('-p', '--passphrase', nargs='?', default='')
    parser.add_argument('-o', '--output', help='Output path for mnemonic words')
    parser.add_argument('-f', '--infile')

    options = parser.parse_args()
    im = IOTAMnemonic(options.language)

    if options.infile:
        # Recover IOTA seed from mnemonic file
        mnemo = open(options.infile, 'r').read().strip()
        if not mnemo:
            raise ValueError(f'Can not read anything from file: {options.infile}')
    elif options.mnemonic:
        mnemo = options.mnemonic
    else:
        # Generate IOTA seed from Bitcoin bip39 mnemonic
        mnemo = im.generate(options.strength)

    
    if options.output:
        with open(options.output, 'w') as f:
            f.write(mnemo)
    else:
        print(f'Mnemonic: {mnemo}')
        print(f'IOTA Seed: {im.to_iota_seed(mnemo, options.passphrase)}')


if __name__ == '__main__':
    main()
    
