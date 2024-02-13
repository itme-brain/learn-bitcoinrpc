import sys

def bech32_polymod(values):
    """Internal function that computes the Bech32 checksum."""
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    checksum = 1
    for value in values:
        top = checksum >> 25
        checksum = ((checksum & 0x1ffffff) << 5) ^ value
        for i in range(5):
            if top >> i & 1:
                checksum ^= generator[i]
    return checksum

def bech32_hrp_expand(hrp):
    """Expand the HRP into values for checksum computation."""
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]

def bech32_create_checksum(hrp, data):
    """Compute the checksum values given HRP and data."""
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

def bech32_encode(hrp, data):
    """Encode a Bech32 string."""
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + '1' + ''.join('qpzry9x8gf2tvdw0s3jn54khce6mua7l'[d] for d in combined)

def convertbits(data, frombits, tobits, pad=True):
    """General power-of-2 base conversion."""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad and bits:
        ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret

def encode_bech32(raw_pubkey, hrp='bc'):
    """Encode a raw public key using Bech32."""
    pubkey_bytes = bytes.fromhex(raw_pubkey)
    data = convertbits(pubkey_bytes, 8, 5)
    if data is None:
        raise ValueError("Data conversion failed")
    return bech32_encode(hrp, data)

def main():
    if len(sys.argv) != 2:
        print("Usage: python bech32_encode.py <raw_pubkey>")
        sys.exit(1)

    raw_pubkey = sys.argv[1]
    try:
        bech32_encoded = encode_bech32(raw_pubkey)
        print(bech32_encoded)
    except ValueError as e:
        print("Error encoding public key:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
