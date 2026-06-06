import math
import os
import time

import numpy as np

import enhanced_rc4
import original_rc4


def measure_execution_time():
    try:
        print("\n[Execution Time] Measuring encryption time for multiple data sizes...")
        test_key = b"TestKey123"
        input_sizes = [1000, 10000, 100000, 1000000]
        original_times_ms = []
        enhanced_times_ms = []
        for size_bytes in input_sizes:
            random_data = os.urandom(size_bytes)
            start_time = time.perf_counter()
            _ = original_rc4.encrypt_decrypt(random_data, test_key)
            end_time = time.perf_counter()
            original_times_ms.append((end_time - start_time) * 1000.0)
            start_time = time.perf_counter()
            _ = enhanced_rc4.encrypt_decrypt(random_data, test_key)
            end_time = time.perf_counter()
            enhanced_times_ms.append((end_time - start_time) * 1000.0)
        print("Size (bytes) | Original (ms) | Enhanced (ms)")
        for size_bytes, orig_ms, enh_ms in zip(input_sizes, original_times_ms, enhanced_times_ms):
            print(f"{size_bytes:12d} | {orig_ms:13.3f} | {enh_ms:13.3f}")
        print("[Execution Time] Measurement complete.")
        return input_sizes, original_times_ms, enhanced_times_ms
    except Exception as error:
        print(f"Friendly Error: Failed to measure execution time. Details: {error}")
        return [1000, 10000, 100000, 1000000], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]


def measure_avalanche_effect():
    try:
        print("\n[Avalanche Effect] Measuring bit changes after one key-bit flip...")
        plaintext = b"A" * 256
        base_key = b"SecretKey"
        flipped_key = bytearray(base_key)
        flipped_key[0] = flipped_key[0] ^ 0b00000001
        flipped_key = bytes(flipped_key)
        cipher_original_base = original_rc4.encrypt_decrypt(plaintext, base_key)
        cipher_original_flipped = original_rc4.encrypt_decrypt(plaintext, flipped_key)
        cipher_enhanced_base = enhanced_rc4.encrypt_decrypt(plaintext, base_key)
        cipher_enhanced_flipped = enhanced_rc4.encrypt_decrypt(plaintext, flipped_key)
        total_bits = len(plaintext) * 8
        original_bit_differences = 0
        enhanced_bit_differences = 0
        for b1, b2 in zip(cipher_original_base, cipher_original_flipped):
            original_bit_differences += (b1 ^ b2).bit_count()
        for b1, b2 in zip(cipher_enhanced_base, cipher_enhanced_flipped):
            enhanced_bit_differences += (b1 ^ b2).bit_count()
        original_percent = (original_bit_differences / total_bits) * 100.0
        enhanced_percent = (enhanced_bit_differences / total_bits) * 100.0
        print(f"Original RC4 Avalanche: {original_percent:.2f}%")
        print(f"Enhanced RC4 Avalanche: {enhanced_percent:.2f}%")
        print("[Avalanche Effect] Measurement complete.")
        return original_percent, enhanced_percent
    except Exception as error:
        print(f"Friendly Error: Failed to measure avalanche effect. Details: {error}")
        return 0.0, 0.0


def measure_entropy():
    try:
        print("\n[Entropy] Measuring Shannon entropy of keystream bytes...")
        test_key = b"TestKey123"
        keystream_length = 10000
        original_stream = original_rc4.prga(original_rc4.ksa(test_key), keystream_length)
        enhanced_stream = enhanced_rc4.enhanced_prga(enhanced_rc4.enhanced_ksa(test_key), keystream_length)
        original_freq_counts = [0] * 256
        enhanced_freq_counts = [0] * 256
        for byte_value in original_stream:
            original_freq_counts[byte_value] += 1
        for byte_value in enhanced_stream:
            enhanced_freq_counts[byte_value] += 1
        original_entropy = 0.0
        enhanced_entropy = 0.0
        for count_value in original_freq_counts:
            if count_value > 0:
                probability = count_value / keystream_length
                original_entropy -= probability * math.log2(probability)
        for count_value in enhanced_freq_counts:
            if count_value > 0:
                probability = count_value / keystream_length
                enhanced_entropy -= probability * math.log2(probability)
        print(f"Original RC4 Entropy: {original_entropy:.4f} bits (Ideal: 8.0)")
        print(f"Enhanced RC4 Entropy: {enhanced_entropy:.4f} bits (Ideal: 8.0)")
        print("[Entropy] Measurement complete.")
        return original_entropy, enhanced_entropy
    except Exception as error:
        print(f"Friendly Error: Failed to measure entropy. Details: {error}")
        return 0.0, 0.0


def measure_frequency_distribution():
    try:
        print("\n[Frequency Distribution] Counting keystream byte frequencies...")
        test_key = b"TestKey123"
        stream_length = 10000
        original_stream = original_rc4.prga(original_rc4.ksa(test_key), stream_length)
        enhanced_stream = enhanced_rc4.enhanced_prga(enhanced_rc4.enhanced_ksa(test_key), stream_length)
        original_frequencies = [0] * 256
        enhanced_frequencies = [0] * 256
        for byte_value in original_stream:
            original_frequencies[byte_value] += 1
        for byte_value in enhanced_stream:
            enhanced_frequencies[byte_value] += 1
        original_min = min(original_frequencies)
        original_max = max(original_frequencies)
        original_avg = sum(original_frequencies) / 256.0
        enhanced_min = min(enhanced_frequencies)
        enhanced_max = max(enhanced_frequencies)
        enhanced_avg = sum(enhanced_frequencies) / 256.0
        print(f"Original RC4 -> min: {original_min}, max: {original_max}, avg: {original_avg:.2f}")
        print(f"Enhanced RC4 -> min: {enhanced_min}, max: {enhanced_max}, avg: {enhanced_avg:.2f}")
        print("[Frequency Distribution] Measurement complete.")
        return original_frequencies, enhanced_frequencies
    except Exception as error:
        print(f"Friendly Error: Failed to measure frequency distribution. Details: {error}")
        return [0] * 256, [0] * 256


def measure_correlation():
    try:
        print("\n[Correlation] Measuring relation between consecutive keystream bytes...")
        test_key = b"TestKey123"
        stream_length = 10000
        original_stream = original_rc4.prga(original_rc4.ksa(test_key), stream_length)
        enhanced_stream = enhanced_rc4.enhanced_prga(enhanced_rc4.enhanced_ksa(test_key), stream_length)
        original_x = np.array(original_stream[:-1], dtype=float)
        original_y = np.array(original_stream[1:], dtype=float)
        enhanced_x = np.array(enhanced_stream[:-1], dtype=float)
        enhanced_y = np.array(enhanced_stream[1:], dtype=float)
        original_correlation = float(np.corrcoef(original_x, original_y)[0, 1])
        enhanced_correlation = float(np.corrcoef(enhanced_x, enhanced_y)[0, 1])
        print(f"Original RC4 Correlation: {original_correlation:.6f}")
        print(f"Enhanced RC4 Correlation: {enhanced_correlation:.6f}")
        print("[Correlation] Measurement complete.")
        return original_correlation, enhanced_correlation
    except Exception as error:
        print(f"Friendly Error: Failed to measure correlation. Details: {error}")
        return 0.0, 0.0
