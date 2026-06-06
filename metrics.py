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
        test_key = b"TestKey123"  # Define a fixed test key.
        input_sizes = [1000, 10000, 100000, 1000000]  # Define input sizes in bytes.
        original_times_ms = []  # Store timing results for Original RC4 (milliseconds).
        enhanced_times_ms = []  # Store timing results for Enhanced RC4 (milliseconds).
        for size_bytes in input_sizes:  # Loop through every test size.
            random_data = os.urandom(size_bytes)  # Generate random bytes for fair testing.
            start_time = time.perf_counter()  # Capture start time for Original RC4.
            _ = original_rc4.encrypt_decrypt(random_data, test_key)  # Run Original RC4 encryption.
            end_time = time.perf_counter()  # Capture end time for Original RC4.
            original_times_ms.append((end_time - start_time) * 1000.0)  # Store milliseconds.
            start_time = time.perf_counter()  # Capture start time for Enhanced RC4.
            _ = enhanced_rc4.encrypt_decrypt(random_data, test_key)  # Run Enhanced RC4 encryption.
            end_time = time.perf_counter()  # Capture end time for Enhanced RC4.
            enhanced_times_ms.append((end_time - start_time) * 1000.0)  # Store milliseconds.
        print("Size (bytes) | Original (ms) | Enhanced (ms)")  # Print table header.
        for size_bytes, orig_ms, enh_ms in zip(input_sizes, original_times_ms, enhanced_times_ms):  # Loop through table rows.
            print(f"{size_bytes:12d} | {orig_ms:13.3f} | {enh_ms:13.3f}")  # Print one formatted row.
        print("[Execution Time] Measurement complete.")  # Confirm metric end.
        return input_sizes, original_times_ms, enhanced_times_ms  # Return results for charting.
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
        base_key = b"SecretKey"  # Define the base key.
        flipped_key = bytearray(base_key)  # Copy key into mutable form.
        flipped_key[0] = flipped_key[0] ^ 0b00000001  # Flip first bit of first byte.
        flipped_key = bytes(flipped_key)  # Convert modified key back to bytes.
        cipher_original_base = original_rc4.encrypt_decrypt(plaintext, base_key)  # Encrypt with base key.
        cipher_original_flipped = original_rc4.encrypt_decrypt(plaintext, flipped_key)  # Encrypt with bit-flipped key.
        cipher_enhanced_base = enhanced_rc4.encrypt_decrypt(plaintext, base_key)  # Encrypt with base key.
        cipher_enhanced_flipped = enhanced_rc4.encrypt_decrypt(plaintext, flipped_key)  # Encrypt with bit-flipped key.
        total_bits = len(plaintext) * 8  # Compute total compared bits.
        original_bit_differences = 0  # Count differing bits for Original RC4.
        enhanced_bit_differences = 0  # Count differing bits for Enhanced RC4.
        for b1, b2 in zip(cipher_original_base, cipher_original_flipped):  # Compare Original RC4 ciphertext pairs.
            original_bit_differences += (b1 ^ b2).bit_count()  # Add number of changed bits.
        for b1, b2 in zip(cipher_enhanced_base, cipher_enhanced_flipped):  # Compare Enhanced RC4 ciphertext pairs.
            enhanced_bit_differences += (b1 ^ b2).bit_count()  # Add number of changed bits.
        original_percent = (original_bit_differences / total_bits) * 100.0  # Convert Original diff to percent.
        enhanced_percent = (enhanced_bit_differences / total_bits) * 100.0  # Convert Enhanced diff to percent.
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
        test_key = b"TestKey123"  # Define a fixed test key.
        keystream_length = 10000  # Set number of bytes for entropy analysis.
        original_stream = original_rc4.prga(original_rc4.ksa(test_key), keystream_length)  # Generate Original keystream.
        enhanced_stream = enhanced_rc4.enhanced_prga(enhanced_rc4.enhanced_ksa(test_key), keystream_length)  # Generate Enhanced keystream.
        original_freq_counts = [0] * 256  # Create 256 counters for Original bytes.
        enhanced_freq_counts = [0] * 256  # Create 256 counters for Enhanced bytes.
        for byte_value in original_stream:  # Count Original byte frequencies.
            original_freq_counts[byte_value] += 1  # Increment matching byte counter.
        for byte_value in enhanced_stream:  # Count Enhanced byte frequencies.
            enhanced_freq_counts[byte_value] += 1  # Increment matching byte counter.
        original_entropy = 0.0  # Initialize Original entropy accumulator.
        enhanced_entropy = 0.0  # Initialize Enhanced entropy accumulator.
        for count_value in original_freq_counts:  # Loop through Original frequency counts.
            if count_value > 0:  # Avoid log2(0) by checking positive counts.
                probability = count_value / keystream_length  # Compute probability of byte.
                original_entropy -= probability * math.log2(probability)  # Apply Shannon formula term.
        for count_value in enhanced_freq_counts:  # Loop through Enhanced frequency counts.
            if count_value > 0:  # Avoid log2(0) by checking positive counts.
                probability = count_value / keystream_length  # Compute probability of byte.
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
        test_key = b"TestKey123"  # Define a fixed test key.
        stream_length = 10000  # Set number of bytes for frequency analysis.
        original_stream = original_rc4.prga(original_rc4.ksa(test_key), stream_length)  # Generate Original keystream.
        enhanced_stream = enhanced_rc4.enhanced_prga(enhanced_rc4.enhanced_ksa(test_key), stream_length)  # Generate Enhanced keystream.
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
        test_key = b"TestKey123"  # Define a fixed test key.
        stream_length = 10000  # Set number of bytes for correlation analysis.
        original_stream = original_rc4.prga(original_rc4.ksa(test_key), stream_length)  # Generate Original keystream.
        enhanced_stream = enhanced_rc4.enhanced_prga(enhanced_rc4.enhanced_ksa(test_key), stream_length)  # Generate Enhanced keystream.
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
