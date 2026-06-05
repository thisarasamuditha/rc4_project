# Enhanced RC4 — Educational Comparison

Summary
-------
This repository is an academic project comparing a classic RC4 implementation with a modified "Enhanced RC4" that reduces some known RC4 weaknesses for teaching and evaluation purposes.

Key files
---------
- `main.py`: Interactive menu to encrypt/decrypt and run evaluations.
- `original_rc4.py`: Baseline RC4 (KSA + PRGA).
- `enhanced_rc4.py`: Modified RC4 with double key mixing and a 256-byte warm-up discard.
- `metrics.py`: Functions that measure execution time, avalanche effect, entropy, frequency distribution, and correlation.
- `charts.py`: Generates PNG charts in `output_charts/`.

What the enhancement does
------------------------
- Double key mixing: the KSA is applied twice (second pass uses the reversed key) to further randomize the S-box.
- Warm-up discard: the first 256 PRGA outputs are discarded to avoid early-byte biases.

Tradeoffs
---------
- Pros: improved statistical properties of the keystream (entropy, avalanche, lower short-range correlation).
- Cons: extra initialization work and slightly slower encryption compared with the original implementation. This is educational only — it is not a production-grade fix for RC4.

How to run
----------
1. First-time setup (creates a `venv/`, installs dependencies, creates `output_charts/`):

```bash
python setup.py
```

2. Activate the virtual environment:

Windows:

```powershell
venv\Scripts\activate
```

3. Run the interactive program:

```bash
python main.py
```

Choose menu options to encrypt/decrypt (original or enhanced) or to run evaluations and save charts to `output_charts/`.

Security notes
--------------
- This project is for learning and testing only. RC4 is deprecated for real applications. The enhancements reduce some biases but do not make RC4 suitable for modern security needs.
- For real systems use vetted ciphers (e.g., ChaCha20, AES-GCM) from established libraries such as `cryptography` or libsodium.

Suggested next steps
--------------------
- Replace RC4 with ChaCha20 or AES-GCM using a standard library.
- Add a KDF (PBKDF2 / Argon2) for deriving keys from passphrases.
- Add unit tests and reproducible measurement scripts (seed RNGs) for consistent evaluation.
- Expand statistical testing (NIST STS or Dieharder) if deep analysis is required.
