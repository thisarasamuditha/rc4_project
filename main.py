# ═══════════════════════════════════════════════════
# HOW TO SET UP AND RUN THIS PROJECT
# ═══════════════════════════════════════════════════
# FIRST TIME ONLY — Run the setup script:
#   python setup.py
#
# This will:
#   - Create a virtual environment (venv/)
#   - Install numpy and matplotlib automatically
#   - Create the output_charts/ folder
#
# Then activate the virtual environment:
#   Windows:    venv\Scripts\activate
#   Mac/Linux:  source venv/bin/activate
#
# Finally, run the project:
#   python main.py
#
# To deactivate the venv when done:
#   deactivate
# ═══════════════════════════════════════════════════

import charts
import enhanced_rc4
import metrics
import original_rc4


def show_header():
    """
    Displays the project title banner at program start.

    Parameters:
    None

    Returns:
    None
    """
    print("╔══════════════════════════════════════════╗")  # Print top border of header.
    print("║  Enhanced RC4 - Information Security     ║")  # Print project title.
    print("║  Academic Project                        ║")  # Print subtitle.
    print("╚══════════════════════════════════════════╝")  # Print bottom border of header.


def show_menu():
    """
    Displays the main menu options for encryption, decryption, and evaluation.

    Parameters:
    None

    Returns:
    None
    """
    print("\nChoose an option:")  # Print menu prompt.
    print("[1] Encrypt a message (Original RC4)")  # Print option 1.
    print("[2] Encrypt a message (Enhanced RC4)")  # Print option 2.
    print("[3] Decrypt a message (Original RC4)")  # Print option 3.
    print("[4] Decrypt a message (Enhanced RC4)")  # Print option 4.
    print("[5] Run all evaluations + generate charts")  # Print option 5.
    print("[6] Exit")  # Print option 6.


def run_encrypt(is_enhanced: bool):
    """
    Encrypts a user-provided plaintext message with selected RC4 version.

    Parameters:
    is_enhanced (bool): True for Enhanced RC4, False for Original RC4.

    Returns:
    None
    """
    try:
        message = input("Enter message to encrypt: ")  # Ask user for plaintext input.
        key_text = input("Enter key: ")  # Ask user for key input.
        data_bytes = message.encode("utf-8")  # Convert message text into bytes.
        key_bytes = key_text.encode("utf-8")  # Convert key text into bytes.
        if is_enhanced:  # Check if Enhanced RC4 should be used.
            cipher_bytes = enhanced_rc4.encrypt_decrypt(data_bytes, key_bytes)  # Encrypt with Enhanced RC4.
            print(f"Encrypted HEX (Enhanced RC4): {cipher_bytes.hex()}")  # Print hex ciphertext.
        else:  # Use Original RC4 when enhanced flag is false.
            cipher_bytes = original_rc4.encrypt_decrypt(data_bytes, key_bytes)  # Encrypt with Original RC4.
            print(f"Encrypted HEX (Original RC4): {cipher_bytes.hex()}")  # Print hex ciphertext.
    except Exception as error:
        print(f"Friendly Error: Encryption failed. Details: {error}")  # Print safe encryption error.


def run_decrypt(is_enhanced: bool):
    """
    Decrypts a user-provided HEX ciphertext with selected RC4 version.

    Parameters:
    is_enhanced (bool): True for Enhanced RC4, False for Original RC4.

    Returns:
    None
    """
    try:
        hex_text = input("Enter HEX string to decrypt: ")  # Ask user for hex ciphertext.
        key_text = input("Enter key: ")  # Ask user for key input.
        cipher_bytes = bytes.fromhex(hex_text.strip())  # Convert hex text to raw bytes.
        key_bytes = key_text.encode("utf-8")  # Convert key text into bytes.
        if is_enhanced:  # Check if Enhanced RC4 should be used.
            plain_bytes = enhanced_rc4.encrypt_decrypt(cipher_bytes, key_bytes)  # Decrypt with Enhanced RC4.
            print(f"Decrypted text (Enhanced RC4): {plain_bytes.decode('utf-8', errors='replace')}")  # Print text safely.
        else:  # Use Original RC4 when enhanced flag is false.
            plain_bytes = original_rc4.encrypt_decrypt(cipher_bytes, key_bytes)  # Decrypt with Original RC4.
            print(f"Decrypted text (Original RC4): {plain_bytes.decode('utf-8', errors='replace')}")  # Print text safely.
    except ValueError:
        print("Friendly Error: Invalid HEX input. Please enter a valid hexadecimal string.")  # Print invalid hex error.
    except Exception as error:
        print(f"Friendly Error: Decryption failed. Details: {error}")  # Print safe decryption error.


def run_evaluations_and_charts():
    """
    Runs all metrics, prints a summary table, and saves all chart files.

    Parameters:
    None

    Returns:
    None
    """
    try:
        print("\nRunning all evaluations in order...")  
        sizes, original_times, enhanced_times = metrics.measure_execution_time()  
        original_avalanche, enhanced_avalanche = metrics.measure_avalanche_effect()  
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
        print(f"Friendly Error: Evaluation flow failed. Details: {error}")  # Print safe evaluation error.


def main():
    """
    Runs the interactive menu loop until the user chooses to exit.

    Parameters:
    None

    Returns:
    None
    """
    show_header()  # Display startup header.
    while True:  # Keep showing menu until user exits.
        show_menu()  # Display available options.
        choice = input("Enter option number: ").strip()  # Read user menu choice.
        if choice == "1":  # Handle Original RC4 encryption.
            run_encrypt(is_enhanced=False)  # Call encrypt flow for Original RC4.
        elif choice == "2":  # Handle Enhanced RC4 encryption.
            run_encrypt(is_enhanced=True)  # Call encrypt flow for Enhanced RC4.
        elif choice == "3":  # Handle Original RC4 decryption.
            run_decrypt(is_enhanced=False)  # Call decrypt flow for Original RC4.
        elif choice == "4":  # Handle Enhanced RC4 decryption.
            run_decrypt(is_enhanced=True)  # Call decrypt flow for Enhanced RC4.
        elif choice == "5":  # Handle full evaluation workflow.
            run_evaluations_and_charts()  # Execute all metrics and chart generation.
        elif choice == "6":  # Handle program exit.
            print("Exiting project. Goodbye.")  # Print exit message.
            break  # Stop menu loop.
        else:  # Handle unsupported option input.
            print("Invalid option. Please choose 1, 2, 3, 4, 5, or 6.")  # Print validation message.


if __name__ == "__main__":  # Ensure script runs only when executed directly.
    try:
        main()  # Start the program.
    except Exception as error:
        print(f"Friendly Error: Program stopped unexpectedly. Details: {error}")  # Print safe fatal error.
