IOTA Mnemonic
=============

This is a command line tool to help user generate IOTA seed from Bitcoin BIP39 mnenomics

Changes in this fork
=======

To prevent sensitive user input being saved to shell history I provided additional options

* -sp or --securepassphrase

 This option activates the passphrase option, but the passphrase is not entered directly in the initial command but in a prompt during program execution. For this the Python library getpass is used for added security.
 
 To create a new mnemonic with passphrase enter
 
 ```
$ python -m iota_mnemonic -sp
```
and then enter the passphrase when prompted.
 
* -m or --mnemonic

 This option allows entering the mnemonic and outputs the corresponding IOTA seed.
 
 To recover the IOTA seed from a mnemonic enter
 ```
 $ python -m iota_menmonic -p TREZOR -m mnemonic "often various act decide tongue sausage summer wall priority knock finish until taxi robot panic toward giraffe acid avocado anchor travel kiwi actress cream"
 ```

* -sm or --securemnemonic

 The same as option --mnemonic but again using the getpass library for added security.
 
 To recover a seed from mnemonic enter
 
 ```
$ python -m iota_mnemonic -sm
```
and then enter the mnemonic when prompted.


The options can be freely combined. To recover a seed from a mnemonic and a passphrase enter

```
$ python -m iota_mnemonic -sm -sp
```

*Note that you need to download the source code from this fork for the newly added options (or wait for the pull request to be merged)!*



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

# Generate mnemonic with passphrase
$ python -m iota_mnemonic -p TREZOR
Mnemonic: limit about defy sail base useless soul album aim border celery false asset average 
romance attract lonely track hope sun afford creek dignity couple
IOTA Seed: LIPSSXDAJQRLBPTTBQTPTYBMUSTJPXWGYBKLSSBDVKPVEAXDGPZXOWPMEGRNSHTJXIUVCXYFTOXMZKIMY

# Generate 12 words mnemonic with passphrase
$ python -m iota_mnemonic -s 128 -p TREZOR
Mnemonic: broccoli merry lucky milk lizard cannon area utility jelly click bag clever
IOTA Seed: YNONELPCFBKQDDQMIBBBGJDZODCKXEBIJIMXRUGBA9AOPJEQ9SYYLGID9IXHILWVVDJ9ZEGQHCGIHQ9TB

# Genreate mnemonic with japanese
$ python -m iota_mnemonic -l japanese
Mnemonic: こいぬ　ようちえん　むせん　いんさつ　しなもの　ふのう　かわく　ひかり　はいけん　
そんしつ　たたかう　ちいさい　そうめん　つうわ　にんげん　とおす　さみだれ　かまぼこ　
らくだ　さずかる　ふとる　とんかつ　きびしい　ひつぜん
IOTA Seed: ISBAFGB9LBGOQYGKKMMNK9APICZCGWIJHCMLOLPAQITGSSIGBJJOYQZJJ9NNGYIJLFB9ORMJGCWFFFYQZ

# Output the mnemonic to file
$ python -m iota_mnemonic -p TREZOR -o mnemonic

# Recover seed from mnemonic
$ python -m iota_menmonic -p TREZOR -f mnemonic
Mnemonic: often various act decide tongue sausage summer wall priority knock finish until 
taxi robot panic toward giraffe acid avocado anchor travel kiwi actress cream
IOTA Seed: CRGFVETUFKUQYTPTEH9TP9BDKBVZLG9UZJDZBDMMFSSCUPIATPEZMKBLKXOEKCRDFHHFNCCBF9SKHNYIA
```

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
