from src.modbusclient import FactoryIOModbusClient

client= FactoryIOModbusClient("192.168.1.109", 502, filepath="./data/tags.csv")

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
p_al1_b_write= client.write_tag("P_AL1_B", False)
# check for write errors
assert (not p_al1_b_write.isError())

# WRITE INTEGER ACTUATOR
# Write actuator AL1_Z_SET
al1_z_set_write = client.write_tag("AL1_Y_SET", 7)
# check for write errors
assert (not al1_z_set_write.isError())
