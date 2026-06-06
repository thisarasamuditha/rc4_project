"""Classic RC4 implementation for educational comparison."""


def ksa(key: bytes) -> list:
    """
    Key Scheduling Algorithm (KSA) - Sets up the S-box using the secret key.
    The S-box starts as [0, 1, 2, ..., 255] and gets shuffled based on the key.
    This shuffled S-box is the starting state for generating the keystream.

    Parameters:
    key (bytes): Secret key used to shuffle the S-box.

    Returns:
    list: A shuffled S-box list with 256 integer values.
    """
    state = list(range(256))  # Create the initial state values from 0 to 255.
    j = 0  # Start index j at 0.
    key_length = len(key)
    for i in range(256):  # Loop through all state positions.
        j = (j + state[i] + key[i % key_length]) % 256  # Update j using key mixing.
        temp = state[i]  # Temporarily store the current i value.
        state[i] = state[j]  # Put value from position j into position i.
        state[j] = temp  # Put original i value into position j.
    return state  # Return the shuffled state.


def prga(state: list, length: int) -> list:
    """
    Pseudo-Random Generation Algorithm (PRGA) - Generates the keystream bytes.
    These bytes will be XORed with the plaintext to encrypt it.

    Parameters:
    s_box (list): The shuffled S-box from the KSA step.
    length (int): Number of keystream bytes to generate.

    Returns:
    list: Keystream bytes as a list of integers.
    """
    i = 0  # Start index i at 0.
    j = 0  # Start index j at 0.
    keystream = []  # Create an empty list to hold keystream bytes.
    for _count in range(length):  # Generate the requested number of bytes.
        i = (i + 1) % 256  # Move i forward in a circular way.
        j = (j + state[i]) % 256  # Update j using current state value.
        temp = state[i]  # Store value at i before swapping.
        state[i] = state[j]  # Move value at j into i.
        state[j] = temp  # Move original i value into j.
        output_index = (state[i] + state[j]) % 256  # Compute the lookup index.
        keystream.append(state[output_index])  # Add one keystream byte.
    return keystream  # Return all generated keystream bytes.


def encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    """
    Encrypts OR decrypts data using RC4. Both operations are identical
    because XORing twice with the same keystream returns the original data.

    Parameters:
    data (bytes): Input bytes to encrypt or decrypt.
    key (bytes): Secret key bytes.

    Returns:
    bytes: Output bytes after XOR with RC4 keystream.
    """
    state = ksa(key)  # Build the shuffled state from the key.
    keystream = prga(state, len(data))  # Generate keystream matching input length.
    output_bytes = []  # Create a list to store XOR results.
    for plain_byte, keystream_byte in zip(data, keystream):  # Process each byte pair.
        output_bytes.append(plain_byte ^ keystream_byte)  # XOR data with keystream byte.
    return bytes(output_bytes)  # Convert list to bytes and return.
