# Imports
from pymodbus.client.sync import ModbusTcpClient
import pandas as pd

# Self-defined imports
from . import FMC_functions

class FactoryIOModbusClient(ModbusTcpClient):

    def __init__(self, host="127.0.0.1", port=502, *, filepath):
        """Constructor
        parameters:
        ----------
        - host: str
            Host address of the Modbus TCP server.
        - port: int
            Host TCP port.
        - filepath: str
            Path to FactoryIO tags file.
        """
        # Load tags
        self.tags= self.load_tags(filepath)
        # Call constructor of superclass
        super().__init__(host, port=port)

    def load_tags(self, filepath):
        """Load FactoryIO tags file that maps signal names to Modbus
        addresses.
        parameters:
        ----------
        filepath: str
            Path to FactoryIO tags file
        returns:
        -------
        Pandas dataframe with addresses reduced to their numeric values
        """
        tags_df= pd.read_csv(filepath)
        clean_addresses= FMC_functions.extract_addresses(tags_df["Address"])
        tags_df["Address"]= clean_addresses

        return tags_df

    def read_tag(self, tag):
        """Read tag
        parameters:
        ----------
        tag: str
            Tag to read
        returns:
        -------
        pymodbus.bit_read_message.ReadDiscreteInputsResponse
        or
        pymodbus.bit_read_message.ReadCoilsResponse
        or
        pymodbus.bit_read_message.ReadHoldingRegistersResponse
        """ 
        # Tag
        try:
            tag= self.tags[self.tags["Name"]==tag].iloc[0]
        except:
            raise ValueError("No tag with specified tag name: {}".format(tag))
        # Evaluate reader
        reader= FMC_functions.evaluate_reader(tag)
        
        # Perform read 
        return eval("self." + reader["read_type"])(tag["Address"], reader["length"], unit=reader["UNIT"])

    def write_tag(self, tag, value):
        """Write tag
        parameters:
        ----------
        tag: str
            Tag to write
        value: bool, int, or float
            Value to write
        returns:
        -------
        pymodbus.bit_write_message.WriteSingleCoilResponse 
        or
        pymodbus.bit_write_message.WriteSingleRegisterResponse
        """
        # Tag
        try:
            tag= self.tags[self.tags["Name"]==tag].iloc[0]
        except:
            raise ValueError("No tag with specified tag name: {}".format(tag))
        # Evaluate writer
        writer= FMC_functions.evaluate_writer(tag)
        # Check if value matches type of Output to write
        if writer["write_type"] == "write_coil":
            # For coil output
            if not type(value) == bool:
                raise ValueError("The supplied value doesn't not match the data type.\n" \
                        + "'bool' required but '{}' supplied.".format(type(value))
                    )
        if writer["write_type"] == "write_register":
            # For register output
            if not type(value) == int:
                raise ValueError("The supplied value doesn't not match the data type.\n" \
                        + "'int' required but '{}' supplied.".format(type(value))
                    )

        # Perform write 
        return eval("self." + writer["write_type"])(tag["Address"], value, unit=writer["UNIT"])




    