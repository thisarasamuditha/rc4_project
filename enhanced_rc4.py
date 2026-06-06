def enhanced_ksa(key: bytes) -> list:
    state = list(range(256))
    j = 0
    key_length = len(key)
    for i in range(256):
        j = (j + state[i] + key[i % key_length]) % 256
        temp = state[i]
        state[i] = state[j]
        state[j] = temp
    reversed_key = key[::-1]
    j = 0
    for i in range(256):
        j = (j + state[i] + reversed_key[i % key_length]) % 256
        temp = state[i]
        state[i] = state[j]
        state[j] = temp
    return state


def enhanced_prga(state: list, length: int) -> list:
    i = 0
    j = 0
    for _warmup in range(256):
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        temp = state[i]
        state[i] = state[j]
        state[j] = temp
        discard_index = (state[i] + state[j]) % 256
        _ = state[discard_index]
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
    state = enhanced_ksa(key)
    keystream = enhanced_prga(state, len(data))
    output_bytes = []
    for plain_byte, keystream_byte in zip(data, keystream):
        output_bytes.append(plain_byte ^ keystream_byte)
    return bytes(output_bytes)
