import mnemonic
import secp256k1
import bip_utils

bip39WordList = mnemonic.Mnemonic("english")

words = bip39WordList.generate(256)

print(words)
