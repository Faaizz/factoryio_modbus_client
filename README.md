# Factory IO Modbus Client
[Pymodbus](https://github.com/riptideio/pymodbus) wrapper for ease of use with [Factory IO](https://factoryio.com/). You can directly read from sensors and write to actuators using their Factory IO tag names.

## Usage
1. Select "Modbus TCP/IP Server" driver in Factory IO and export tags.
2. Setup a Modbus Client using the *FactoryIOModbusClient* class and provide the path to exported tags in the constructor:
```python
from src.modbusclient import FactoryIOModbusClient

client= FactoryIOModbusClient("127.0.0.1", 502, filepath="/path/to/tags.csv")
```
3. Connect to the Factory IO Modbus Server and read/write sensors and actuators using tag names
```python
# CONNECT
isSuccess= client.connect()
# check for connection error
assert (isSuccess)

# READ DISCRETE SENSOR
# Read sensor S_AL1_B
s_al1_b_read= client.read_tag("S_AL1_B")
# check for read errors
assert (not s_al1_b_read.isError())
# Get bit value
S_AL1_B= s_al1_b_read.getBit(0)
print("S_AL1_B: {}".format(S_AL1_B))

# READ INTEGER SENSOR
# Read sensor AL1_X_POS
al1_x_pos_read = client.read_tag("AL1_X_POS")
# check for read errors
assert (not al1_x_pos_read.isError())
# Get register value
AL1_X_POS= al1_x_pos_read.getRegister(0)
print("AL1_X_POS: {}".format(AL1_X_POS))

# WRITE DISCRETE ACTUATOR
# Write actuator P_AL1_B
p_al1_b_write= client.write_tag("P_AL1_B", True)
# check for write errors
assert (not p_al1_b_write.isError())

# WRITE INTEGER ACTUATOR
# Write actuator AL1_Z_SET
al1_z_set_write = client.write_tag("AL1_Z_SET", 5)
# check for write errors
assert (not al1_z_set_write.isError())
```


## Project Organization

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
  

## Testing
On windows, run [test_runner.bat](./test_runner.bat) or [test_runner.sh](./test_runner.sh) on Linux/macOS.