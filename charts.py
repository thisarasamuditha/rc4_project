"""Chart generation functions for RC4 metric comparisons."""

import os

import matplotlib.pyplot as plt


def plot_execution_time(sizes, orig_times, enh_times):
    """
    Creates a line chart of encryption execution time across input sizes.

    Parameters:
    sizes (list): Input sizes in bytes.
    orig_times (list): Execution times for Original RC4 in milliseconds.
    enh_times (list): Execution times for Enhanced RC4 in milliseconds.

    Returns:
    str: File path of the saved chart image.
    """
    try:
        print("[Chart] Creating execution time chart...")  # Announce chart creation.
        os.makedirs("output_charts", exist_ok=True)  # Ensure output folder exists.
        plt.figure(figsize=(8, 5))  # Create a new figure with readable size.
        plt.plot(sizes, orig_times, color="red", marker="o", label="Original RC4")  # Plot Original RC4 line.
        plt.plot(sizes, enh_times, color="blue", marker="o", label="Enhanced RC4")  # Plot Enhanced RC4 line.
        plt.title("Execution Time Comparison")  # Add chart title.
        plt.xlabel("Input Size (bytes)")  # Label x-axis.
        plt.ylabel("Time (milliseconds)")  # Label y-axis.
        plt.legend()  # Show chart legend.
        plt.tight_layout()  # Adjust spacing to prevent clipping.
        output_path = "output_charts/1_execution_time.png"  # Define output file path.
        plt.savefig(output_path)  # Save chart image to file.
        plt.close()  # Close figure to free memory.
        print(f"[Chart] Saved: {output_path}")  # Confirm saved chart.
        return output_path  # Return output file path.
    except Exception as error:
        print(f"Friendly Error: Could not create execution time chart. Details: {error}")  # Print safe error.
        return ""  # Return empty path on failure.


def plot_avalanche(orig_val, enh_val):
    """
    Creates a bar chart for avalanche effect with a 50% ideal reference line.

    Parameters:
    orig_val (float): Original RC4 avalanche percentage.
    enh_val (float): Enhanced RC4 avalanche percentage.

    Returns:
    str: File path of the saved chart image.
    """
    try:
        print("[Chart] Creating avalanche effect chart...")  # Announce chart creation.
        os.makedirs("output_charts", exist_ok=True)  # Ensure output folder exists.
        plt.figure(figsize=(7, 5))  # Create a new figure with readable size.
        labels = ["Original RC4", "Enhanced RC4"]  # Define bar labels.
        values = [orig_val, enh_val]  # Define bar values.
        plt.bar(labels, values, color=["red", "blue"])  # Draw the bar chart.
        plt.axhline(y=50.0, color="black", linestyle="--", label="Ideal (50%)")  # Draw ideal reference line.
        plt.title("Avalanche Effect Comparison")  # Add chart title.
        plt.xlabel("Algorithm")  # Label x-axis.
        plt.ylabel("Avalanche Effect (%)")  # Label y-axis.
        plt.legend()  # Show chart legend.
        plt.tight_layout()  # Adjust spacing to prevent clipping.
        output_path = "output_charts/2_avalanche_effect.png"  # Define output file path.
        plt.savefig(output_path)  # Save chart image to file.
        plt.close()  # Close figure to free memory.
        print(f"[Chart] Saved: {output_path}")  # Confirm saved chart.
        return output_path  # Return output file path.
    except Exception as error:
        print(f"Friendly Error: Could not create avalanche chart. Details: {error}")  # Print safe error.
        return ""  # Return empty path on failure.


def plot_entropy(orig_val, enh_val):
    """
    Creates a bar chart for entropy values with an 8.0-bit ideal reference line.

    Parameters:
    orig_val (float): Original RC4 entropy value.
    enh_val (float): Enhanced RC4 entropy value.

    Returns:
    str: File path of the saved chart image.
    """
    try:
        print("[Chart] Creating entropy chart...")  # Announce chart creation.
        os.makedirs("output_charts", exist_ok=True)  # Ensure output folder exists.
        plt.figure(figsize=(7, 5))  # Create a new figure with readable size.
        labels = ["Original RC4", "Enhanced RC4"]  # Define bar labels.
        values = [orig_val, enh_val]  # Define bar values.
        plt.bar(labels, values, color=["red", "blue"])  # Draw the bar chart.
        plt.axhline(y=8.0, color="black", linestyle="--", label="Ideal (8.0 bits)")  # Draw ideal reference line.
        plt.title("Shannon Entropy Comparison")  # Add chart title.
        plt.xlabel("Algorithm")  # Label x-axis.
        plt.ylabel("Shannon Entropy (bits)")  # Label y-axis.
        plt.legend()  # Show chart legend.
        plt.tight_layout()  # Adjust spacing to prevent clipping.
        output_path = "output_charts/3_entropy.png"  # Define output file path.
        plt.savefig(output_path)  # Save chart image to file.
        plt.close()  # Close figure to free memory.
        print(f"[Chart] Saved: {output_path}")  # Confirm saved chart.
        return output_path  # Return output file path.
    except Exception as error:
        print(f"Friendly Error: Could not create entropy chart. Details: {error}")  # Print safe error.
        return ""  # Return empty path on failure.


