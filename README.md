
# SME256 Encryption Library
![Apache-2.0 License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)     ![Python Version](https://img.shields.io/badge/python-3.10%2B-green.svg)
![none](https://img.shields.io/github/languages/code-size/yo525/SME)

The **SME256 Encryption Library** is a Python package that implements the 256 Scrambled-Matrix-Encryption (SME256) algorithm. It provides encryption and decryption functionalities with dynamic matrix transformations.

## Table of Contents

- [Files](#files)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Encryption/Decryption](#basic-encryptiondecryption)
  - [Dependent Matrix Encryption/Decryption](#dependent-matrix-encryptiondecryption)
  - [Step-by-Step Encryption/Decryption (shows each step)](#step-by-step-encryptiondecryption-shows-each-step)
  - [Performance Benchmarking and matrix integrity checker](#performance-benchmarking-and-matrix-integrity-checker)
-  [Workflow](#workflow)
	- [SME256BF Workflow](#sme256bf-workflow)
	- [SME256dBF Workflow](#sme256dbf-workflow)
-  [Matrix Transformations](#matrix-transformations)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Security Disclosure](#security-disclosure)
- [Roadmap](#roadmap)
- [Contact](#contact)

## Files

- [SME.py](SME.py) --> Main core of the SME256 Encryption Library
- [extendSME.py](extendSME.py) --> Extends/adds functions to the SME main core

## Features

-  **Scrambled-Matrix-Encryption (SME256):** A unique encryption algorithm that uses a scrambled matrix for encryption and decryption.
-  **Rich Console Output:** Utilizes the `rich` library to provide visually appealing and informative console output.
- **Performance Benchmarking:** Includes methods to benchmark the performance of the encryption algorithm.
- **Step-by-Step Visualization:** Provides a step-by-step visualization of the encryption and decryption processes.
- **Multiple Encryption Modes:** 
	- **SME256:** 256 Scrambled Matrix Encryption.
		- **SME256BF:** Byte-Flow Encryption. Basic frame encryption function.
		- **SME256dBF:** Dependent-Byte-Flow Encryption with dynamic matrix updates. Updates the transformation matrix dynamically during encryption and decryption.
- **Error Handling:** Comprehensive error handling to manage invalid inputs and index errors gracefully.
- **Matrix Operations:** Advanced matrix operations for row and column rotations, ensuring data integrity.

## Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yo525/SME.git
   cd SME
   ```

2. **Install Dependencies** [^1]

   ```bash
   # This is only necessary if you want to make use of the extendSME version
   # Use pip or pip3 to install the requirements
   pip install -r requirements.txt
   ```

## Usage

### Basic Encryption/Decryption


```python
from SME import SME256BF
from  hashlib  import  scrypt

# Calculate the password using a secure key derivation function like scrypt from the hashlib python module
p =  scrypt(password=b'your_secure_password', salt=b'random_generate_phrase', dklen=16, n=2**14, r=8, p=1)

# Initialize the SME256BF object with a password
sme = SME256BF(password=p)

# Encrypt a plaintext message
plaintext = "Hello, World!"
ciphertext = sme.encrypt(plaintext)
print(f"Ciphertext: {ciphertext}")

# Decrypt the ciphertext back to plaintext
decrypted_text = sme.decrypt(ciphertext)
print(f"Decrypted Text: {decrypted_text}")
```
![](/assets/basic_encryption-decryption.png)

### Dependent Matrix Encryption/Decryption

```python
from SME import SME256dBF
from  hashlib  import  scrypt

# Calculate the password using a secure key derivation function like scrypt from the hashlib python module
p =  scrypt(password=b'your_secure_password', salt=b'random_generate_phrase', dklen=16, n=2**14, r=8, p=1)

# Initialize the SME256dBF object with a password
sme_dbf = SME256dBF(password=p)

# Encrypt a plaintext message with dynamic matrix transformation
plaintext = "Hello, World!"
ciphertext = sme_dbf.encrypt(plaintext)
print(f"Ciphertext: {ciphertext}")

# Decrypt the ciphertext back to plaintext with dynamic matrix transformation
decrypted_text = sme_dbf.decrypt(ciphertext)
print(f"Decrypted Text: {decrypted_text}")
```
![](/assets/dependent_matrix_encryption-decryption.png)

### Step-by-Step Encryption/Decryption (shows each step) [^2]

```python
# Only available with the extendSME version
from extendSME import SME256BF
from  hashlib  import  scrypt

# Calculate the password using a secure key derivation function like scrypt from the hashlib python module
p =  scrypt(password=b'your_secure_password', salt=b'random_generate_phrase', dklen=16, n=2**14, r=8, p=1)

# Initialize the SME256BF object with a password
sme = SME256BF(password=p)

# Encrypt a plaintext message with step-by-step display
plaintext = "Hello, World!"
ciphertext = sme.encrypt_show(plaintext)
print(f"Ciphertext: {ciphertext}")

# Decrypt the ciphertext back to plaintext with step-by-step display
decrypted_text = sme.decrypt_show(ciphertext)
print(f"Decrypted Text: {decrypted_text}")
```
![](/assets/step-by-step_encryption-decryption.png)

### Performance Benchmarking and matrix integrity checker [^3]

```python
# Only available with the extendSME version
from extendSME import SME256BF
from  hashlib  import  scrypt

# Calculate the password using a secure key derivation function like scrypt from the hashlib python module
p =  scrypt(password=b'your_secure_password', salt=b'random_generate_phrase', dklen=16, n=2**14, r=8, p=1)

# Initialize the SME256BF object with a password
sme = SME256BF(password=p)

# Benchmark the SME256 algorithm and display the calculate matrix
sme.check(cycles=1000)
```
## Workflow

### SME256BF Workflow

The `SME256BF` class extends the `SME256` class and implements basic frame encryption functions. Here is a step-by-step breakdown of its workflow:

1.  **Initialization (`__init__` method):**
    
    -   Initializes the SME256 object with a password.
    -   Checks the password length and prints a warning if it's too short.
    -   Initializes the transformation matrix based on the password.

2.  **Encryption (`encrypt` method):**
    
    -   **Step 1:** Convert plaintext to bytes if it is not already.
    -   **Step 2:** For each byte in the plaintext:
        -   Map the byte to a value in the transformed matrix (uses the plaintext value as index to get the ciphertext value in the matrix).
        -   Append the mapped value to the ciphertext.
    -   **Step 3:** Returns the resulting ciphertext.
 
3.  **Encryption with Display (`encrypt_show` method):** [^2]
    
    - Similar to `encrypt`, but includes a step-by-step display of the encryption process using the `rich` library.
    -   Pauses between steps for better visualization.
 
5.  **Decryption (`decrypt` method):**
    
    -   **Step 1:** Convert ciphertext to bytes if it is not already.
    -   **Step 2:** For each byte in the ciphertext:
        -   Find the index of the byte in the transformed matrix.
        -   Append the index byte to the plaintext.
    -   **Step 3:** Returns the resulting plaintext.


6.  **Decryption with Display (`decrypt_show` method):** [^2]
    
    - Similar to `decrypt`, but includes a step-by-step display of the decryption process using the `rich` library.
    -   Pauses between steps for better visualization.

### SME256dBF Workflow

The `SME256dBF` class also extends the `SME256` class but implements an alternative encryption method that updates the transformation matrix dynamically during encryption and decryption. Here is a step-by-step breakdown of its workflow:

1.  **Initialization (`__init__` method):**
    
    -   Initializes the SME256 object with a password.
    -   Checks the password length and prints a warning if it's too short.
    -   Initializes the transformation matrix based on the password

2.  **Encryption (`encrypt` method):**
    
    -   **Step 1:** Convert plaintext to bytes if it is not already.
    -   **Step 2:** For each byte in the plaintext:
        -   Map the byte to a value in the transformed matrix (uses the plaintext value as index to get the ciphertext value in the matrix).
        -   Append the mapped value to the ciphertext.
        -   Update the matrix based on the XOR of the current matrix value and the plaintext byte.
    -   **Step 3:** Returns the resulting ciphertext.

3.  **Encryption with Display (`encrypt_show` method):** [^2]
    
    - Similar to `encrypt`, but includes a step-by-step display of the encryption process using the `rich` library.
    -   Pauses between steps for better visualization.
    -   Dynamically updates the transformation matrix and displays the changes.


4.  **Decryption (`decrypt` method):**
    
    -   **Step 1:** Convert ciphertext to bytes if it is not already.
    -   **Step 2:** For each byte in the ciphertext:
        -   Find the index of the byte in the transformed matrix.
        -   Append the index byte to the plaintext.
        -   Update the matrix dynamically based on the XOR of the current matrix value and the plaintext byte.
    -   **Step 3:** Returns the resulting plaintext.


5.  **Decryption with Display (`decrypt_show` method):** [^2]

    - Similar to `decrypt`, but includes a step-by-step display of the decryption process using the `rich` library.
    -   Pauses between steps for better visualization.
    -   Dynamically updates the transformation matrix and displays the changes.
 ## Matrix Transformations

The matrix transformations in the SME256 algorithm are crucial for the encryption and decryption processes. The transformations include:

-   **Initialization:**
    
    -   The matrix is initialized with values from 0 to 255.
-   **Password-Based Transformation:**
    
    -   The matrix is scrambled based on the provided password using a series of rotations and scramblings.

### Detailed Transformation Steps

1.  **Rotation of Rows and Columns:**
    
    -   Rows and columns of the matrix are rotated based on the XOR of the current matrix value and the password byte.
    -   This involves shifting elements within rows and columns to create a scrambled matrix.
2.  **Scrambling Based on Index:**
    
    -   The matrix is scrambled using specific patterns based on the index calculated from the XOR operation.
    -   This involves converting columns to rows and applying even/odd rules to further scramble the matrix.
3.  **Bringing Values to the Front:**
    
    -   Specific values are moved to the front of the matrix based on their index.
    -   This ensures that the matrix remains dynamic and scrambled throughout the process.
 
## API Reference

- **SME256 Class:**
  - `__init__(password: bytes, warnings: bool = True)`
  - `check`[^3]`(cycles: int = 1000)`
  - `rotate_column(column_index: int, pos: int) -> list`
  - `rotate_row(row_index: int, pos: int) -> list`
  - `rotate_row_column(n: int) -> None`
  - `bring_front(value_index: int) -> None`
  - `column_to_row_even(column_index: int, row_index: int) -> list`
  - `column_to_row_uneven(column_index: int, row_index: int) -> list`
  - `column_select_scrambler_uneven(index: int) -> None`
  - `column_select_scrambler_even(index: int) -> None`
  - `imprimir`[^2]`(val: list = [], subtitule: str = None, color: str = 'blue', matriz: list = None) -> None`
  - `print_matrix`[^2]`(self) -> None`
  - `calculate_table_from_values(values: bytes = None) -> None`
  - `calculate_table_from_values_show`[^2]`(interval: int | float = 0.01, eliminar: bool = False, values: bytes = None) -> None`

- **SME256BF Class (extends SME256):**
  - `encrypt(plaintext: bytes | str) -> bytes`
  - `encrypt_show`[^2]`(plaintext: bytes | str, interval: int = 0.001) -> bytes`
  - `decrypt(ciphertext: bytes | str) -> bytes`
  - `decrypt_show`[^2]`(ciphertext: bytes | str, interval: int = 0.001) -> bytes`

- **SME256dBF Class (extends SME256):**
  - `encrypt(plaintext: bytes | str) -> bytes`
  - `encrypt_show`[^2]`(plaintext: bytes | str, interval: int = 0.001) -> bytes`
  - `decrypt(ciphertext: bytes | str) -> bytes`
  - `decrypt_show`[^2]`(ciphertext: bytes | str, interval: int = 0.001) -> bytes`


## Contributing

Contributions are welcome! Please follow the guidelines below to contribute to the project:

1. **Fork the Repository**
2. **Create Your Feature Branch (`git checkout -b feature/AmazingFeature`)** 
3. **Commit Your Changes (`git commit -m 'Add some AmazingFeature'`)** 
4. **Push to the Branch (`git push origin feature/AmazingFeature`)** 
5. **Open a Pull Request**

## License

This project is licensed under the **Apache-2.0 License**. For more details, see the [LICENSE](LICENSE) file.

## Security Disclosure

**Important**: The SME256 encryption algorithm is a custom implementation and has not undergone rigorous security analysis. While it incorporates various encryption techniques and dynamic updates, it is recommended to use it with caution and not for critical applications where security is paramount. Always evaluate encryption libraries based on their security audits and peer reviews before deploying them in production environments.

## Roadmap

- [ ] **Performance Enhancements**: Optimize matrix transformations and encryption/decryption processes for faster performance.
- [ ] **Additional Modes**: Introduce new encryption modes with different matrix transformation techniques.
- [ ] **Documentation/Whitepaper:** Improved documentation and created a white paper to explain the encryption/decryption algorithm step by step.
- [ ] **Correction of the SME256dBF:** SME256dBF has a vulnerability that allows an attacker to obtain the password of an encrypted message if both the plaintext and ciphertext are available. This can later be used to compromise other information if it has been encrypted with the same password. This is a critical vulnerability that must be addressed.

## Contact

- **Author:** yo525
- **Email:** [yo525@proton.me](mailto:yo525@proton.me)
-   **GitHub:** [yo525](https://github.com/yo525)

Feel free to reach out for any questions or feedback!

[^1]: *Not required for the check function.*
[^2]: *Only available with the extendSME version. Dependencies installation necessary, dependencies required.*
[^3]: *Only available with the extendSME version. Dependencies installation not necessary, dependencies not required.*

