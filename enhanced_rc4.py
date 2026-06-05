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
    s_box = list(range(256))  # Create the initial S-box values from 0 to 255.
    j = 0  # Start index j at 0 for pass 1.
    for i in range(256):  # First pass uses the normal key order.
        j = (j + s_box[i] + key[i % len(key)]) % 256  # Update j using normal key bytes.
        swap_temp = s_box[i]  # Store i value before swapping.
        s_box[i] = s_box[j]  # Move j value into i.
        s_box[j] = swap_temp  # Move original i value into j.
    reversed_key = key[::-1]  # Create reversed key bytes for extra mixing.
    j = 0  # Reset j before second pass.
    for i in range(256):  # Second pass uses reversed key order.
        j = (j + s_box[i] + reversed_key[i % len(reversed_key)]) % 256  # Update j with reversed key.
        swap_temp = s_box[i]  # Store i value before swapping.
        s_box[i] = s_box[j]  # Move j value into i.
        s_box[j] = swap_temp  # Move original i value into j.
    return s_box  # Return the doubly mixed S-box.


def enhanced_prga(s_box: list, length: int) -> list:
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
    for _ in range(256):  # Run 256 warm-up steps to discard biased output.
        i = (i + 1) % 256  # Move i forward in a circular way.
        j = (j + s_box[i]) % 256  # Update j using current S-box value.
        swap_temp = s_box[i]  # Store i value before swapping.
        s_box[i] = s_box[j]  # Move j value into i.
        s_box[j] = swap_temp  # Move original i value into j.
        discard_index = (s_box[i] + s_box[j]) % 256  # Compute output index for discard.
        _ = s_box[discard_index]  # Read and discard this warm-up byte.
    keystream = []  # Create a list to hold final keystream bytes.
    for _ in range(length):  # Generate requested useful output bytes.
        i = (i + 1) % 256  # Move i forward in a circular way.
        j = (j + s_box[i]) % 256  # Update j using current S-box value.
        swap_temp = s_box[i]  # Store i value before swapping.
        s_box[i] = s_box[j]  # Move j value into i.
        s_box[j] = swap_temp  # Move original i value into j.
        t = (s_box[i] + s_box[j]) % 256  # Compute output index t.
        keystream.append(s_box[t])  # Add one useful keystream byte.
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
    s_box = enhanced_ksa(key)  # Build the enhanced shuffled S-box.
    keystream = enhanced_prga(s_box, len(data))  # Generate enhanced keystream.
    output_bytes = []  # Create a list to store XOR results.
    for data_byte, key_byte in zip(data, keystream):  # Process each byte pair.
        output_bytes.append(data_byte ^ key_byte)  # XOR data with keystream byte.
    return bytes(output_bytes)  # Convert list to bytes and return.