def plot_frequency_distribution(orig_freq, enh_freq):
    """
    Creates side-by-side frequency distribution charts for Original and Enhanced RC4.

    Parameters:
    orig_freq (list): Byte frequency list for Original RC4.
    enh_freq (list): Byte frequency list for Enhanced RC4.

    Returns:
    str: File path of the saved chart image.
    """
    try:
        print("[Chart] Creating frequency distribution chart...")  # Announce chart creation.
        os.makedirs("output_charts", exist_ok=True)  # Ensure output folder exists.
        x_values = list(range(256))  # Create x-axis byte values from 0 to 255.
        figure, axes = plt.subplots(1, 2, figsize=(12, 4))  # Create two side-by-side subplots.
        axes[0].bar(x_values, orig_freq, color="red")  # Draw Original RC4 distribution.
        axes[0].set_title("Original RC4 Frequency")  # Set left subplot title.
        axes[0].set_xlabel("Byte Value (0-255)")  # Set left x-axis label.
        axes[0].set_ylabel("Frequency Count")  # Set left y-axis label.
        axes[1].bar(x_values, enh_freq, color="blue")  # Draw Enhanced RC4 distribution.
        axes[1].set_title("Enhanced RC4 Frequency")  # Set right subplot title.
        axes[1].set_xlabel("Byte Value (0-255)")  # Set right x-axis label.
        axes[1].set_ylabel("Frequency Count")  # Set right y-axis label.
        figure.suptitle("Keystream Frequency Distribution Comparison")  # Set overall figure title.
        plt.tight_layout()  # Adjust spacing to prevent clipping.
        output_path = "output_charts/4_frequency_distribution.png"  # Define output file path.
        plt.savefig(output_path)  # Save chart image to file.
        plt.close()  # Close figure to free memory.
        print(f"[Chart] Saved: {output_path}")  # Confirm saved chart.
        return output_path  # Return output file path.
    except Exception as error:
        print(f"Friendly Error: Could not create frequency chart. Details: {error}")  # Print safe error.
        return ""  # Return empty path on failure.


def plot_correlation(orig_val, enh_val):
    """
    Creates a bar chart for correlation values with a 0 ideal reference line.

    Parameters:
    orig_val (float): Original RC4 correlation coefficient.
    enh_val (float): Enhanced RC4 correlation coefficient.

    Returns:
    str: File path of the saved chart image.
    """
    try:
        print("[Chart] Creating correlation chart...")  # Announce chart creation.
        os.makedirs("output_charts", exist_ok=True)  # Ensure output folder exists.
        labels = ["Original RC4", "Enhanced RC4"]  # Define bar labels.
        values = [orig_val, enh_val]  # Define bar values.
        plt.figure(figsize=(7, 5))  # Create a new figure with readable size.
        plt.bar(labels, values, color=["red", "blue"])  # Draw the bar chart.
        plt.axhline(y=0.0, color="black", linestyle="--", label="Ideal (0)")  # Draw ideal reference line.
        plt.title("Consecutive Byte Correlation Comparison")  # Add chart title.
        plt.xlabel("Algorithm")  # Label x-axis.
        plt.ylabel("Correlation Coefficient")  # Label y-axis.
        plt.legend()  # Show chart legend.
        plt.tight_layout()  # Adjust spacing to prevent clipping.
        output_path = "output_charts/5_correlation.png"  # Define output file path.
        plt.savefig(output_path)  # Save chart image to file.
        plt.close()  # Close figure to free memory.
        print(f"[Chart] Saved: {output_path}")  # Confirm saved chart.
        return output_path  # Return output file path.
    except Exception as error:
        print(f"Friendly Error: Could not create correlation chart. Details: {error}")  # Print safe error.
        return ""  # Return empty path on failure.
