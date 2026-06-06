import os
import matplotlib.pyplot as plt


def plot_execution_time(input_sizes, original_times_ms, enhanced_times_ms):
    try:
        print("[Chart] Creating execution time chart...")
        os.makedirs("output_charts", exist_ok=True)
        plt.figure(figsize=(8, 5))
        plt.plot(input_sizes, original_times_ms, color="red", marker="o", label="Original RC4")
        plt.plot(input_sizes, enhanced_times_ms, color="blue", marker="o", label="Enhanced RC4")
        plt.title("Execution Time Comparison")
        plt.xlabel("Input Size (bytes)")
        plt.ylabel("Time (milliseconds)")
        plt.legend()
        plt.tight_layout()
        output_path = "output_charts/1_execution_time.png"
        plt.savefig(output_path)
        plt.close()
        print(f"[Chart] Saved: {output_path}")
        return output_path
    except Exception as error:
        print(f"Friendly Error: Could not create execution time chart. Details: {error}")
        return ""


def plot_avalanche(original_avalanche_pct, enhanced_avalanche_pct):
    try:
        print("[Chart] Creating avalanche effect chart...")
        os.makedirs("output_charts", exist_ok=True)
        plt.figure(figsize=(7, 5))
        labels = ["Original RC4", "Enhanced RC4"]
        values = [original_avalanche_pct, enhanced_avalanche_pct]
        plt.bar(labels, values, color=["red", "blue"])
        plt.axhline(y=50.0, color="black", linestyle="--", label="Ideal (50%)")
        plt.title("Avalanche Effect Comparison")
        plt.xlabel("Algorithm")
        plt.ylabel("Avalanche Effect (%)")
        plt.legend()
        plt.tight_layout()
        output_path = "output_charts/2_avalanche_effect.png"
        plt.savefig(output_path)
        plt.close()
        print(f"[Chart] Saved: {output_path}")
        return output_path
    except Exception as error:
        print(f"Friendly Error: Could not create avalanche chart. Details: {error}")
        return ""


def plot_entropy(original_entropy_bits, enhanced_entropy_bits):
    try:
        print("[Chart] Creating entropy chart...")
        os.makedirs("output_charts", exist_ok=True)
        plt.figure(figsize=(7, 5))
        labels = ["Original RC4", "Enhanced RC4"]
        values = [original_entropy_bits, enhanced_entropy_bits]
        plt.bar(labels, values, color=["red", "blue"])
        plt.axhline(y=8.0, color="black", linestyle="--", label="Ideal (8.0 bits)")
        plt.title("Shannon Entropy Comparison")
        plt.xlabel("Algorithm")
        plt.ylabel("Shannon Entropy (bits)")
        plt.legend()
        plt.tight_layout()
        output_path = "output_charts/3_entropy.png"
        plt.savefig(output_path)
        plt.close()
        print(f"[Chart] Saved: {output_path}")
        return output_path
    except Exception as error:
        print(f"Friendly Error: Could not create entropy chart. Details: {error}")
        return ""


def plot_frequency_distribution(original_frequencies, enhanced_frequencies):
    try:
        print("[Chart] Creating frequency distribution chart...")
        os.makedirs("output_charts", exist_ok=True)
        x_values = list(range(256))
        figure, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].bar(x_values, original_frequencies, color="red")
        axes[0].set_title("Original RC4 Frequency")
        axes[0].set_xlabel("Byte Value (0-255)")
        axes[0].set_ylabel("Frequency Count")
        axes[1].bar(x_values, enhanced_frequencies, color="blue")
        axes[1].set_title("Enhanced RC4 Frequency")
        axes[1].set_xlabel("Byte Value (0-255)")
        axes[1].set_ylabel("Frequency Count")
        figure.suptitle("Keystream Frequency Distribution Comparison")
        plt.tight_layout()
        output_path = "output_charts/4_frequency_distribution.png"
        plt.savefig(output_path)
        plt.close()
        print(f"[Chart] Saved: {output_path}")
        return output_path
    except Exception as error:
        print(f"Friendly Error: Could not create frequency chart. Details: {error}")
        return ""


def plot_correlation(original_corr, enhanced_corr):
    try:
        print("[Chart] Creating correlation chart...")
        os.makedirs("output_charts", exist_ok=True)
        labels = ["Original RC4", "Enhanced RC4"]
        values = [original_corr, enhanced_corr]
        plt.figure(figsize=(7, 5))
        plt.bar(labels, values, color=["red", "blue"])
        plt.axhline(y=0.0, color="black", linestyle="--", label="Ideal (0)")
        plt.title("Consecutive Byte Correlation Comparison")
        plt.xlabel("Algorithm")
        plt.ylabel("Correlation Coefficient")
        plt.legend()
        plt.tight_layout()
        output_path = "output_charts/5_correlation.png"
        plt.savefig(output_path)
        plt.close()
        print(f"[Chart] Saved: {output_path}")
        return output_path
    except Exception as error:
        print(f"Friendly Error: Could not create correlation chart. Details: {error}")
        return ""
