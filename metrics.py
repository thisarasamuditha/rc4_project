"""Evaluation functions for comparing Original RC4 and Enhanced RC4."""

import math
import os
import time

import numpy as np

import enhanced_rc4
import original_rc4


def measure_execution_time():
    """
    Measures encryption runtime for different input sizes using both RC4 versions.

    Parameters:
    None

    Returns:
    tuple: (sizes, original_times, enhanced_times) where times are in milliseconds.
    """
    try:
        print("\n[Execution Time] Measuring encryption time for multiple data sizes...")  # Explain metric start.
        key = b"TestKey123"  # Define a fixed test key.
        sizes = [1000, 10000, 100000, 1000000]  # Define input sizes in bytes.
        original_times = []  # Store timing results for Original RC4.
        enhanced_times = []  # Store timing results for Enhanced RC4.
        for size in sizes:  # Loop through every test size.
            test_data = os.urandom(size)  # Generate random bytes for fair testing.
            start_time = time.perf_counter()  # Capture start time for Original RC4.
            _ = original_rc4.encrypt_decrypt(test_data, key)  # Run Original RC4 encryption.
            end_time = time.perf_counter()  # Capture end time for Original RC4.
            original_times.append((end_time - start_time) * 1000.0)  # Store milliseconds.
            start_time = time.perf_counter()  # Capture start time for Enhanced RC4.
            _ = enhanced_rc4.encrypt_decrypt(test_data, key)  # Run Enhanced RC4 encryption.
            end_time = time.perf_counter()  # Capture end time for Enhanced RC4.
            enhanced_times.append((end_time - start_time) * 1000.0)  # Store milliseconds.
        print("Size (bytes) | Original (ms) | Enhanced (ms)")  # Print table header.
        for size, orig, enh in zip(sizes, original_times, enhanced_times):  # Loop through table rows.
            print(f"{size:12d} | {orig:13.3f} | {enh:13.3f}")  # Print one formatted row.
        print("[Execution Time] Measurement complete.")  # Confirm metric end.
        return sizes, original_times, enhanced_times  # Return results for charting.
    except Exception as error:
        print(f"Friendly Error: Failed to measure execution time. Details: {error}")  # Print safe error.
        return [1000, 10000, 100000, 1000000], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]  # Return defaults.


def measure_avalanche_effect():
    """
    Measures avalanche effect by flipping one key bit and comparing ciphertext bits.

    Parameters:
    None

    Returns:
    tuple: (original_percent, enhanced_percent) avalanche percentages.
    """
    try:
        print("\n[Avalanche Effect] Measuring bit changes after one key-bit flip...")  # Explain metric start.
        plaintext = b"A" * 256  # Create fixed plaintext for controlled comparison.
        original_key = b"SecretKey"  # Define the base key.
        modified_key = bytearray(original_key)  # Copy key into mutable form.
        modified_key[0] = modified_key[0] ^ 0b00000001  # Flip first bit of first byte.
        modified_key = bytes(modified_key)  # Convert modified key back to bytes.
        cipher_original_1 = original_rc4.encrypt_decrypt(plaintext, original_key)  # Encrypt with base key.
        cipher_original_2 = original_rc4.encrypt_decrypt(plaintext, modified_key)  # Encrypt with bit-flipped key.
        cipher_enhanced_1 = enhanced_rc4.encrypt_decrypt(plaintext, original_key)  # Encrypt with base key.
        cipher_enhanced_2 = enhanced_rc4.encrypt_decrypt(plaintext, modified_key)  # Encrypt with bit-flipped key.
        total_bits = len(plaintext) * 8  # Compute total compared bits.
        orig_diff = 0  # Count differing bits for Original RC4.
        enh_diff = 0  # Count differing bits for Enhanced RC4.
        for byte_a, byte_b in zip(cipher_original_1, cipher_original_2):  # Compare Original RC4 ciphertext pairs.
            orig_diff += (byte_a ^ byte_b).bit_count()  # Add number of changed bits.
        for byte_a, byte_b in zip(cipher_enhanced_1, cipher_enhanced_2):  # Compare Enhanced RC4 ciphertext pairs.
            enh_diff += (byte_a ^ byte_b).bit_count()  # Add number of changed bits.
        original_percent = (orig_diff / total_bits) * 100.0  # Convert Original diff to percent.
        enhanced_percent = (enh_diff / total_bits) * 100.0  # Convert Enhanced diff to percent.
        print(f"Original RC4 Avalanche: {original_percent:.2f}%")  # Print Original result.
        print(f"Enhanced RC4 Avalanche: {enhanced_percent:.2f}%")  # Print Enhanced result.
        print("[Avalanche Effect] Measurement complete.")  # Confirm metric end.
        return original_percent, enhanced_percent  # Return values for charting.
    except Exception as error:
        print(f"Friendly Error: Failed to measure avalanche effect. Details: {error}")  # Print safe error.
        return 0.0, 0.0  # Return defaults.


