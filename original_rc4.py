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
    s_box = list(range(256))  # Create the initial S-box values from 0 to 255.
    j = 0  # Start index j at 0.
    for i in range(256):  # Loop through all S-box positions.
        j = (j + s_box[i] + key[i % len(key)]) % 256  # Update j using key mixing.
        swap_temp = s_box[i]  # Temporarily store the current i value.
        s_box[i] = s_box[j]  # Put value from position j into position i.
        s_box[j] = swap_temp  # Put original i value into position j.
    return s_box  # Return the shuffled S-box.


def prga(s_box: list, length: int) -> list:
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
    for _ in range(length):  # Generate the requested number of bytes.
        i = (i + 1) % 256  # Move i forward in a circular way.
        j = (j + s_box[i]) % 256  # Update j using current S-box value.
        swap_temp = s_box[i]  # Store value at i before swapping.
        s_box[i] = s_box[j]  # Move value at j into i.
        s_box[j] = swap_temp  # Move original i value into j.
        t = (s_box[i] + s_box[j]) % 256  # Compute the lookup index t.
        keystream.append(s_box[t])  # Add one keystream byte.
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
    s_box = ksa(key)  # Build the shuffled S-box from the key.
    keystream = prga(s_box, len(data))  # Generate keystream matching input length.
    output_bytes = []  # Create a list to store XOR results.
    for data_byte, key_byte in zip(data, keystream):  # Process each byte pair.
        output_bytes.append(data_byte ^ key_byte)  # XOR data with keystream byte.
    return bytes(output_bytes)  # Convert list to bytes and return.
