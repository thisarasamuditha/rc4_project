def ksa(key: bytes) -> list:
    state = list(range(256))
    j = 0
    key_length = len(key)
    for i in range(256):
        j = (j + state[i] + key[i % key_length]) % 256
        temp = state[i]
        state[i] = state[j]
        state[j] = temp
    return state


def prga(state: list, length: int) -> list:
    i = 0
    j = 0
    keystream = []
    for _count in range(length):
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        temp = state[i]
        state[i] = state[j]
        state[j] = temp
        output_index = (state[i] + state[j]) % 256
        keystream.append(state[output_index])
    return keystream


def encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    state = ksa(key)
    keystream = prga(state, len(data))
    output_bytes = []
    for plain_byte, keystream_byte in zip(data, keystream):
        output_bytes.append(plain_byte ^ keystream_byte)
    return bytes(output_bytes)
