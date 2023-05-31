from serial import Serial
from time import sleep
import re

class Money_Dispenser:
    """A class representing a money dispenser."""
    
    def __init__(self, tens_inventory: int, twenties_inventory: int, fifties_inventory: int) -> None:
        """
        Initialize the Money_Dispenser.

        Args:
            tens_inventory (int): The initial inventory count for tens.
            twenties_inventory (int): The initial inventory count for twenties.
            fifties_inventory (int): The initial inventory count for fifties.
        """
        self.tens_inventory = tens_inventory
        self.twenties_inventory = twenties_inventory
        self.fifties_inventory = fifties_inventory

    def get_denominations(self, amount: int) -> dict:
        """
        Get the money in the requested amount from the dispenser.

        Args:
            amount (int): The amount of money to retrieve.

        Returns:
            dict: A dictionary containing the number of each denomination to give, or None if unable to dispense.

        """
        billsToTransfer = {'tensToGive': 0, 'twentiesToGive': 0, 'fiftiesToGive': 0}
        denominations = [50, 20, 10]

        for denomination in denominations:
            while amount >= denomination and self._inventory_available(denomination):
                billsToTransfer[self._get_key(denomination)] += 1
                amount -= denomination
                self._decrement_inventory(denomination)

        if amount > 0:
            return None
        return billsToTransfer

    def process_dispensing(self, serial_port: str, amounts: dict) -> bool:
        """
        Handle the money dispensing process.

        Args:
            amounts (dict): A dictionary containing the number of each denomination to dispense.

        Returns:
            bool: True if the money was successfully dispensed, False otherwise.
        """
        ser = Serial(serial_port, 9600)
        sleep(2)
        try:
            data_string = '{} {} {}'.format(amounts.get('tensToGive', 0), amounts.get('twentiesToGive', 0),
                                            amounts.get('fiftiesToGive', 0))
            ser.write(data_string.encode() + b'\n')
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    if line == "done":
                        return True
                else:
                    sleep(0.1)  # wait a bit before checking again
        finally:
            ser.close()

    def _inventory_available(self, denomination: int) -> bool:
        """
        Check if the given denomination is available in the inventory.

        Args:
            denomination (int): The denomination to check.

        Returns:
            bool: True if the denomination is available, False otherwise.
        """
        if denomination == 50:
            return self.fifties_inventory > 0
        elif denomination == 20:
            return self.twenties_inventory > 0
        elif denomination == 10:
            return self.tens_inventory > 0
        return False

    def _get_key(self, denomination: int) -> str:
        """
        Get the corresponding key for the given denomination.

        Args:
            denomination (int): The denomination.

        Returns:
            str: The corresponding key for the denomination.
        """
        if denomination == 50:
            return 'fiftiesToGive'
        elif denomination == 20:
            return 'twentiesToGive'
        elif denomination == 10:
            return 'tensToGive'
        return ''

    def _decrement_inventory(self, denomination: int) -> None:
        """
        Decrement the inventory count for the given denomination.

        Args:
            denomination (int): The denomination to decrement.
        """
        if denomination == 50:
            self.fifties_inventory -= 1
        elif denomination == 20:
            self.twenties_inventory -= 1
        elif denomination == 10:
            self.tens_inventory -= 1

def process_RFID(serial_port: str) -> str:
    """
    Reads RFID data from a specified serial port and returns the data as a string.
    
    Args:
        serial_port (str): The name or address of the serial port to communicate with the RFID reader.
        
    Returns:
        str: The RFID data read from the serial port.
    """
    rfid_serial = Serial(serial_port, 9600)
    sleep(1)
    rfid_data = ""
    while rfid_data == "":
        try:
            rfid_data = rfid_serial.readline().decode('utf-8', errors='ignore').strip()
        except UnicodeDecodeError:
            continue        
    match = re.search(r"[A-Z]{6}\d{3,10}", rfid_data)
    if match:
        return match.group()  # Return the matched string
    else:
        return "No match found"


