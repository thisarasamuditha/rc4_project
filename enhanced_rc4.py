"""Enhanced RC4 implementation with improved mixing and bias reduction."""


def enhanced_ksa(key: bytes) -> list:
    """
    Enhanced Key Scheduling Algorithm with DOUBLE KEY MIXING.
    Improvement over original: The S-box is shuffled TWICE using the key.
    - First pass: shuffle using key in normal order (same as original KSA)
    - Second pass: shuffle again using key in REVERSE order
    This extra pass makes the S-box harder to predict from the key alone.

    Parameters:
    key (bytes): Secret key used for both mixing passes.

    Returns:
    list: A doubly mixed S-box list with 256 integer values.
    """
    state = list(range(256))  # Create the initial state array values from 0 to 255.
    j = 0  # Start index j at 0 for pass 1.
    key_length = len(key)
    for i in range(256):  # First pass uses the normal key order.
        j = (j + state[i] + key[i % key_length]) % 256  # Update j using normal key bytes.
        temp = state[i]  # Store current value before swapping.
        state[i] = state[j]  # Move value at j into position i.
        state[j] = temp  # Move original i value into j.
    reversed_key = key[::-1]  # Create reversed key bytes for extra mixing.
    j = 0  # Reset j before second pass.
    for i in range(256):  # Second pass uses reversed key order.
        j = (j + state[i] + reversed_key[i % key_length]) % 256  # Update j with reversed key.
        temp = state[i]  # Store current value before swapping.
        state[i] = state[j]  # Move value at j into position i.
        state[j] = temp  # Move original i value into j.
    return state  # Return the doubly mixed state array.


def enhanced_prga(state: list, length: int) -> list:
    """
    Enhanced PRGA with BIAS REDUCTION.
    Improvement over original: The first 256 keystream bytes are discarded.
    Why? RC4's early keystream bytes are statistically biased (not truly random).
    Discarding them makes the remaining output much more random and secure.

    Parameters:
    s_box (list): The shuffled S-box from enhanced KSA.
    length (int): Number of useful keystream bytes to return.

    Returns:
    list: Keystream bytes after discarding the first 256 bytes.
    """
    i = 0  # Start index i at 0.
    j = 0  # Start index j at 0.
    # Warm-up: run 256 steps and discard outputs to reduce bias.
    for _warmup in range(256):
        i = (i + 1) % 256  # Move i forward in a circular way.
        j = (j + state[i]) % 256  # Update j using current state value.
        temp = state[i]  # Store current value before swapping.
        state[i] = state[j]  # Move value at j into position i.
        state[j] = temp  # Move original i value into j.
        discard_index = (state[i] + state[j]) % 256  # Compute output index for discard.
        _discarded = state[discard_index]  # Read and discard this warm-up byte.
    keystream = []  # Create a list to hold final keystream bytes.
    for _count in range(length):  # Generate requested useful output bytes.
        i = (i + 1) % 256  # Move i forward in a circular way.
        j = (j + state[i]) % 256  # Update j using current state value.
        temp = state[i]  # Store current value before swapping.
        state[i] = state[j]  # Move value at j into position i.
        state[j] = temp  # Move original i value into j.
        output_index = (state[i] + state[j]) % 256  # Compute output index.
        keystream.append(state[output_index])  # Add one useful keystream byte.
    return keystream  # Return only the useful bytes.


def encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    """
    Encrypts OR decrypts data using Enhanced RC4.
    Uses enhanced_ksa and enhanced_prga instead of the originals.

    Parameters:
    data (bytes): Input bytes to encrypt or decrypt.
    key (bytes): Secret key bytes.

    Returns:
    bytes: Output bytes after XOR with enhanced RC4 keystream.
    """
    state = enhanced_ksa(key)  # Build the enhanced shuffled state array.
    keystream = enhanced_prga(state, len(data))  # Generate enhanced keystream.
    output_bytes = []  # Create a list to store XOR results.
    for plain_byte, keystream_byte in zip(data, keystream):  # Process each byte pair.
        output_bytes.append(plain_byte ^ keystream_byte)  # XOR data with keystream byte.
    return bytes(output_bytes)  # Convert list to bytes and return.
