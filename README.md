# IOTA Mnemonic

This is a command line tool to help user generate IOTA seed from Bitcoin BIP39 mnenomics

## Install

### `$ pipenv install iota_mnemonic`

To install IOTA mnemonic, simply run this simple command in your terminal of choice:

```
$ pipenv install iota_mnemonic
```

### Get the source code

You can clone the source code from repository:

```
$ git clone https://github.com/mlouielu/iota-mnemonic
```

## How to use

Generate 24 words mnemonic and IOTA seed:
```
$ python -m iota_mnemonic
Mnemonic: come grocery cube calm void liberty increase pigeon captain appear employ among 
float fancy cargo faith seek buzz argue lift agent split bachelor judge
IOTA Seed: RTWTRPAEGJQFRWAYTIJTKWZKLN9K9VRUETFSIPUAUCLKPNNSNWAKTOXBWSCPQVNNWDLTEIPMILIOVPGIX
```

Generate mnemonic with passphrase:
```
$ python -m iota_mnemonic -p TREZOR
Mnemonic: limit about defy sail base useless soul album aim border celery false asset average 
romance attract lonely track hope sun afford creek dignity couple
IOTA Seed: LIPSSXDAJQRLBPTTBQTPTYBMUSTJPXWGYBKLSSBDVKPVEAXDGPZXOWPMEGRNSHTJXIUVCXYFTOXMZKIMY
```

Generate 12 words mnemonic with passphrase:
```
$ python -m iota_mnemonic -s 128 -p TREZOR
Mnemonic: broccoli merry lucky milk lizard cannon area utility jelly click bag clever
IOTA Seed: YNONELPCFBKQDDQMIBBBGJDZODCKXEBIJIMXRUGBA9AOPJEQ9SYYLGID9IXHILWVVDJ9ZEGQHCGIHQ9TB
```

Genreate mnemonic with japanese:
```
$ python -m iota_mnemonic -l japanese
Mnemonic: こいぬ　ようちえん　むせん　いんさつ　しなもの　ふのう　かわく　ひかり　はいけん　
そんしつ　たたかう　ちいさい　そうめん　つうわ　にんげん　とおす　さみだれ　かまぼこ　
らくだ　さずかる　ふとる　とんかつ　きびしい　ひつぜん
IOTA Seed: ISBAFGB9LBGOQYGKKMMNK9APICZCGWIJHCMLOLPAQITGSSIGBJJOYQZJJ9NNGYIJLFB9ORMJGCWFFFYQZ
```

Output the mnemonic to file:
```
$ python -m iota_mnemonic -p TREZOR -o mnemonic
```

Recover seed from mnemonic:
```
$ python -m iota_menmonic -p TREZOR -f mnemonic
Mnemonic: often various act decide tongue sausage summer wall priority knock finish until 
taxi robot panic toward giraffe acid avocado anchor travel kiwi actress cream
IOTA Seed: CRGFVETUFKUQYTPTEH9TP9BDKBVZLG9UZJDZBDMMFSSCUPIATPEZMKBLKXOEKCRDFHHFNCCBF9SKHNYIA
```

### Running on docker

Generate 24 words mnemonic and IOTA seed:
```
$ docker run --net=none -it velo/iota-mnemonic
Mnemonic: amused tragic witness trouble foam tomato fabric once peanut air resist change swift logic bundle cube tortoise sunset sock pepper summer bracket coast bullet
IOTA Seed: KOTXEWLFJQQPMZGL9YPKIBMNAOMPJCKQLQJMRBXCHFN9WRRZQLWGEUXN9WMTTQYMC9STCDW9LOTUZ9WGB
```

Any arguments passed after the image name will be passed strait to `iota_menmonic`.

For instance, to generate mnemonic with passphrase:
```
$ docker run --net=none -it velo/iota-mnemonic -p DEMO
Mnemonic: priority exercise can raise provide vicious feel draft perfect mix sand torch december pony glare clown foster airport enemy battle smooth zero solve attack
IOTA Seed: XXGGLHXHZUBFS9INROEPASQPQAWDBNIQI9ADGSAQUYXKOWMRVVNNKZTIWJMCQHNDBLJQCHUATUUIOQAOC
```

#### Why use `--net=none`?

This is a safeguard to prevent any seed leakage. `--net=none` means no networking at all.

## How it works?

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

## Security tips:

* Run this on a offline computer
* Look at the code, don't trust my blue eyes
* Test this, create a mnemonic, restore seed from mnemonic. Play around, get confortable with the tool before you use to generate your real mnemonic/seed
* Safely store your backups
