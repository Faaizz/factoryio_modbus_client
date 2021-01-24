# Imports
import unittest
import src.FMC_functions as FMC_functions

class FMC_functionsTest(unittest.TestCase):
    # ================================================================
    # extract_address
    def test_extract_addresses1(self):
        self.assertEqual(
            FMC_functions.extract_addresses(["Input 0", "Coil 6", "Holding Reg 17", "Input Reg 80"]),
            [0, 6, 17, 80]
        )

    # Expect program to handle invalid address gracefully
    def test_extract_addresses2(self):
        FMC_functions.extract_addresses(["Input p", "Coil a", "Holding Reg17", "Input Reg"]),

    # ===============================================================
    # evaluate_reader
    def test_evaluate_reader1(self):
        # Discrete Input
        self.assertEqual(
            FMC_functions.evaluate_reader({
                "Type": "Input",
                "Data Type": "Bool"
            }),
            {
                "read_type": "read_discrete_inputs",
                "UNIT": 0x1,
                "length": 1
            }
        )
        # Discrete Output
        self.assertEqual(
            FMC_functions.evaluate_reader({
                "Type": "Output",
                "Data Type": "Bool"
            }),
            {
                "read_type": "read_coils",
                "UNIT": 0x1,
                "length": 1
            }
        )
        # Real Input
        self.assertEqual(
            FMC_functions.evaluate_reader({
                "Type": "Input",
                "Data Type": "Real"
            }),
            {
                "read_type": "read_input_registers",
                "UNIT": 0x1,
                "length": 1
            }
        )
        # Real Output
        self.assertEqual(
            FMC_functions.evaluate_reader({
                "Type": "Output",
                "Data Type": "Real"
            }),
            {
                "read_type": "read_holding_registers",
                "UNIT": 0x1,
                "length": 1
            }
        )
    
    @unittest.expectedFailure
    def test_evaluate_reader_fail1(self):
        # Bad Input
        self.assertEqual(
            FMC_functions.evaluate_reader({
                "Type": "",
                "Data Type": "Real"
            }),
            {
                "read_type": "read_holding_registers",
                "UNIT": 0x1,
                "length": 1
            }
        )

    # ===============================================================
    # evaluate_writer
    def test_evaluate_writer1(self):
        # Discrete Output
        self.assertEqual(
            FMC_functions.evaluate_writer({
                "Type": "Output",
                "Data Type": "Bool"
            }),
            {
                "write_type": "write_coil",
                "UNIT": 0x1
            }
        )

        # Real Output
        self.assertEqual(
            FMC_functions.evaluate_writer({
                "Type": "Output",
                "Data Type": "Real"
            }),
            {
                "write_type": "write_register",
                "UNIT": 0x1
            }
        )

    @unittest.expectedFailure
    def test_evaluate_writer_fail1(self):
        # Bad Input
        self.assertEqual(
            FMC_functions.evaluate_reader({
                "Type": "Input",
                "Data Type": "Real"
            }),
            {
                "write_type": "write_register",
                "UNIT": 0x1
            }
        )

