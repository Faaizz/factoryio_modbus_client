# Imports
import unittest, os
from unittest.mock import MagicMock
import pandas as pd

# Self-defined imports
from src.modbusclient import FactoryIOModbusClient

class FactoryIOModbusClientTest(unittest.TestCase):
    # Setup mock FactoryIO tags
    mock_tags_dict= {
        "Name": ["S_AL1_B", "AL2_ST_GRAB", "Machining Center 3 (Reset)",
            "AL2_ST_Z_POS", "AL1_Z_SET"],
        "Type": ["Input", "Output", "Output", "Input", "Output"],
        "Data Type": ["Bool", "Bool", "Bool", "Real", "Real"],
        "Address": ["Input 0", "Coil 54", "Coil 187", "Input Reg 11", 
            "Holding Reg 2"]
    }
    MOCK_TAGS_PATH= "./test/integration/mock_tags.csv"
    
    # SETUP
    # ===================================================================================
    @classmethod
    def setUpClass(cls):
        # Create mock tags dataframe
        mock_tags_df= pd.DataFrame.from_dict(FactoryIOModbusClientTest.mock_tags_dict)
        # Save to file
        mock_tags_df.to_csv(FactoryIOModbusClientTest.MOCK_TAGS_PATH, index=False)

    @classmethod
    def tearDownClass(cls):
        # Delete
        os.remove(FactoryIOModbusClientTest.MOCK_TAGS_PATH)

    def setUp(self):
        # Initialize FactoryIOModbusClient object
        self.fmc= FactoryIOModbusClient("127.0.0.1", 
            filepath= FactoryIOModbusClientTest.MOCK_TAGS_PATH)

    # ===================================================================================
    # TESTING
    # ===================================================================================
    # __init__
    def test_constructor(self):
        self.assertEqual(
            self.fmc.fault_tags,
            { "read": {}, "write": {} }
        )
    # load_tags
    def test_load_tags(self):
        loaded_tags= self.fmc.load_tags(FactoryIOModbusClientTest.MOCK_TAGS_PATH)
        # Assertions
        self.assertEqual(loaded_tags["Name"][0], 
            FactoryIOModbusClientTest.mock_tags_dict["Name"][0])
        self.assertEqual(loaded_tags["Address"][2], 187)
        self.assertEqual(loaded_tags["Type"][4], 
            FactoryIOModbusClientTest.mock_tags_dict["Type"][4])
        self.assertEqual(loaded_tags["Data Type"][1], 
            FactoryIOModbusClientTest.mock_tags_dict["Data Type"][1])

    # ===================================================================================
    # read_tag
    def test_read_tag1(self):
        # Spy on FactoryIOModbusClient object method "read_discrete_inputs"
        self.fmc.read_discrete_inputs= MagicMock()
        # Read an Input Bool tag
        self.fmc.read_tag("S_AL1_B")
        # Assert that "read_discrete_inputs" was called with:
        exp_args= {
            "Address": 0,
            "length": 1,
            "UNIT": 0x1
        }
        self.fmc.read_discrete_inputs.assert_called_with(
            exp_args["Address"], exp_args["length"], unit= exp_args["UNIT"]
            )

    def test_read_tag2(self):
        # Spy on FactoryIOModbusClient object method "read_coils"
        self.fmc.read_coils= MagicMock()
        # Read an Output Bool tag
        self.fmc.read_tag("AL2_ST_GRAB")
        # Assert that "read_coils" was called with:
        exp_args= {
            "Address": 54,
            "length": 1,
            "UNIT": 0x1
        }
        self.fmc.read_coils.assert_called_with(
            exp_args["Address"], exp_args["length"], unit= exp_args["UNIT"]
            )

    def test_read_tag3(self):
        # Spy on FactoryIOModbusClient object method "read_input_registers"
        self.fmc.read_input_registers= MagicMock()
        # Read an Input Reg Real tag
        self.fmc.read_tag("AL2_ST_Z_POS")
        # Assert that "read_input_registers" was called with:
        exp_args= {
            "Address": 11,
            "length": 1,
            "UNIT": 0x1
        }
        self.fmc.read_input_registers.assert_called_with(
            exp_args["Address"], exp_args["length"], unit= exp_args["UNIT"]
            )

    def test_read_tag4(self):
        # Spy on FactoryIOModbusClient object method "read_holding_registers"
        self.fmc.read_holding_registers= MagicMock()
        # Read an Holding Reg Real tag
        self.fmc.read_tag("AL1_Z_SET")
        # Assert that "read_holding_registers" was called with:
        exp_args= {
            "Address": 2,
            "length": 1,
            "UNIT": 0x1
        }
        self.fmc.read_holding_registers.assert_called_with(
            exp_args["Address"], exp_args["length"], unit= exp_args["UNIT"]
            )

    @unittest.expectedFailure
    def test_read_tag_fail1(self):
        # Invalid tag name (Tag not present in supplied tags)
        self.fmc.read_tag("TAG_NOT_PRESENT")


    # ===================================================================================
    # write_tag
    def test_write_tag1(self):
        # Spy on FactoryIOModbusClient object method "write_register"
        self.fmc.write_register= MagicMock()
        # Expected arguments
        exp_args= {
            "Address": 2,
            "value": 5,
            "UNIT": 0x1
        }
        # Write to a Holding Reg Real tag
        self.fmc.write_tag("AL1_Z_SET", exp_args["value"])
        # Assert that "write_register" was called with expected arguments
        self.fmc.write_register.assert_called_with(
            exp_args["Address"], exp_args["value"], unit= exp_args["UNIT"]
            )

    def test_write_tag2(self):
        # Spy on FactoryIOModbusClient object method "write_coil"
        self.fmc.write_coil= MagicMock()
        # Expected arguments
        exp_args= {
            "Address": 54,
            "value": True,
            "UNIT": 0x1
        }
        # Write to an Output Bool tag
        self.fmc.write_tag("AL2_ST_GRAB", exp_args["value"])
        # Assert that "write_coil" was called with expected arguments
        self.fmc.write_coil.assert_called_with(
            exp_args["Address"], exp_args["value"], unit= exp_args["UNIT"]
            )

    @unittest.expectedFailure
    def test_write_tag_fail1(self):
        # Write an integer to an Output Bool tag
        self.fmc.write_tag("AL2_ST_GRAB", 5)

    @unittest.expectedFailure
    def test_write_tag_fail2(self):
        # Write to an Input Bool tag
        self.fmc.write_tag("S_AL1_B", True)

    @unittest.expectedFailure
    def test_write_tag_fail3(self):
        # Write a boolean to an Output Reg Real tag
        self.fmc.write_tag("AL1_Z_SET", False)

    @unittest.expectedFailure
    def test_write_tag_fail4(self):
        # Write a float to an Output Reg Real tag
        self.fmc.write_tag("AL1_Z_SET", 5.2)


    # ===================================================================================
    # read_fault
    def test_read_fault1(self):
        # Spy on FactoryIOModbusClient object method "read_discrete_inputs"
        self.fmc.read_discrete_inputs= MagicMock()
        tag_name= "S_AL1_B"
        forced_value= False
        # assertions
        self.assertTrue(self.fmc.read_fault(tag_name, forced_value))
        self.assertTrue(tag_name in self.fmc.fault_tags["read"])
        self.assertTrue(self.fmc.fault_tags["read"][tag_name] == forced_value)
        self.assertTrue(self.fmc.read_tag(tag_name) == forced_value)
    
    def test_read_fault2(self):
        # Spy on FactoryIOModbusClient object method "read_input_registers"
        self.fmc.read_input_registers= MagicMock()
        tag_name= "AL2_ST_Z_POS"
        forced_value= 500
        # assertions
        self.assertTrue(self.fmc.read_fault(tag_name, forced_value))
        self.assertTrue(tag_name in self.fmc.fault_tags["read"])
        self.assertTrue(self.fmc.fault_tags["read"][tag_name] == forced_value)
        self.assertTrue(self.fmc.read_tag(tag_name) == forced_value)

    def test_read_fault3(self):
        # Spy on FactoryIOModbusClient object method "read_coils"
        self.fmc.read_coils= MagicMock()
        tag_name= "AL2_ST_GRAB"
        forced_value= False
        # assertions
        self.assertTrue(self.fmc.read_fault(tag_name, forced_value))
        self.assertTrue(tag_name in self.fmc.fault_tags["read"])
        self.assertTrue(self.fmc.fault_tags["read"][tag_name] == forced_value)
        self.assertTrue(self.fmc.read_tag(tag_name) == forced_value)

    def test_read_fault4(self):
        # Spy on FactoryIOModbusClient object method "read_holding_registers"
        self.fmc.read_holding_registers= MagicMock()
        tag_name= "AL1_Z_SET"
        forced_value= 400
        # assertions
        self.assertTrue(self.fmc.read_fault(tag_name, forced_value))
        self.assertTrue(tag_name in self.fmc.fault_tags["read"])
        self.assertTrue(self.fmc.fault_tags["read"][tag_name] == forced_value)
        self.assertTrue(self.fmc.read_tag(tag_name) == forced_value)

    @unittest.expectedFailure
    def test_read_fault_fail1(self):
        tag_name= "AL2_ST_Z_POS"
        forced_value= False
        # assertions
        self.fmc.read_fault(tag_name, forced_value)

    @unittest.expectedFailure
    def test_read_fault_fail2(self):
        tag_name= "S_AL1_B"
        forced_value= 500
        # assertions
        self.fmc.read_fault(tag_name, forced_value)

    @unittest.expectedFailure
    def test_read_fault_fail3(self):
        tag_name= "AL2_ST_GRAB"
        forced_value= 500
        # assertions
        self.fmc.read_fault(tag_name, forced_value)

    @unittest.expectedFailure
    def test_read_fault_fail4(self):
        tag_name= "AL1_Z_SET"
        forced_value= False
        # assertions
        self.fmc.read_fault(tag_name, forced_value)


    # ===================================================================================
    # write_fault
    def test_write_fault1(self):
        # Spy on FactoryIOModbusClient object method "write_coil"
        self.fmc.write_coil= MagicMock()
        tag_name= "AL2_ST_GRAB"
        # Expected arguments
        exp_args= {
            "Address": 54,
            "value": True,
            "UNIT": 0x1
        }
        forced_value= False
        # assertions
        self.assertTrue(self.fmc.write_fault(tag_name, forced_value))
        self.assertTrue(tag_name in self.fmc.fault_tags["write"])
        self.assertTrue(self.fmc.fault_tags["write"][tag_name] == forced_value)
        self.fmc.write_tag(tag_name, exp_args["value"])
        self.fmc.write_coil.assert_called_with(
            exp_args["Address"],
            forced_value, unit=exp_args["UNIT"]
        )

    def test_write_fault2(self):
        # Spy on FactoryIOModbusClient object method "write_register"
        self.fmc.write_register= MagicMock()
        tag_name= "AL1_Z_SET"
        # Expected arguments
        exp_args= {
            "Address": 2,
            "value": 700,
            "UNIT": 0x1
        }
        forced_value= 400
        # assertions
        self.assertTrue(self.fmc.write_fault(tag_name, forced_value))
        self.assertTrue(tag_name in self.fmc.fault_tags["write"])
        self.assertTrue(self.fmc.fault_tags["write"][tag_name] == forced_value)
        self.fmc.write_tag(tag_name, exp_args["value"])
        self.fmc.write_register.assert_called_with(
            exp_args["Address"],
            forced_value, unit=exp_args["UNIT"]
        )

    @unittest.expectedFailure
    def test_write_fault_fail1(self):
        tag_name= "AL2_ST_GRAB"
        forced_value= 500
        # assertions
        self.fmc.write_fault(tag_name, forced_value)

    @unittest.expectedFailure
    def test_write_fault_fail2(self):
        tag_name= "AL1_Z_SET"
        forced_value= False
        # assertions
        self.fmc.write_fault(tag_name, forced_value)
