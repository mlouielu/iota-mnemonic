IOTA Mnemonic
=============

This is a command line tool to help user generate IOTA seed from Bitcoin BIP39 mnenomics

Install
=======

### $ pipenv install iota_mnemonic

To install IOTA mnemonic, simply run this simple command in your terminal of choice:

```
$ pipenv install iota_mnemonic
```

### Get the source code

You can clone the source code from repository:

```
$ git clone https://github.com/mlouielu/iota-mnemonic
```

How to use
==========

```
# Generate 24 words mnemonic and IOTA seed
$ python -m iota_mnemonic
Mnemonic: come grocery cube calm void liberty increase pigeon captain appear employ among
float fancy cargo faith seek buzz argue lift agent split bachelor judge
IOTA Seed: RTWTRPAEGJQFRWAYTIJTKWZKLN9K9VRUETFSIPUAUCLKPNNSNWAKTOXBWSCPQVNNWDLTEIPMILIOVPGIX

# Generate mnemonic with passphrase (passphrase is entered in separate prompt)
$ python -m iota_mnemonic -sp
Passphrase:
Mnemonic: limit about defy sail base useless soul album aim border celery false asset average
romance attract lonely track hope sun afford creek dignity couple
IOTA Seed: LIPSSXDAJQRLBPTTBQTPTYBMUSTJPXWGYBKLSSBDVKPVEAXDGPZXOWPMEGRNSHTJXIUVCXYFTOXMZKIMY

# Generate 12 words mnemonic with passphrase
$ python -m iota_mnemonic -s 128 -sp
Mnemonic: broccoli merry lucky milk lizard cannon area utility jelly click bag clever
IOTA Seed: YNONELPCFBKQDDQMIBBBGJDZODCKXEBIJIMXRUGBA9AOPJEQ9SYYLGID9IXHILWVVDJ9ZEGQHCGIHQ9TB

# Genreate mnemonic with japanese
$ python -m iota_mnemonic -l japanese
Mnemonic: こいぬ　ようちえん　むせん　いんさつ　しなもの　ふのう　かわく　ひかり　はいけん　
そんしつ　たたかう　ちいさい　そうめん　つうわ　にんげん　とおす　さみだれ　かまぼこ　
らくだ　さずかる　ふとる　とんかつ　きびしい　ひつぜん
IOTA Seed: ISBAFGB9LBGOQYGKKMMNK9APICZCGWIJHCMLOLPAQITGSSIGBJJOYQZJJ9NNGYIJLFB9ORMJGCWFFFYQZ

# Recover seed from mnemonic (hidden passphrase in example is TREZOR)
$ python -m iota_mnemonic -sm -sp
Mnemonic:
Passphrase:
Mnemonic: often various act decide tongue sausage summer wall priority knock finish until
taxi robot panic toward giraffe acid avocado anchor travel kiwi actress cream
IOTA Seed: CRGFVETUFKUQYTPTEH9TP9BDKBVZLG9UZJDZBDMMFSSCUPIATPEZMKBLKXOEKCRDFHHFNCCBF9SKHNYIA

# Output the mnemonic to file
$ python -m iota_mnemonic -sp -o mnemonic
Passphrase:

# Recover seed from mnemonic file
$ python -m iota_mnemonic -sp -f mnemonic
Passphrase:
Mnemonic: often various act decide tongue sausage summer wall priority knock finish until
taxi robot panic toward giraffe acid avocado anchor travel kiwi actress cream
IOTA Seed: CRGFVETUFKUQYTPTEH9TP9BDKBVZLG9UZJDZBDMMFSSCUPIATPEZMKBLKXOEKCRDFHHFNCCBF9SKHNYIA
```

The options -sp and -sm use the getpass library to ask for the password in a separate prompt without echoing. This ensures that neither the passphrase nor the mnemonic are saved in shell history.

How it works?
=============

To create IOTA seed from the mnemonic, we use IOTA Kerl function with a mnemonic
sentence (in UTF-8 NFKD) used as the password and the string "mnemonic" + passphrase
(again in UTF-8 NFKD) used as the salt.

To get a valid tryte hash, we concat salt and mnemonic sentence, and load into `iota.Hash`
by `from_string` function. `from_string` will encode UTF-8 NFKD into bytes, then convert
bytes into IOTA hash.

Using each hash, we then use hash trits and Kerl to absorb and squeeze:

```python
trits = []
sponge = iota.crypto.kerl.Kerl()

for word in mnemonic:
    hash = iota.Hash.from_string(f'mnemonic{passphrase}{word}')
    hash_trits = hash.as_trits()
    k = iota.crypto.kerl.Kerl()
    k.absorb(hash_trits)
    k.squeeze(hash_trits)
    sponge.absorb(hash_trits)
sponge.squeeze(trits)
return iota.Hash.from_trits(trits)
```