def measure_entropy():
    """
    Measures Shannon entropy of generated keystream bytes for both RC4 versions.

    Parameters:
    None

    Returns:
    tuple: (original_entropy, enhanced_entropy) in bits.
    """
    try:
        print("\n[Entropy] Measuring Shannon entropy of keystream bytes...")  # Explain metric start.
        key = b"TestKey123"  # Define a fixed test key.
        stream_length = 10000  # Set number of bytes for entropy analysis.
        original_stream = original_rc4.prga(original_rc4.ksa(key), stream_length)  # Generate Original keystream.
        enhanced_stream = enhanced_rc4.enhanced_prga(enhanced_rc4.enhanced_ksa(key), stream_length)  # Generate Enhanced keystream.
        original_counts = [0] * 256  # Create 256 counters for Original bytes.
        enhanced_counts = [0] * 256  # Create 256 counters for Enhanced bytes.
        for byte_value in original_stream:  # Count Original byte frequencies.
            original_counts[byte_value] += 1  # Increment matching byte counter.
        for byte_value in enhanced_stream:  # Count Enhanced byte frequencies.
            enhanced_counts[byte_value] += 1  # Increment matching byte counter.
        original_entropy = 0.0  # Initialize Original entropy accumulator.
        enhanced_entropy = 0.0  # Initialize Enhanced entropy accumulator.
        for count_value in original_counts:  # Loop through Original frequency counts.
            if count_value > 0:  # Avoid log2(0) by checking positive counts.
                probability = count_value / stream_length  # Compute probability of byte.
                original_entropy -= probability * math.log2(probability)  # Apply Shannon formula term.
        for count_value in enhanced_counts:  # Loop through Enhanced frequency counts.
            if count_value > 0:  # Avoid log2(0) by checking positive counts.
                probability = count_value / stream_length  # Compute probability of byte.
                enhanced_entropy -= probability * math.log2(probability)  # Apply Shannon formula term.
        print(f"Original RC4 Entropy: {original_entropy:.4f} bits (Ideal: 8.0)")  # Print Original result.
        print(f"Enhanced RC4 Entropy: {enhanced_entropy:.4f} bits (Ideal: 8.0)")  # Print Enhanced result.
        print("[Entropy] Measurement complete.")  # Confirm metric end.
        return original_entropy, enhanced_entropy  # Return entropy values.
    except Exception as error:
        print(f"Friendly Error: Failed to measure entropy. Details: {error}")  # Print safe error.
        return 0.0, 0.0  # Return defaults.


