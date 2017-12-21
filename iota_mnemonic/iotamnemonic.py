# -*- coding: utf-8 -*-

import iota
import mnemonic


class IOTAMnemonic(mnemonic.Mnemonic):
    @classmethod
    def to_iota_seed(cls, mnemonic, passphrase=''):
        mnemonic = cls.normalize_string(mnemonic)
        passphrase = cls.normalize_string(passphrase)

        trits = []
        sponge = iota.crypto.kerl.Kerl()
        for word in mnemonic.split():
            hash = iota.Hash.from_string(f'mnemonic{passphrase}{word}')
            hash_trits = hash.as_trits()
            k = iota.crypto.kerl.Kerl()
            k.absorb(hash_trits)
            k.squeeze(hash_trits)
            sponge.absorb(hash_trits)
        sponge.squeeze(trits)
        return iota.Hash.from_trits(trits)


if __name__ == '__main__':
    i = IOTAMnemonic('english')
    mnemo = i.generate(256)
    print(mnemo)
    print(i.to_iota_seed(mnemo))
