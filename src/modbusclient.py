# Imports
import os, importlib, sys
from pymodbus.client.sync import ModbusTcpClient
import pandas as pd

# Self-defined imports
# Long-styled import method is used to preserve import structure 
#   regardless of execution/import method
# FMC_functions
work_dir= os.path.dirname(os.path.realpath(__file__))
module_name= "FMC_functions"
file_path= work_dir + "/FMC_functions.py"
spec = importlib.util.spec_from_file_location(module_name, file_path)
FMC_functions = importlib.util.module_from_spec(spec)
sys.modules[module_name] = FMC_functions
spec.loader.exec_module(FMC_functions)


class FactoryIOModbusClient(ModbusTcpClient):

    def __init__(self, host="127.0.0.1", port=502, *, filepath):
        """Constructor
        parameters:
        ----------
        host: str
            Host address of the Modbus TCP server.
        port: int
            Host TCP port.
        filepath: str
            Path to FactoryIO tags file.
        """
        # Initialize fault tags
        self.fault_tags= {"read": {}, "write": {}}
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
        bool or int
        """ 
        # Tag
        try:
            tag= self.tags[self.tags["Name"]==tag].iloc[0]
        except:
            raise ValueError(
                "No tag with specified tag name: {}".format(tag))
        # Evaluate reader
        reader= FMC_functions.evaluate_reader(tag)
        
        # Perform read 
        read_step= eval("self." + reader["read_type"]) \
                (tag["Address"], reader["length"], unit=reader["UNIT"])
        # Check if fault is injected in tag
        if tag["Name"] in self.fault_tags["read"]:
            # Fault present
            return self.fault_tags["read"][tag["Name"]]
        else:
            # No fault
            return eval("read_step." + reader["unit_reader"])

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
                raise ValueError(
                        "The supplied value doesn't not match the data type.\n" \
                        + "'bool' required but '{}' supplied.".format(type(value))
                    )
        if writer["write_type"] == "write_register":
            # For register output
            if not type(value) == int:
                raise ValueError(
                        "The supplied value doesn't not match the data type.\n" \
                        + "'int' required but '{}' supplied.".format(type(value))
                    )
        # Check if fault has been injected in specified tag
        if tag["Name"] in self.fault_tags["write"]:
            # If so, write the faulty value
            value= self.fault_tags["write"][tag["Name"]]

        # Perform write 
        return eval("self." + writer["write_type"]) \
                (tag["Address"], value, unit=writer["UNIT"])


    def read_fault(self, tag, value):
        """Inject read (sensor) fault to specified tag.
        parameters:
        ----------
        tag: str
            Tag to inject read fault.
        value: bool or int
            Value to inject
        returns:
        True on success and False otherwise
        """
        # Tag
        try:
            tag= self.tags[self.tags["Name"]==tag].iloc[0]
        except:
            raise ValueError("No tag with specified tag name: {}".format(tag))
        # Evaluate fault
        isValid= False
        reader= FMC_functions.evaluate_reader(tag)
        # Expected boolean
        if reader["read_type"] == "read_discrete_inputs" \
            or reader["read_type"] == "read_coils":
            try:
                assert type(value) == bool
                isValid= True
            except:
                raise ValueError(
                    "The supplied value doesn't not match the data type.\n" \
                    + "'bool' required but '{}' supplied.".format(type(value))
                )
        # Expected integer
        if reader["read_type"] == "read_input_registers" \
            or reader["read_type"] == "read_holding_registers":
            try:
                assert type(value) == int
                isValid= True
            except:
                raise ValueError(
                    "The supplied value doesn't not match the data type.\n" \
                    + "'int' required but '{}' supplied.".format(type(value))
                )

        # Validation successful
        if isValid:
            self.fault_tags["read"][tag["Name"]]= value
            return True
        else:
            return False


    def write_fault(self, tag, value):
        """Inject write (actuator) fault to specified tag.
        parameters:
        ----------
        tag: str
            Tag to inject write fault.
        value: bool or int
            Value to inject
        returns:
        True on success and False otherwise
        """
        # Tag
        try:
            tag= self.tags[self.tags["Name"]==tag].iloc[0]
        except:
            raise ValueError("No tag with specified tag name: {}".format(tag))
        # Evaluate fault
        isValid= False
        writer= FMC_functions.evaluate_writer(tag)
        # Expected boolean
        if writer["write_type"] == "write_coil":
            try:
                assert type(value) == bool
                isValid= True
            except:
                raise ValueError(
                    "The supplied value doesn't not match the data type.\n" \
                    + "'bool' required but '{}' supplied.".format(type(value))
                )
        # Expected integer
        if writer["write_type"] == "write_register":
            try:
                assert type(value) == int
                isValid= True
            except:
                raise ValueError(
                    "The supplied value doesn't not match the data type.\n" \
                    + "'int' required but '{}' supplied.".format(type(value))
                )

        # Validation successful
        if isValid:
            self.fault_tags["write"][tag["Name"]]= value
            return True
        else:
            return False
        





    