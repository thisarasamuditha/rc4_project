import charts
import enhanced_rc4
import metrics
import original_rc4


def show_header():
    print("╔══════════════════════════════════════════╗")
    print("║  Enhanced RC4 - Information Security     ║")
    print("║  Academic Project                        ║")
    print("╚══════════════════════════════════════════╝")


def show_menu():
    print("\nChoose an option:")
    print("[1] Encrypt a message (Original RC4)")
    print("[2] Encrypt a message (Enhanced RC4)")
    print("[3] Decrypt a message (Original RC4)")
    print("[4] Decrypt a message (Enhanced RC4)")
    print("[5] Run all evaluations + generate charts")
    print("[6] Exit")


def run_encrypt(is_enhanced: bool):
    try:
        message = input("Enter message to encrypt: ")
        key_text = input("Enter key: ")
        data_bytes = message.encode("utf-8")
        key_bytes = key_text.encode("utf-8")
        if is_enhanced:
            cipher_bytes = enhanced_rc4.encrypt_decrypt(data_bytes, key_bytes)
            print(f"Encrypted HEX (Enhanced RC4): {cipher_bytes.hex()}")
        else:
            cipher_bytes = original_rc4.encrypt_decrypt(data_bytes, key_bytes)
            print(f"Encrypted HEX (Original RC4): {cipher_bytes.hex()}")
    except Exception as error:
        print(f"Friendly Error: Encryption failed. Details: {error}")


def run_decrypt(is_enhanced: bool):
    try:
        hex_text = input("Enter HEX string to decrypt: ")
        key_text = input("Enter key: ")
        cipher_bytes = bytes.fromhex(hex_text.strip())
        key_bytes = key_text.encode("utf-8")
        if is_enhanced:
            plain_bytes = enhanced_rc4.encrypt_decrypt(cipher_bytes, key_bytes)
            print(f"Decrypted text (Enhanced RC4): {plain_bytes.decode('utf-8', errors='replace')}")
        else:
            plain_bytes = original_rc4.encrypt_decrypt(cipher_bytes, key_bytes)
            print(f"Decrypted text (Original RC4): {plain_bytes.decode('utf-8', errors='replace')}")
    except ValueError:
        print("Friendly Error: Invalid HEX input. Please enter a valid hexadecimal string.")
    except Exception as error:
        print(f"Friendly Error: Decryption failed. Details: {error}")


def run_evaluations_and_charts():
    """
    Runs all metrics, prints a summary table, and saves all chart files.

    Parameters:
    None

    Returns:
    None
    """
    try:
        print("\nRunning all evaluations in order...")  # Announce evaluation start.
        sizes, original_times, enhanced_times = metrics.measure_execution_time()  # Run execution time metric.
        original_avalanche, enhanced_avalanche = metrics.measure_avalanche_effect()  # Run avalanche metric.
        original_entropy, enhanced_entropy = metrics.measure_entropy()  # Run entropy metric.
        original_freq, enhanced_freq = metrics.measure_frequency_distribution()  # Run frequency metric.
        original_corr, enhanced_corr = metrics.measure_correlation()  # Run correlation metric.
        print("\n╔══════════════════════════════════════════════════════════╗")  # Print summary top border.
        print("║              EVALUATION RESULTS SUMMARY                  ║")  # Print summary title.
        print("╠══════════════════╦══════════════════╦════════════════════╣")  # Print summary header divider.
        print("║ Metric           ║  Original RC4    ║  Enhanced RC4      ║")  # Print summary header labels.
        print("╠══════════════════╬══════════════════╬════════════════════╣")  # Print summary column divider.
        print(f"║ Entropy          ║    {original_entropy:>5.2f} bits     ║    {enhanced_entropy:>5.2f} bits       ║")  # Print entropy row.
        print(f"║ Avalanche Effect ║    {original_avalanche:>6.2f}%      ║    {enhanced_avalanche:>6.2f}%          ║")  # Print avalanche row.
        print(f"║ Correlation      ║    {original_corr:>8.5f}      ║    {enhanced_corr:>8.5f}        ║")  # Print correlation row.
        print("╚══════════════════╩══════════════════╩════════════════════╝")  # Print summary bottom border.
        charts.plot_execution_time(sizes, original_times, enhanced_times)  # Save execution time chart.
        charts.plot_avalanche(original_avalanche, enhanced_avalanche)  # Save avalanche chart.
        charts.plot_entropy(original_entropy, enhanced_entropy)  # Save entropy chart.
        charts.plot_frequency_distribution(original_freq, enhanced_freq)  # Save frequency chart.
        charts.plot_correlation(original_corr, enhanced_corr)  # Save correlation chart.
        print("All charts saved to output_charts/ folder")  # Confirm all charts saved.
    except Exception as error:
        print(f"Friendly Error: Evaluation flow failed. Details: {error}")


def main():
    show_header()
    while True:
        show_menu()
        choice = input("Enter option number: ").strip()
        if choice == "1":
            run_encrypt(is_enhanced=False)
        elif choice == "2":
            run_encrypt(is_enhanced=True)
        elif choice == "3":
            run_decrypt(is_enhanced=False)
        elif choice == "4":
            run_decrypt(is_enhanced=True)
        elif choice == "5":
            run_evaluations_and_charts()
        elif choice == "6":
            print("Exiting project. Goodbye.")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, 4, 5, or 6.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Friendly Error: Program stopped unexpectedly. Details: {error}")
