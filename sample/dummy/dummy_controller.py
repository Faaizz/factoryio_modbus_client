#============================================================
# DUMMY CONTROLLER
# AUTHOR: Faizudeen Kajogbola and Ridwan Shobande
#============================================================

#============================================================
# Constants
MODBUS_HOST= "192.168.1.111"
MODBUS_PORT= 502
TAGS_PATH= "./sample/stacker/tags.csv"
CYCLE_PERIOD= 100 #milliseconds

#============================================================
# Imports
import sys, time, threading
from importlib import util

# User-defined Imports
module_name="modbusclient"
file_path= "./src/modbusclient.py"
spec = util.spec_from_file_location(module_name, file_path)
modbusclient = util.module_from_spec(spec)
sys.modules[module_name] = modbusclient
spec.loader.exec_module(modbusclient)
from modbusclient import FactoryIOModbusClient

#============================================================
# FAULT INJECTION THREAD
class FaultInjector(threading.Thread):
    def __init__(self, fmc):
        threading.Thread.__init__(self)
        self.fmc= fmc

    def run(self):
        # FAULT INJECTION
        # ACTUATORS
        time.sleep(5)
        self.fmc.write_fault("A1", 700)
        # SENSORS
        time.sleep(7)
        self.fmc.read_fault("S1", True)


#============================================================
# Create client instance
with FactoryIOModbusClient(
    MODBUS_HOST, MODBUS_PORT, filepath=TAGS_PATH
    ) as client:
    # Connect client
    isConnected= client.connect()
    assert isConnected

    # Initialize FaultInjection thread
    fi_background= FaultInjector(client)
    # start thread in background
    fi_background.start()

    # Initialize Places
    # Places
    P0= True
    P1= True

    # Controller execution cycle
    while True:

        # Read inputs
        S1= client.read_tag("S1")

        # Controller Logic
        
        # Transitions
        #T0
        if P0 and S1 and not P1:
            P0=False
            P1=True
        
        #T1
        if P1 and not S1 and not P0:
            P1=False
            P0=True

        # Outputs
        if P0:
            client.write_tag("A1", False)
        if P1:
            client.write_tag("A1", True)
       
        time.sleep(CYCLE_PERIOD/1000)
