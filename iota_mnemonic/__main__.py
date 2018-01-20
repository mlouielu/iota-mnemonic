# -*- coding: utf-8 -*-

import argparse
import getpass

from .iotamnemonic import IOTAMnemonic


def main():
    prog = 'iotamenomic'
    description = 'Create and recover IOTA seed from Bitcoin BIP39 mnemonic'
    parser = argparse.ArgumentParser(prog=prog, description=description)

    parser.add_argument('-s', '--strength', nargs='?',
                     choices=[128, 160, 192, 224, 256],
                     type=int, default=256)
    parser.add_argument('-l', '--language', nargs='?', default='english')
    mnemonicGroup = parser.add_mutually_exclusive_group()
    mnemonicGroup.add_argument('-m', '--mnemonic', nargs='?')
    mnemonicGroup.add_argument('-sm', '--securemnemonic', action='store_true', help='Allows entering of mnemonic in extra prompt, where entry is not saved in shell history')
    passphraseGroup = parser.add_mutually_exclusive_group()
    passphraseGroup.add_argument('-p', '--passphrase', nargs='?', default='')
    passphraseGroup.add_argument('-sp', '--securepassphrase', action='store_true', help='Allows entering of passphrase in extra prompt, where entry is not saved in shell history')
    parser.add_argument('-o', '--output', help='Output path for mnemonic words')
    parser.add_argument('-f', '--infile')

    options = parser.parse_args()
    im = IOTAMnemonic(options.language)

    if options.infile:
        # Recover IOTA seed from mnemonic file
        mnemo = open(options.infile, 'r').read().strip()
        if not mnemo:
            raise ValueError(f'Can not read anything from file: {options.infile}')
    elif options.securemnemonic:
        mnemo = getpass.getpass('Mnemonic:')
    elif options.mnemonic:
        mnemo = options.mnemonic
    else:
        # Generate IOTA seed from Bitcoin bip39 mnemonic
        mnemo = im.generate(options.strength)

    if options.securepassphrase:
        passphrase = getpass.getpass('Passphrase:')
    else:
        passphrase = options.passphrase
    
    if options.output:
        with open(options.output, 'w') as f:
            f.write(mnemo)
    else:
        print(f'Mnemonic: {mnemo}')
        print(f'IOTA Seed: {im.to_iota_seed(mnemo, passphrase)}')


if __name__ == '__main__':
    main()
    
