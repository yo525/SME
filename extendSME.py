#Copyright 2025 yo525
#SPDX-License-Identifier: Apache-2.0

#Import necessary modules
from SME import SME256 as sme256
from SME import SME256dBF as sme256dbf
from SME import SME256BF as sme256bf

from time import sleep
from timeit import default_timer
from cProfile import runctx
from importlib.util import find_spec as check_dependencie
from sys import exit

try:
    from rich import print as pprint
    from rich.panel import Panel
    from rich.live import Live
except:
    pass

class SME256(sme256):
    """
    Adds function to the main class SME256, adds a benchmarking/matrix-integrity-checker tool
    and two functions to add graphical efects.
    """

    def check(self, cycles: int = 1000) -> None:
        """
        Benchmarks the SME256 algorithm for a specified number of cycles.

        Args:
            cycles (int): Number of benchmark iterations (default 1000).
        """
        print('Checking and benchmarking SME256 algorithm, this may take a while...\n')
        fastest, slowest, median = 0, 0, 0

        for i in range(1, cycles + 1):
            self.matrix = [i for i in range(0, 256)]  # Reset matrix for each cycle
            start_time = default_timer()  # Start timer
            self.calculate_table_from_values()  # Calculate values for benchmarking
            end_time = default_timer()  # End timer
            total_time = end_time - start_time  # Calculate duration for this cycle
            print(f'Round: {i} out of: {cycles} completed in: {total_time:.6f}s', end='\r')

            # Update benchmarking metrics
            if i == 1:
                median += total_time
                fastest = [total_time, i]
                slowest = [total_time, i]
            else:
                median = (median + total_time) / 2  # Update median estimate
                if total_time < fastest[0]:  # Update fastest time
                    fastest = [total_time, i]
                elif total_time > slowest[0]:  # Update slowest time
                    slowest = [total_time, i]

        # Print benchmark results
        print('\n\n' + '*' * 47)
        print('*              BENCHMARK RESULTS              *')
        print('*' * 47 + '\n')
        print(f' • End of the benchmarking, {cycles} repetitions --> Average time: {median:.6f}s')
        print(f'   - Fastest: cycle {fastest[1]} --> {fastest[0]:.6f}s')
        print(f'   - Slowest: cycle {slowest[1]} --> {slowest[0]:.6f}s')
        print('\n • cProfile results:\n')
        runctx('self.calculate_table_from_values()', locals=locals(), globals=globals())

        conteo = {}  # Dictionary to count repetitions of items in the matrix
        percentage = 0

        # Print results of the checks
        print('\n\n' + '*' * 47)
        print('*                CHECK RESULTS                *')
        print('*' * 47 + '\n')
        if check_dependencie('rich') != None:
            self.print_matrix()
        else:
            tabla = []
            for i in range(0, 255, 16):
                # Construct the display for each row in the matrix
                tabla.append("|".join([
                    " " + str(i).zfill(3) + " "
                    for i in self.matrix[i + i % 16:i + 16]
                ]))
            print('\n'.join(tabla)+'\n')

        # Count occurrences of items in the matrix and match against their indices
        for i in self.matrix:
            if self.matrix.count(i) > 1 and i not in conteo:
                conteo[str(i)] = str(self.matrix.count(i))  # Count occurrences of repeated values
            
            if i == self.matrix.index(i):  # Check if value is in its original index
                percentage += 1

        # Print equality percentage and repeated items
        print(f' • Equality percentage: {((percentage / 256) * 100):.2f}% with {percentage} item(s) in their original index\n • Repeated items:')
        
        for i in conteo:
            print(f'\t- {i} appears {conteo[i]} times.')
        
        if len(conteo) == 0:  # If no repeated items were found
            print('\tNone')


    def imprimir(self, val: list = [], subtitule: str = None, color: str = 'blue', matriz: list = None) -> None:
        """
        Prints the current state of the matrix in a formatted panel.

        Args:
            val (list): A list of values to highlight in the display (default empty).
            subtitule (str): A subtitle for the panel display (default None).
            color (str): Text color for highlighted values (default 'blue').
            matriz (list): A specific matrix to print (default is the current matrix).
        """
        if check_dependencie('rich') == None:
            print('!' * 64 + '   Reference')
            print('* WARNING: Need to install rich in order to use this function. *    in the')
            print('!' * 64 + ' documentation')
            exit()

        if matriz is None:
            matriz = self.matrix
        
        tabla = []
        for i in range(0, 255, 16):
            # Construct the display for each row in the matrix
            tabla.append("|".join([
                " " + str(i).zfill(3) + " " if i not in val else " [" + color + "]" + str(i).zfill(3) + "[/]" 
                for i in matriz[i + i % 16:i + 16]
            ]))

        return (Panel.fit("[u]" + "\n".join(tabla) + "[/]", title='SME_256 Matrix', subtitle=subtitule))

    def print_matrix(self) -> None:
        """ Prints the current matrix using pprint formatting. """
        if check_dependencie('rich') == None:
            print('!' * 64 + '   Reference')
            print('* WARNING: Need to install rich in order to use this function. *    in the')
            print('!' * 64 + ' documentation')
            exit()
        pprint(self.imprimir())

    def calculate_table_from_values_show(self, interval: int | float = 0.01, eliminar: bool = False, values: bytes = None) -> None:
        """
        Shows the step-by-step calculation of the transformation process with delays.

        Args:
            interval (int | float): Time interval between each step display.
            eliminar (bool): Whether to remove the live display after completion (default False).
            values (bytes): The values to use for transformation (default is self.password).
        """
        if check_dependencie('rich') == None:
            print('!' * 64 + '   Reference')
            print('* WARNING: Need to install rich in order to use this function. *    in the')
            print('!' * 64 + ' documentation')
            exit()
            
        self.matrix = [i for i in range(0, 256)]  # Initialize matrix
        if values is None:
            values = self.password
        
        with Live(self.imprimir(), auto_refresh=False, transient=eliminar) as live:
            step = 1
            for i in values:
                valor = self.matrix[self.matrix[0]] ^ i  # Current transformation value determined by XOR
                for j in range(0, valor):  # Iterate through transformation steps
                    try:
                        if j % 2 == 0:
                            # Update the display for row and column rotation
                            live.update(self.imprimir(self.rotate_row(j % 16, 1), subtitule=f'Step: {step} out of {len(values)}\nShifting row: {str(j).zfill(3)} --> {str(valor)}'))
                            live.refresh()
                            sleep(interval)
                            live.update(self.imprimir(self.rotate_column(j % 16, 1), subtitule=f'Step: {step} out of {len(values)}\nShifting column: {str(j).zfill(3)} --> {str(valor)}'))
                            live.refresh()
                            sleep(interval)
                        else:
                            # Update the display for column and row rotation
                            live.update(self.imprimir(self.rotate_column(j % 16, 1), subtitule=f'Step: {step} out of {len(values)}\nShifting column: {str(j).zfill(3)} --> {str(valor)}'))
                            live.refresh()
                            sleep(interval)
                            live.update(self.imprimir(self.rotate_row(j % 16, 1), subtitule=f'Step: {step} out of {len(values)}\nShifting row: {str(j).zfill(3)} --> {str(valor)}'))
                            live.refresh()
                            sleep(interval)
                    except Exception as e:
                        print("Error9 during show step-by-step calculation. Please check the transformation logic.")
                        raise e
                    
                value_index = self.matrix[0] ^ i  # Get the new index value
                if value_index % 16 == 0:
                    column = 16
                    row = (value_index // 16) + 1
                else:
                    column = (value_index % 16) + 1
                    row = (value_index // 16) + 1
                
                # Determine the relationship for moving columns
                relation = 15 if row == 0 else 15 if int(column / row) == 16 else column / row
                column_moves = 0
                column_previous = 0
                value = self.matrix[((row - 1) * 16) + column - 1]
                live.update(self.imprimir([value], color='red', subtitule=f'Step: {step} out of {len(values)}\nBringing front\nIndex value: {value_index} --> {value}'))
                live.refresh()
                sleep(interval + (interval * 0.2))
                
                while self.matrix[0] != value:  # Continue until the desired value is at the front
                    column_moves += relation
                    self.rotate_column(column - 1, 0 if row == 1 else 1)
                    live.update(self.imprimir([value], color='red', subtitule=f'Step: {step} out of {len(values)}\nBringing front\nIndex value: {value}'))
                    live.refresh()
                    sleep(interval)
                    row -= 0 if row == 1 else 1
                    
                    self.rotate_row(row - 1, int(column_moves) - int(column_previous) if column != 1 and column - int(column_moves) - int(column_previous) >= 1 else 0 if column == 1 else column - 1)
                    live.update(self.imprimir([value], color='red', subtitule=f'Step: {step} out of {len(values)}\nBringing front\nIndex value: {value}'))
                    live.refresh()
                    sleep(interval)
                    
                    column -= int(column_moves) - int(column_previous) if column != 1 and column - int(column_moves) - int(column_previous) >= 1 else 0 if column == 1 else column - 1
                    column_previous = column_moves if int(column_moves) - int(column_previous) >= 1 else column_previous
                
                # Scramble the matrix based on even/odd indexing
                if (self.matrix[0] ^ i) % 2 == 0:
                    index = self.matrix[0] ^ i
                    matrix_support = ["   " for _ in range(0, 256)]  # Reset support matrix
                    row = (index >> 4) & 0x0F  # Determine row from index
                    column = index & 0x0F  # Determine column from index
                    
                    for j in range(0, 46, 3):
                        if self.matrix[(column + j) % 16] % 2 == 0:
                            valores = self.column_to_row_even((column + j) % 16, row)  # Even column handling
                        else:
                            valores = self.column_to_row_uneven((column + j) % 16, row)  # Odd column handling
                        matrix_support.extend(valores)
                        del matrix_support[0:16]  # Prevent overflow of support matrix
                        live.update(self.imprimir(valores, subtitule=f'Step: {step} out of {len(values)}\nConverting column: {column + j} to row', matriz=matrix_support))
                        live.refresh()
                        sleep(interval + (interval * 0.25))
                    
                    self.matrix = matrix_support  # Update the main matrix
                else:
                    index = self.matrix[0] ^ i
                    matrix_support = ["   " for _ in range(0, 256)]  # Reset support matrix
                    row = (index >> 4) & 0x0F  # Determine row from index
                    column = index & 0x0F  # Determine column from index
                    
                    for j in range(0, 16):
                        if j % 2:
                            # Handle odd indices differently
                            if self.matrix[(column + j) % 16] % 2 == 0:
                                valores = self.column_to_row_even((column + j) % 16, row)
                                matrix_support.extend(valores)
                                del matrix_support[0:16]
                            else:
                                valores = self.column_to_row_uneven((column + j) % 16, row)
                                matrix_support.extend(valores)
                                del matrix_support[0:16]
                        else:
                            # Handle even indices
                            if self.matrix[(column - j) % 16] % 2 == 0:
                                valores = self.column_to_row_even((column - j) % 16, row)
                                matrix_support.extend(valores)
                                del matrix_support[0:16]
                            else:
                                valores = self.column_to_row_uneven((column - j) % 16, row)
                                matrix_support.extend(valores)
                                del matrix_support[0:16]

                        live.update(self.imprimir(valores, subtitule=f'Step: {step} out of {len(values)}\nConverting column: {column + j} to row', matriz=matrix_support))
                        live.refresh()
                        sleep(interval + (interval * 0.25))

                    self.matrix = matrix_support  # Update the main matrix
                
                step += 1  # Increment step count
                live.update(self.imprimir(subtitule=f'Step: {len(values)} out of {len(values)}\nSME calculation finish'))
                live.refresh()

            if eliminar:
                live.stop()


class SME256BF(sme256bf,SME256):
    """
    A child class that extends the original SME256BF for basic frame encryption functions.
    Adds the ability to print the encryption process while it is happening..
    """

    def encrypt_show(self, plaintext: bytes | str, interval: int = 0.001) -> bytes:
        """
        Encrypts the provided plaintext and shows the process step-by-step.

        Args:
            plaintext (bytes | str): The plaintext to encrypt.
            interval (int): The time in seconds for the delay between steps (default 0.001).

        Returns:
            bytes: The resulting ciphertext.
        """
        if check_dependencie('rich') == None:
            print('!' * 64 + '   Reference')
            print('* WARNING: Need to install rich in order to use this function. *    in the')
            print('!' * 64 + ' documentation')
            exit()
        
        ciphertext = []
        
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode()  # Ensure plaintext is bytes
        
        self.calculate_table_from_values_show(interval=interval, eliminar=True)  # Prepare for display

        with Live(self.imprimir(), auto_refresh=False) as live:
            for i in plaintext:
                try:
                    # Update display with current value being encrypted
                    live.update(self.imprimir(val=[self.matrix[i]], color='red', subtitule='Encrypting plaintext...'))
                    live.refresh()
                    sleep(interval + (interval * 0.25))  # Pause for visibility
                    ciphertext.append(self.matrix[i])  # Append the encrypted value
                except IndexError as e:
                    print("Error11: Encryption process failed due to invalid index.")
                    raise e

            live.update(self.imprimir(subtitule='Plaintext Encrypted...'))
            live.refresh()

        return bytes(ciphertext)

    def decrypt_show(self, ciphertext: bytes | str, interval: int = 0.001) -> bytes:
        """
        Decrypts the provided ciphertext and shows the process step-by-step.

        Args:
            ciphertext (bytes | str): The ciphertext to decrypt.
            interval (int): The time in seconds for the delay between steps (default 0.001).

        Returns:
            bytes: The resulting plaintext.
        """
        if check_dependencie('rich') == None:
            print('!' * 64 + '   Reference')
            print('* WARNING: Need to install rich in order to use this function. *    in the')
            print('!' * 64 + ' documentation')
            exit()
        
        plaintext = []
        
        if not isinstance(ciphertext, bytes):
            ciphertext = ciphertext.encode()  # Ensure ciphertext is bytes
        
        self.calculate_table_from_values_show(interval=interval, eliminar=True)  # Prepare for display
        
        # Iterate over each element in the ciphertext
        for i in ciphertext:
            try:
                plaintext.append(self.matrix.index(i))  # Decrypt value based on matrix indices
                # Update display for current value being decrypted
                with Live(auto_refresh=False, transient=True) as live:
                    live.update(self.imprimir(val=[self.matrix.index(i)], color='red', subtitule='Decrypting ciphertext...'))
                    live.refresh()
                    sleep(interval + (interval * 0.25))  # Pause for visibility
                    live.update(pprint('', end=''))  # Some formatting and refresh
                
            except ValueError as e:
                print("Error13: Decrypting process failed because index was not found in the matrix.")
                raise e

        with Live(self.imprimir(), auto_refresh=False) as live:
            live.update(self.imprimir(subtitule='Ciphertext decrypted...'))  # End messaging display
            live.refresh()

        return bytes(plaintext)

class SME256dBF(sme256dbf,SME256):
    """
    A child class that extends the SME256dBF that implements an alternative encryption method 
    wich updates the transformation matrix dynamically during encryption and decryption.
    Adds the ability to print the encryption process while it is happening.
    """

    def encrypt_show(self, plaintext: bytes | str, interval: int = 0.001) -> bytes:
        """
        Encrypts plaintext using dynamic matrix updates with step-by-step display.

        Args:
            plaintext (bytes | str): The plaintext to encrypt.
            interval (int): The time in seconds for the delay between steps (default 0.001).

        Returns:
            bytes: The resulting ciphertext.
        """
        if check_dependencie('rich') == None:
            print('!' * 64 + '   Reference')
            print('* WARNING: Need to install rich in order to use this function. *    in the')
            print('!' * 64 + ' documentation')
            exit()
        
        ciphertext = []
        support_matrix = [i for i in self.matrix]  # Save initial matrix state
        
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode()  # Ensure plaintext is bytes

        self.calculate_table_from_values_show(interval=interval, eliminar=True)  # Prepare for display
        
        for i in plaintext:
            try:
                with Live(auto_refresh=False, transient=True) as live:
                    ciphertext.append(self.matrix[i])  # Encrypt value based on matrix
                    live.update(self.imprimir(val=[self.matrix[i]], color='red', subtitule='Encrypting plaintext...'))
                    live.refresh()
                    sleep(interval + (interval * 0.25))  # Pause for visibility
                    live.stop()

                self.calculate_table_from_values_show(values=[self.matrix[i] ^ i], interval=interval, eliminar=True)  # Update
            except IndexError as e:
                print("Error15: Encryption process failed due to invalid index.")
                raise e

        with Live(self.imprimir(), auto_refresh=False) as live:
            live.update(self.imprimir(subtitule='Plaintext encrypted...'))  # End messaging display
            live.refresh()

        self.matrix = support_matrix  # Reset matrix state for consistency
        return bytes(ciphertext)

    def decrypt_show(self, ciphertext: bytes | str, interval: int = 0.001) -> bytes:
        """
        Decrypts ciphertext with dynamic matrix updates with step-by-step display.

        Args:
            ciphertext (bytes | str): The ciphertext to decrypt.
            interval (int): The time in seconds for the delay between steps (default 0.001).

        Returns:
            bytes: The resulting plaintext.
        """
        if check_dependencie('rich') == None:
            print('!' * 64 + '   Reference')
            print('* WARNING: Need to install rich in order to use this function. *    in the')
            print('!' * 64 + ' documentation')
            exit()
        
        plaintext = []
        support_matrix = [i for i in self.matrix]  # Save initial matrix state
        
        if not isinstance(ciphertext, bytes):
            ciphertext = ciphertext.encode()  # Ensure ciphertext is bytes

        self.calculate_table_from_values_show(interval=interval, eliminar=True)  # Prepare for display
        
        for i in ciphertext:
            try:
                with Live(auto_refresh=False, transient=True) as live:
                    plaintext.append(self.matrix.index(i))  # Decrypt value based on matrix indices
                    live.update(self.imprimir(val=[self.matrix.index(i)], color='red', subtitule='Decrypting ciphertext...'))
                    live.refresh()
                    sleep(interval + (interval * 0.25))  # Pause for visibility
                    live.update(pprint('', end=''))  # Some formatting and refresh
                    live.refresh()

                self.calculate_table_from_values_show(interval=interval, values=[i ^ self.matrix.index(i)], eliminar=True)  # Update
            except ValueError as e:
                print("Error17: Decryption process failed because index was not found in the matrix.")
                raise e

        with Live(self.imprimir(), auto_refresh=False) as live:
            live.update(self.imprimir(subtitule='Ciphertext decrypted...'))  # End messaging display
            live.refresh()

        self.matrix = support_matrix  # Reset matrix state for consistency
        return bytes(plaintext)

