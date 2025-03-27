#Copyright 2025 yo525
#SPDX-License-Identifier: Apache-2.0

class SME256:
    """
    The main class for 256 Scrambled-Matrix-Encryption (SME256), which implements
    a scrambling encryption technique using a matrix of values.
    """

    # Initialize a matrix with values from 0 to 255
    matrix = [i for i in range(0, 256)]

    def __init__(self, password: bytes, warnings: bool = True) -> None:
        """
        Initialize the SME256 object with a password.
        
        Args:
            password (bytes): The password for the encryption process.
            warnings (bool): Whether to display warnings for short passwords (default True).
        
        Raises:
            Print a warning if the password is less than 16 bytes.
        """
        # Check password length and print warning if it's too short
        if len(password) < 16 and warnings:
            print('\n' + '!' * 80)
            print('* WARNING: Password too short, recommend the use of a longer password *')
            print('!' * 80 + '\n')

        self.password = password
        self.calculate_table_from_values()  # Initialize matrix transformation using the password

    def rotate_column(self, column_index: int, pos: int) -> list:
        """
        Rotates a specific column in the matrix.

        Args:
            column_index (int): The index of the column to be rotated.
            pos (int): The number of positions to rotate.

        Returns:
            list: The new order of values in the rotated column.
        """
        try:
            out = []
            # Construct the column to be rotated based on the column_index
            column = [self.matrix[i + column_index] for i in range(0, 256, 16)]

            for i in range(0, 256, 16):
                # Rotate the column based on the specified positions
                out.append(self.matrix[i - pos * 16 + column_index])  
                self.matrix[i - pos * 16 + column_index] = column[i // 16]
            
            return out
        except IndexError as e:
            print("Error1: Rotation out of bounds. Please check column_index and pos.")
            raise e

    def rotate_row(self, row_index: int, pos: int) -> list:
        """
        Rotates a specific row in the matrix.

        Args:
            row_index (int): The index of the row to be rotated.
            pos (int): The number of positions to rotate.

        Returns:
            list: The new order of values in the rotated row.
        """
        try:
            out = []
            # Extract the row to be rotated based on the row_index
            row = self.matrix[16 * row_index:(16 * row_index) + 16]

            for i in range(0, 16):
                # Rotate the row based on the specified positions
                out.append(self.matrix[((i - pos + 16) % 16) + 16 * row_index])
                self.matrix[((i - pos + 16) % 16) + 16 * row_index] = row[i % 16]

            return out
        except IndexError as e:
            print("Error2: Rotation out of bounds. Please check row_index and pos.")
            raise e

    def rotate_row_column(self, n: int) -> None:
        """
        Rotates both rows and columns in a specific pattern for a number of iterations.

        Args:
            n (int): Number of iterations for the rotations.
        """
        for i in range(0, n):
            if i % 2 == 0:
                self.rotate_row(i % 16, 1)  # Rotate row if iteration is even
                self.rotate_column(i % 16, 1)  # Rotate column if iteration is even
            else:
                self.rotate_column(i % 16, 1)  # Rotate column if iteration is odd
                self.rotate_row(i % 16, 1)  # Rotate row if iteration is odd

    def bring_front(self, value_index: int) -> None:
        """
        Moves a specified value to the front of the matrix based on its index.

        Args:
            value_index (int): The index of the value to move to the front.
        """
        try:
            # Determine the column and row based on value_index
            if value_index % 16 == 0:
                column = 16
                row = (value_index // 16) + 1
            else:
                column = (value_index % 16) + 1
                row = (value_index // 16) + 1

            relation = 15 if row == 0 else 15 if int(column / row) == 16 else column / row
            column_moves = 0
            column_previous = 0
            # Get the value at the calculated position to bring to the front
            value = self.matrix[((row - 1) * 16) + column - 1]

            while self.matrix[0] != value:  # Loop until the desired value is at the front
                column_moves += relation
                self.rotate_column(column - 1, 0 if row == 1 else 1)  # Rotate column
                row -= 0 if row == 1 else 1  # Move up a row if not already at the top
                self.rotate_row(
                    row - 1,
                    int(column_moves) - int(column_previous) if column != 1 and 
                    column - int(column_moves) - int(column_previous) >= 1 
                    else 0 if column == 1 else column - 1
                )
                column -= int(column_moves) - int(column_previous) if column != 1 and column - int(column_moves) - int(column_previous) >= 1 else 0 if column == 1 else column - 1
                column_previous = column_moves if int(column_moves) - int(column_previous) >= 1 else column_previous
        except IndexError as e:
            print("Error3: In bringing value to front, index is out of bounds.")
            raise e

    # Additional methods below would include similar detailed comments and error handling

    def column_to_row_even(self, column_index: int, row_index: int) -> list:
        """
        Converts column values to row values when the row index is even.

        Args:
            column_index (int): The column index to convert from.
            row_index (int): The row index to convert to.

        Returns:
            list: The rearranged row of values from the specified column index.
        """
        try:
            values = [self.matrix[column_index + i] for i in range(0, 256, 16)]
            values_support = []  # Support for rearranging values
            values_support.extend(values[row_index:])  # Take values from row_index to end
            values_support.extend(values[:row_index])  # Add values from start to row_index
            return values_support
        except IndexError as e:
            print("Error4: Column to row even conversion failed. Please check indices.")
            raise e

    def column_to_row_uneven(self, column_index: int, row_index: int) -> list:
        """
        Converts column values to row values when the row index is odd.

        Args:
            column_index (int): The column index to convert from.
            row_index (int): The row index to convert to.

        Returns:
            list: The rearranged row of values from the specified column index.
        """
        try:
            values = [self.matrix[column_index + i] for i in range(0, 256, 16)]
            first = values[row_index + 1:]  # Values after the row_index
            first.reverse()  # Reverse those values
            second = values[:row_index]  # Values before row_index
            second.reverse()  # Reverse those values

            values_support = [values[row_index]]  # Start with the row_index value
            values_support.extend(second)  # Append reversed values from second half
            values_support.extend(first)  # Append reversed values from first half
            return values_support
        except IndexError as e:
            print("Error5: Uneven column to row conversion failed. Please check indices.")
            raise e

    def column_select_scrambler_uneven(self, index: int) -> None:
        """
        Scrambles the matrix using a specific pattern based on the given index for an uneven column.

        Args:
            index (int): The index used to determine scramble order.
        """
        matrix_support = []
        row = (index >> 4) & 0x0F  # Find the row by shifting right
        column = index & 0x0F  # Get the last 4 bits for the column
        
        for i in range(0, 16):
            try:
                # Alternate based on even/odd index positions to decide scrambling method
                if i % 2:  # Odd indices
                    if self.matrix[(column + i) % 16] % 2 == 0:
                        matrix_support.extend(self.column_to_row_even((column + i) % 16, row))  # Even column
                    else:
                        matrix_support.extend(self.column_to_row_uneven((column + i) % 16, row))  # Odd column
                else:  # Even indices
                    if self.matrix[(column - i) % 16] % 2 == 0:
                        matrix_support.extend(self.column_to_row_even((column - i) % 16, row))  # Even column
                    else:
                        matrix_support.extend(self.column_to_row_uneven((column - i) % 16, row))  # Odd column
            
            except IndexError as e:
                print("Error6: Scrambling with uneven column failed. Please check indices.")
                raise e
        
        self.matrix = matrix_support  # Reassign scrambled matrix

    def column_select_scrambler_even(self, index: int) -> None:
        """
        Scrambles the matrix using a specific pattern based on the given index for an even column.

        Args:
            index (int): The index used to determine scramble order.
        """
        matrix_support = []
        row = (index >> 4) & 0x0F  # Shift right to find the row
        column = index & 0x0F  # Mask to keep last 4 bits
        
        for i in range(0, 46, 3):  # Skip every 3rd position in this scrambling method
            try:
                if self.matrix[(column + i) % 16] % 2 == 0:
                    matrix_support.extend(self.column_to_row_even((column + i) % 16, row))  # Even column
                else:
                    matrix_support.extend(self.column_to_row_uneven((column + i) % 16, row))  # Odd column

            except IndexError as e:
                print("Error7: Scrambling with even column failed. Please check indices.")
                raise e

        self.matrix = matrix_support  # Reassign scrambled matrix

    def calculate_table_from_values(self, values: bytes = None) -> None:
        """
        Calculates transformation of the matrix based on the provided values (default is the password).

        Args:
            values (bytes): The values to use for transformation (default is self.password).
        """
        if values is None:
            values = self.password

        try:
            for i in values:
                self.rotate_row_column(self.matrix[self.matrix[0]] ^ i)  # Rotate based on XOR with current leading value
                self.bring_front(self.matrix[0] ^ i)  # Bring current leading value to the front
                # Depending on whether the value is even or odd, apply the appropriate scrambling method
                if (self.matrix[0] ^ i) % 2 == 0:
                    self.column_select_scrambler_even(self.matrix[0] ^ i)
                else:
                    self.column_select_scrambler_uneven(self.matrix[0] ^ i)
        except (IndexError, TypeError) as e:
            print("Error8 in calculating table from values. Please check input values.")
            raise e

    
class SME256BF(SME256):
    """
    A child class that extends SME256 for basic frame encryption functions.
    256 Scrambled-Matrix-Encryption Byte-Flow (SMEBF256)
    """

    def encrypt(self, plaintext: bytes | str) -> bytes:
        """
        Encrypts the provided plaintext using the SME256 algorithm.

        Args:
            plaintext (bytes | str): The plaintext to encrypt.

        Returns:
            bytes: The resulting ciphertext.
        """
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode()  # Ensure encryption function works with bytes
        
        # Handle potential encoding issues in the list comprehension
        try:
            ciphertext = bytes([self.matrix[i] for i in plaintext])  # Map plaintext indices to matrix values
            return ciphertext
        except IndexError as e:
            print("Error10: Encryption failed due to invalid index in plaintext.")
            raise e

    def decrypt(self, ciphertext: bytes | str) -> bytes:
        """
        Decrypts the provided ciphertext back into plaintext.

        Args:
            ciphertext (bytes | str): The ciphertext to decrypt.

        Returns:
            bytes: The resulting plaintext.
        """
        if not isinstance(ciphertext, bytes):
            ciphertext = ciphertext.encode()  # Ensure ciphertext is bytes
        
        try:
            # Rebuild plaintext from indices based on the matrix
            plaintext = bytes([self.matrix.index(i) for i in ciphertext])
            return bytes(plaintext)
        except ValueError as e:
            print("Error12: Decrypting failed because index was not found in the matrix.")
            raise e


class SME256dBF(SME256):
    """
    A child class of SME256 that implements an alternative encryption method 
    that updates the transformation matrix dynamically during encryption and decryption.
    256 Scrambled-Matrix-Encryption dependent-Byte-Flow (SMEdBF256)
    """

    def encrypt(self, plaintext: bytes | str) -> bytes:
        """
        Encrypts plaintext, updating transformation dynamically.

        Args:
            plaintext (bytes | str): The plaintext to encrypt.

        Returns:
            bytes: The resulting ciphertext.
        """
        ciphertext = []
        support_matrix = [i for i in self.matrix]  # Save initial matrix state
        
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode()  # Ensure plaintext is bytes

        for i in plaintext:
            try:
                ciphertext.append(self.matrix[i])  # Encrypt value based on matrix
                self.calculate_table_from_values([self.matrix[i] ^ i])  # Dynamically update matrix based on XOR
            except IndexError as e:
                print("Error14: Encryption process failed due to invalid index.")
                raise e

        self.matrix = support_matrix  # Reset matrix state for consistency
        return bytes(ciphertext)

    def decrypt(self, ciphertext: bytes | str) -> bytes:
        """
        Decrypts ciphertext with dynamic matrix updates.

        Args:
            ciphertext (bytes | str): The ciphertext to decrypt.

        Returns:
            bytes: The resulting plaintext.
        """
        plaintext = []
        support_matrix = [i for i in self.matrix]  # Save initial matrix state
        
        if not isinstance(ciphertext, bytes):
            ciphertext = ciphertext.encode()  # Ensure ciphertext is bytes

        for i in ciphertext:
            try:
                plaintext.append(self.matrix.index(i))  # Decrypt value based on matrix indices
                self.calculate_table_from_values([i ^ self.matrix.index(i)])  # Update the matrix
            except ValueError as e:
                print("Error16: Decryption process failed because index was not found in the matrix.")
                raise e

        self.matrix = support_matrix  # Reset matrix state for consistency
        return bytes(plaintext)