def measure_frequency_distribution():
    """
    Counts byte frequencies in keystream output to inspect distribution uniformity.

    Parameters:
    None

    Returns:
    tuple: (original_frequencies, enhanced_frequencies) lists of 256 counts.
    """
    try:
        print("\n[Frequency Distribution] Counting keystream byte frequencies...")  # Explain metric start.
        key = b"TestKey123"  # Define a fixed test key.
        stream_length = 10000  # Set number of bytes for frequency analysis.
        original_stream = original_rc4.prga(original_rc4.ksa(key), stream_length)  # Generate Original keystream.
        enhanced_stream = enhanced_rc4.enhanced_prga(enhanced_rc4.enhanced_ksa(key), stream_length)  # Generate Enhanced keystream.
        original_frequencies = [0] * 256  # Create 256 counters for Original bytes.
        enhanced_frequencies = [0] * 256  # Create 256 counters for Enhanced bytes.
        for byte_value in original_stream:  # Count Original byte frequencies.
            original_frequencies[byte_value] += 1  # Increment matching byte counter.
        for byte_value in enhanced_stream:  # Count Enhanced byte frequencies.
            enhanced_frequencies[byte_value] += 1  # Increment matching byte counter.
        original_min = min(original_frequencies)  # Find smallest Original count.
        original_max = max(original_frequencies)  # Find largest Original count.
        original_avg = sum(original_frequencies) / 256.0  # Compute Original average count.
        enhanced_min = min(enhanced_frequencies)  # Find smallest Enhanced count.
        enhanced_max = max(enhanced_frequencies)  # Find largest Enhanced count.
        enhanced_avg = sum(enhanced_frequencies) / 256.0  # Compute Enhanced average count.
        print(f"Original RC4 -> min: {original_min}, max: {original_max}, avg: {original_avg:.2f}")  # Print Original stats.
        print(f"Enhanced RC4 -> min: {enhanced_min}, max: {enhanced_max}, avg: {enhanced_avg:.2f}")  # Print Enhanced stats.
        print("[Frequency Distribution] Measurement complete.")  # Confirm metric end.
        return original_frequencies, enhanced_frequencies  # Return frequency lists.
    except Exception as error:
        print(f"Friendly Error: Failed to measure frequency distribution. Details: {error}")  # Print safe error.
        return [0] * 256, [0] * 256  # Return defaults.


def measure_correlation():
    """
    Measures correlation between consecutive keystream bytes for both RC4 versions.

    Parameters:
    None

    Returns:
    tuple: (original_correlation, enhanced_correlation) float coefficients.
    """
    try:
        print("\n[Correlation] Measuring relation between consecutive keystream bytes...")  # Explain metric start.
        key = b"TestKey123"  # Define a fixed test key.
        stream_length = 10000  # Set number of bytes for correlation analysis.
        original_stream = original_rc4.prga(original_rc4.ksa(key), stream_length)  # Generate Original keystream.
        enhanced_stream = enhanced_rc4.enhanced_prga(enhanced_rc4.enhanced_ksa(key), stream_length)  # Generate Enhanced keystream.
        original_x = np.array(original_stream[:-1], dtype=float)  # Create Original first-shift array.
        original_y = np.array(original_stream[1:], dtype=float)  # Create Original second-shift array.
        enhanced_x = np.array(enhanced_stream[:-1], dtype=float)  # Create Enhanced first-shift array.
        enhanced_y = np.array(enhanced_stream[1:], dtype=float)  # Create Enhanced second-shift array.
        original_correlation = float(np.corrcoef(original_x, original_y)[0, 1])  # Compute Original correlation.
        enhanced_correlation = float(np.corrcoef(enhanced_x, enhanced_y)[0, 1])  # Compute Enhanced correlation.
        print(f"Original RC4 Correlation: {original_correlation:.6f}")  # Print Original result.
        print(f"Enhanced RC4 Correlation: {enhanced_correlation:.6f}")  # Print Enhanced result.
        print("[Correlation] Measurement complete.")  # Confirm metric end.
        return original_correlation, enhanced_correlation  # Return correlation values.
    except Exception as error:
        print(f"Friendly Error: Failed to measure correlation. Details: {error}")  # Print safe error.
        return 0.0, 0.0  # Return defaults.
