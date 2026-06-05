"""
Project Setup Script
Run this ONCE before starting the project:
  python setup.py

What it does:
  1. Creates a virtual environment called 'venv'
  2. Installs numpy and matplotlib into the venv
  3. Creates the output_charts/ folder
  4. Prints instructions on how to activate the venv
"""

import os
import subprocess
import sys


try:
    if sys.version_info < (3, 10):  # Check that Python version is 3.10+.
        print("Error: Python 3.10 or above is required.")  # Print version error message.
        sys.exit(1)  # Exit because project requirements are not met.

    print("Step 1/5: Python version check passed.")  # Confirm successful version check.

    print("Step 2/5: Creating virtual environment...")  # Announce venv creation step.
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)  # Create venv folder named venv.
    print("Virtual environment created successfully")  # Confirm venv creation.

    print("Step 3/5: Installing dependencies from requirements.txt...")  # Announce dependency install step.
    if os.name == "nt":  # Detect Windows operating system.
        pip_path = os.path.join("venv", "Scripts", "pip")  # Use Windows pip path.
    else:  # Handle macOS and Linux paths.
        pip_path = os.path.join("venv", "bin", "pip")  # Use Unix-like pip path.
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)  # Install required packages.
    print("Dependencies installed: numpy, matplotlib")  # Confirm dependency installation.

    print("Step 4/5: Creating output_charts folder...")  # Announce chart folder creation step.
    os.makedirs("output_charts", exist_ok=True)  # Create folder if missing, skip if already there.
    print("output_charts/ folder created")  # Confirm folder creation.

    print("Step 5/5: Setup finished. Showing activation instructions...")  # Announce final instructions.
    print("")  # Print setup completion banner.
    print("╔══════════════════════════════════════════════════════╗")  # Print top border line.
    print("║              SETUP COMPLETE!                         ║")  # Print banner title.
    print("╠══════════════════════════════════════════════════════╣")  # Print section divider.
    print("║  Activate your virtual environment:                  ║")  # Print activation intro.
    print("║                                                      ║")  # Print spacing line.
    print("║  Windows:   venv\\Scripts\\activate                    ║")  # Print Windows activate command.
    print("║  Mac/Linux: source venv/bin/activate                 ║")  # Print Unix activate command.
    print("║                                                      ║")  # Print spacing line.
    print("║  Then run the project:                               ║")  # Print run intro.
    print("║      python main.py                                  ║")  # Print run command.
    print("║                                                      ║")  # Print spacing line.
    print("║  To deactivate when done:                            ║")  # Print deactivate intro.
    print("║      deactivate                                      ║")  # Print deactivate command.
    print("╚══════════════════════════════════════════════════════╝")  # Print bottom border line.
except Exception as error:
    print(f"Friendly Error: Setup failed. Details: {error}")  # Print safe failure message.
    sys.exit(1)  # Exit with failure code when setup fails.
