# Imports
import logging

def extract_addresses(addresses):
        """Extract address numeral from textual representation.
        Extract address numeral from textual representation by 
        removing description prefix. e.g. 'Input Reg 2' becomes 2.

        parameters:
        ----------
        addresses: list or pandas.core.series.Series
            List of textual addresses.

        returns:
        -------
        A list of integers extracted from supplied addresses. 
        """
        
        # Since lists are iterated over in Python in an oerderly fashion, 
        #   put 'Input Reg ' before 'Input ' such that the 'Reg 'an address 
        #   with an 'Input Reg ' prefix doesn't get left behind
        address_prefixes= ["Input Reg ", "Holding Reg ", "Input ", "Coil "]

        
        for idx,address in enumerate(addresses):
            # Replace prefixes with empty string
            for prefix in address_prefixes:
                addresses[idx]=addresses[idx].replace(prefix, "")
            # Extract numeral
            try:
                addresses[idx]= int(addresses[idx])
            except:
                logging.warning("Invalid modbus address suppied at index {}".format(idx))

        # Return
        return addresses

def evaluate_reader(tag):
    """Evaluate tag properties
    Assign the read type according to the tag info.
    e.g. if Type=="Input" and Data Type=="Bool", use read_type="read_discrete_inputs"
    parameters:
    ----------
    tag: pandas.core.frame.DataFrame
    returns:
    dict
    """
    # Initials
    read_type= None
    UNIT= 0x1
    length= 1

    if tag["Type"]=="Input" and tag["Data Type"]=="Bool":
        read_type="read_discrete_inputs"
    
    if tag["Type"]=="Output" and tag["Data Type"]=="Bool":
        read_type="read_coils"

    if tag["Type"]=="Input" and tag["Data Type"]=="Real":
        read_type="read_input_registers"
    
    if tag["Type"]=="Output" and tag["Data Type"]=="Real":
        read_type="read_holding_registers"

    # Check if no type is matched, raise  ValueError
    if read_type == None: 
        raise ValueError("Tag type error")

    # Return dict of matched type
    return ({
        "read_type": read_type,
        "UNIT": UNIT,
        "length": length
    })

def evaluate_writer(tag):
    """Evaluate tag properties
    Assign the read type according to the tag info.
    e.g. if Type=="Input" and Data Type=="Bool", use read_type="read_discrete_inputs"
    parameters:
    ----------
    tag: pandas.core.frame.DataFrame
    returns:
    dict
    """
    # Initials
    write_type= None
    UNIT= 0x1
    
    if tag["Type"]=="Output" and tag["Data Type"]=="Bool":
        write_type="write_coil"
    
    if tag["Type"]=="Output" and tag["Data Type"]=="Real":
        write_type="write_register"

    # Check if no type is matched, raise  ValueError
    if write_type == None: 
        raise ValueError("Tag type error")

    # Return dict of matched type
    return ({
        "write_type": write_type,
        "UNIT": UNIT
    })
