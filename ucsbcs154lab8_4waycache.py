# ucsbcs154lab8_4waycache.py
# All Rights Reserved
# Copyright (c) 2022 Jonathan Balkind
# Distribution Prohibited

import pyrtl

pyrtl.core.set_debug_mode()

# Cache parameters:
# 32 bit addresses
# 4 ways
# 16 rows
# 16 bytes (4 words) per block

# Inputs
req_new = pyrtl.Input(bitwidth=1, name='req_new')       # High on cycles when a request is occurring
req_addr = pyrtl.Input(bitwidth=32, name='req_addr')    # Requested address
req_type = pyrtl.Input(bitwidth=1, name='req_type')     # 0 read, 1 write
req_data = pyrtl.Input(bitwidth=32, name='req_data')    # Only for writes

# Outputs
resp_hit = pyrtl.Output(bitwidth=1, name='resp_hit')    # Indicates whether there was a cache hit
resp_data = pyrtl.Output(bitwidth=32, name='resp_data') # If read request, return data at req_addr

# Memories
valid_0 = pyrtl.MemBlock(bitwidth=1, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='valid_0')
valid_1 = pyrtl.MemBlock(bitwidth=1, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='valid_1')
valid_2 = pyrtl.MemBlock(bitwidth=1, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='valid_2')
valid_3 = pyrtl.MemBlock(bitwidth=1, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='valid_3')

tag_0 = pyrtl.MemBlock(bitwidth=24, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='tag_0')
tag_1 = pyrtl.MemBlock(bitwidth=24, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='tag_1')
tag_2 = pyrtl.MemBlock(bitwidth=24, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='tag_2')
tag_3 = pyrtl.MemBlock(bitwidth=24, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='tag_3')

data_0 = pyrtl.MemBlock(bitwidth=128, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='data_0')
data_1 = pyrtl.MemBlock(bitwidth=128, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='data_1')
data_2 = pyrtl.MemBlock(bitwidth=128, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='data_2')
data_3 = pyrtl.MemBlock(bitwidth=128, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='data_3')

# To track which Way entry to replace next.
repl_way = pyrtl.MemBlock(bitwidth=2, addrwidth=4, max_read_ports=2, max_write_ports=1, asynchronous=True, name='repl_way')

# TODO: Declare your own WireVectors, MemBlocks, etc.
tag = pyrtl.WireVector(bitwidth=24, name='tag')
index = pyrtl.WireVector(bitwidth=4, name='index')
offset = pyrtl.WireVector(bitwidth=4, name='offset')

tag <<= req_addr[8:32]
index <<= req_addr[4:8]
offset <<= req_addr[0:4]

write_mask = pyrtl.WireVector(bitwidth=128, name='write_mask')
write_data = pyrtl.WireVector(bitwidth=128, name='write_data')

hit_result = pyrtl.WireVector(bitwidth=1, name='hit_result')
enable_0 = pyrtl.WireVector(bitwidth=1, name='enable_0')
enable_1 = pyrtl.WireVector(bitwidth=1, name='enable_1')
enable_2 = pyrtl.WireVector(bitwidth=1, name='enable_2')
enable_3 = pyrtl.WireVector(bitwidth=1, name='enable_3')

data_0_payload = pyrtl.WireVector(bitwidth=128, name='data_0_payload')
data_1_payload = pyrtl.WireVector(bitwidth=128, name='data_1_payload')
data_2_payload = pyrtl.WireVector(bitwidth=128, name='data_2_payload')
data_3_payload = pyrtl.WireVector(bitwidth=128, name='data_3_payload')

hit_0 = pyrtl.WireVector(bitwidth=1, name='hit_0')
hit_1 = pyrtl.WireVector(bitwidth=1, name='hit_1')
hit_2 = pyrtl.WireVector(bitwidth=1, name='hit_2')
hit_3 = pyrtl.WireVector(bitwidth=1, name='hit_3')

temp = pyrtl.WireVector(bitwidth=128, name='temp')
way = pyrtl.WireVector(bitwidth=2, name='way')
####################################################################################

# TODO: Check four entries in a row in parallel.


with pyrtl.conditional_assignment:
    with req_new == 0b1:
        with (valid_0[index] == 0b1) & (tag_0[index] == tag):
            hit_result |= 0b1
            hit_0 |= 0b1
            temp |= data_0[index]
            # resp_hit |= 0b1
        with (valid_1[index] == 0b1) & (tag_1[index] == tag):
            hit_result |= 0b1
            hit_1 |= 0b1
            temp |= data_1[index]
            # resp_hit |= 0b1
        with (valid_2[index] == 0b1) & (tag_2[index] == tag):
            hit_result |= 0b1
            hit_2 |= 0b1
            temp |= data_2[index]
            # resp_hit |= 0b1
        with (valid_3[index] == 0b1) & (tag_3[index] == tag):
            hit_result |= 0b1
            hit_3 |= 0b1
            temp |= data_3[index]
            # resp_hit |= 0b1
        with pyrtl.otherwise:
            hit_result |= 0b0
            # resp_hit |= 0b0
    with pyrtl.otherwise:
        hit_result |= 0b0
        # resp_hit |= 0b0

resp_hit |= hit_result



# resp_hit <<= hit_result



# with pyrtl.conditional_assignment: 
#     with req_new == 0b00:
#         resp_data |= 0b00
#         resp_hit |= 0b00


#     with req_new == 0b01 & req_type == 0b00: # read request 
#         with (): # hits in cache 
#             # resp_data |= 
#             resp_hit |= 0b01 
#         with pyrtl.otherwise: # read miss 
#             resp_hit |= 0b00
#             resp_data |= 0b00
#             # set data block to 0 for future accesses 
#     with req_new == 0b01 & req_type == 0b01: #write request
#         with (): # hits in cache
#             # replace word w/ req_data
#             resp_hit == 0b01
#             resp_data == 0b00
#         with pyrtl.otherwise: 
#             resp_hit |= 0b00 
#             resp_data |= 0b00
#             # A new entry should be added to the cache forreq_addr
#             # whose datablock should consist of req_data at the 
#             # appropriate word location and the rest of the words 
#             # in the block set to “0”. As with a read miss, the
#             # new block should be made valid.


    



# TODO: Determine if hit or miss.
# hit_result = hit_0 | hit_1 | hit_2 | hit_3



# TODO: If request type is write, write req_data to appropriate block address
# enable_0 = ...
# # new request, write, hit, hit 0 
# enable_1 = ...
# enable_2 = ...
# enable_3 = ...

# with pyrtl.conditional_assignment: 
#     with (req_new == 0b1) & (req_type == 0b1) & (hit_result == 0b1) & (hit_0 == 0b1):
#         enable_0 |= 0b1
#     with (req_new == 0b1) & (req_type == 0b1) & (hit_result == 0b1) & (hit_1 == 0b1):
#         enable_1 |= 0b1
#     with (req_new == 0b1) & (req_type == 0b1) & (hit_result == 0b1) & (hit_2 == 0b1):
#         enable_2 |= 0b1
#     with (req_new == 0b1) & (req_type == 0b1) & (hit_result == 0b1) & (hit_3 == 0b1):
#         enable_3 |= 0b1


data_shift_amount = offset * 8
# offset times 8 

way <<= repl_way[index]


write_mask <<= pyrtl.select(hit_result, ~pyrtl.shift_left_logical(pyrtl.Const(0x0ffffffff, bitwidth=128), data_shift_amount), 0)
write_data <<= pyrtl.shift_left_logical(req_data.zero_extended(bitwidth=128), data_shift_amount)

data_0_payload |= data_0[index]
data_1_payload |= data_1[index]
data_2_payload |= data_2[index]
data_3_payload |= data_3[index]

data_0[index] <<= pyrtl.MemBlock.EnabledWrite((data_0_payload & write_mask) | write_data, enable_0) 
data_1[index] <<= pyrtl.MemBlock.EnabledWrite((data_1_payload & write_mask) | write_data, enable_1)
data_2[index] <<= pyrtl.MemBlock.EnabledWrite((data_2_payload & write_mask) | write_data, enable_2)
data_3[index] <<= pyrtl.MemBlock.EnabledWrite((data_3_payload & write_mask) | write_data, enable_3)



# TODO: Handle replacement. Be careful handling replacement when you
# also have to do a write

# replacement is 0, enable 0 
# if replacement way at index is 0, then enable_0 = 1

# dont hit, but have request, check repway 
# set valid at index 1, tag bits at index, repway = 1

# if its 3, then repl way = 0

# if miss, repl_way where to replace 

# repl_way[index] 

# with pyrtl.conditional_assignment:
#     with hit_result == 0b0 & req_new == 0b1:
#         with repl_way[index] == 0b00:
#             repl_way[index] = 1
#             valid_0 |=...
#             tag_0 |=...
#         with repl_way[index] == 0b01:
#             repl_way[index] = 1
#             valid_1 |=...
#             tag_1 |=...        
#         with repl_way[index] == 0b10:
#             repl_way[index] = 1
#             valid_2 |=...
#             tag_2 |=...             
#         with repl_way[index] == 0b11:
#             repl_way[index] = 1
#             valid_3 |=...
#             tag_3 |=...     
    

# with pyrtl.conditional_assignment:
#     with hit_result == 0b0 & req_new == 0b1:
#         with repl_way[index] == 0b00:
#             repl_way[index] = 1
#             valid_0 |=...
#             tag_0 |=...
#         with repl_way[index] == 0b01:
#             repl_way[index] = 1
#             valid_1 |=...
#             tag_1 |=...        
#         with repl_way[index] == 0b10:
#             repl_way[index] = 1
#             valid_2 |=...
#             tag_2 |=...             
#         with repl_way[index] == 0b11:
#             repl_way[index] = 1
#             valid_3 |=...
#             tag_3 |=...     

# with pyrtl.conditional_assignment:
#     with hit_result == 0b0 & req_new == 0b1:
#         with repl_way[index] == 0b00:
#             repl_way[index] = 1
#             valid_0 |=...
#             tag_0 |=...
#         with repl_way[index] == 0b01:
#             repl_way[index] = 1
#             valid_1 |=...
#             tag_1 |=...        
#         with repl_way[index] == 0b10:
#             repl_way[index] = 1
#             valid_2 |=...
#             tag_2 |=...             
#         with repl_way[index] == 0b11:
#             repl_way[index] = 1
#             valid_3 |=...
#             tag_3 |=...  


# with pyrtl.conditional_assignment: # read miss / write miss 
    
    

with pyrtl.conditional_assignment:
    with req_new == 0b0: 
        enable_0 |= 0b0
        enable_1 |= 0b0
        enable_2 |= 0b0
        enable_3 |= 0b0
    with (req_new == 0b1) & (hit_result == 0b0): #misses 
        with way == 0b00: 
            enable_0 |= 0b1
            repl_way[index] |= pyrtl.MemBlock.EnabledWrite(1,1)
        with way == 0b01: 
            enable_1 |= 0b1
            repl_way[index] |= pyrtl.MemBlock.EnabledWrite(2,1)
        with way == 0b10: 
            enable_2 |= 0b1
            repl_way[index] |= pyrtl.MemBlock.EnabledWrite(3,1)
        with way == 0b11: 
            enable_3 |= 0b1
            repl_way[index] |= pyrtl.MemBlock.EnabledWrite(0,1)
        
        tag_0[index] |= pyrtl.MemBlock.EnabledWrite(tag, enable_0)
        tag_1[index] |= pyrtl.MemBlock.EnabledWrite(tag, enable_1)
        tag_2[index] |= pyrtl.MemBlock.EnabledWrite(tag, enable_2)
        tag_3[index] |= pyrtl.MemBlock.EnabledWrite(tag, enable_3)

        valid_0[index] |= pyrtl.MemBlock.EnabledWrite(1, enable_0)
        valid_1[index] |= pyrtl.MemBlock.EnabledWrite(1, enable_1)
        valid_2[index] |= pyrtl.MemBlock.EnabledWrite(1, enable_2)
        valid_3[index] |= pyrtl.MemBlock.EnabledWrite(1, enable_3)



    with (req_new == 0b1) & (hit_result == 0b1) & (req_type == 0b1): #write hit 
            with hit_0 == 0b1: 
                enable_0 |= 0b1
                repl_way[index] |= pyrtl.MemBlock.EnabledWrite(1,1)
            with hit_1 == 0b1: 
                enable_1 |= 0b1
                repl_way[index] |= pyrtl.MemBlock.EnabledWrite(2,1)
            with hit_2 == 0b1: 
                enable_2 |= 0b1
                repl_way[index] |= pyrtl.MemBlock.EnabledWrite(3,1)
            with hit_3 == 0b1: 
                enable_3 |= 0b1
                repl_way[index] |= pyrtl.MemBlock.EnabledWrite(0,1)
            
            tag_0[index] |= pyrtl.MemBlock.EnabledWrite(tag, enable_0)
            tag_1[index] |= pyrtl.MemBlock.EnabledWrite(tag, enable_1)
            tag_2[index] |= pyrtl.MemBlock.EnabledWrite(tag, enable_2)
            tag_3[index] |= pyrtl.MemBlock.EnabledWrite(tag, enable_3)

            valid_0[index] |= pyrtl.MemBlock.EnabledWrite(1, enable_0)
            valid_1[index] |= pyrtl.MemBlock.EnabledWrite(1, enable_1)
            valid_2[index] |= pyrtl.MemBlock.EnabledWrite(1, enable_2)
            valid_3[index] |= pyrtl.MemBlock.EnabledWrite(1, enable_3)


# resp_hit <<= hit_result

# TODO: Determine output
with pyrtl.conditional_assignment: 
    with (req_new == 0b1) & (req_type == 0b0): #read
        with (hit_result == 0b1) & (hit_0 == 0b1):
            # resp_hit |= 0b1
            resp_data |= pyrtl.shift_right_logical(temp, data_shift_amount)[0:32]
        with (hit_result == 0b1) & (hit_1 == 0b1):
            # resp_hit |= 0b1
            resp_data |= pyrtl.shift_right_logical(temp, data_shift_amount)[0:32]
        with (hit_result == 0b1) & (hit_2 == 0b1):
            # resp_hit |= 0b1
            resp_data |= pyrtl.shift_right_logical(temp, data_shift_amount)[0:32]
        with (hit_result == 0b1) & (hit_3 == 0b1):
            # resp_hit |= 0b1
            resp_data |= pyrtl.shift_right_logical(temp, data_shift_amount)[0:32]
        with (hit_result == 0b0): #read miss
            resp_data |= 0b0
            # resp_hit |= 0b0
    with (req_new == 0b1) & (req_type == 0b1): #write 
        with (hit_result) & hit_0:
            # resp_hit |= 0b1
            resp_data |= 0b0
        with (hit_result) & hit_1:
            # resp_hit |= 0b1
            resp_data |= 0b0
        with (hit_result) & hit_2:
            # resp_hit |= 0b1
            resp_data |= 0b0
        with (hit_result) & hit_3:
            # resp_hit |= 0b1
            resp_data |= 0b0
        with ~(hit_result): #write miss 
            resp_data |= 0b0
            # resp_hit |= 0b0
    with (req_new == 0b0):
        resp_data |= 0b0
        # resp_hit |= 0b0
    
        
    
    


            
    #with req_new == 0b01 & 
        #resp_data |= pyrtl.shift_right_logical(pyrtl.Const(0x0ffffffff, bitwidth=128), data_shift_amount)
    # need to shift back 32 bits for read 
    # read, dont hit --> 0 
    # write, --> 0 
############################## SIMULATION ######################################

def TestNoRequest(simulation, trace, addr=1024):
    simulation.step({
        'req_new':0,
        'req_addr':addr,
        'req_type':0,
        'req_data':0,
    })

    assert(trace.trace["resp_hit"][-1] == 0)
    assert(trace.trace["resp_data"][-1] == 0)
    print("Passed No Request Case!")

# Precondition: addr is not already in the cache.
# Postcondition: There is a cache miss. 
def TestMiss(simulation, trace, addr = 0):
    simulation.step({
        'req_new':1,
        'req_addr':addr,
        'req_type':0,
        'req_data':0,
    })

    assert(trace.trace["resp_hit"][-1] == 0)
    assert(trace.trace["resp_data"][-1] == 0)

    print("Passed Miss Case!")

# Precondition: addr is already in the cache.
# Postcondition: There is a cache hit and the cache returns
# the expected word. 
def TestHit(simulation, trace, addr = 0, expected_data = 0):
    simulation.step({
        'req_new':1,
        'req_addr':addr,
        'req_type':0,
        'req_data':0,
    })

    assert(trace.trace["resp_hit"][-1] == 1)
    assert(trace.trace["resp_data"][-1] == expected_data) 

    print("Passed Hit Case!")

# Precondition: addr is already in the cache.
# Postcondition: The word located at memory address 'addr'
# has been replaced with 'new_data'.
def TestWrite(simulation, trace, addr=0, new_data=156):
    simulation.step({
        'req_new': 1,
        'req_addr': addr,
        'req_type': 1,
        'req_data': new_data,
    })

    assert(trace.trace["resp_hit"][-1] == 1)
    assert(trace.trace["resp_data"][-1] == 0) 

    # Read back the correct value
    simulation.step({
        'req_new': 1,
        'req_addr': addr,
        'req_type': 0,
        'req_data': 0,
    })

    assert(trace.trace["resp_hit"][-1] == 1)
    assert(trace.trace["resp_data"][-1] == new_data) 
    print("Passed Write Test!")

# Precondition: addr does not already hit in the cache.
# Postcondition: addr exists in the cache at the correct
# cache index
def TestCorrectIndex(simulation, trace, addr = 32):
    simulation.step({
        'req_new': 1,
        'req_addr': addr,
        'req_type': 0,
        'req_data': 0,
    })

    assert(trace.trace["resp_hit"][-1] == 0)
    assert(trace.trace["resp_data"][-1] == 0) 

    bin_addr = bin(addr)[2:]
    missing_bits = 32 - len(bin_addr)
    if missing_bits > 0:
        bin_addr = ("0" * missing_bits) + bin_addr

    cache_index = int("0b" + bin_addr[-8:-4], 2)
    tag = int("0b" + bin_addr[:24], 2)

    tag_0_val = float('inf') if cache_index not in simulation.inspect_mem(tag_0) else simulation.inspect_mem(tag_0)[cache_index]
    tag_1_val = float('inf') if cache_index not in simulation.inspect_mem(tag_1) else simulation.inspect_mem(tag_1)[cache_index]
    tag_2_val = float('inf') if cache_index not in simulation.inspect_mem(tag_2) else simulation.inspect_mem(tag_2)[cache_index]
    tag_3_val = float('inf') if cache_index not in simulation.inspect_mem(tag_3) else simulation.inspect_mem(tag_3)[cache_index]

    assert((tag_0_val == tag) or (tag_1_val == tag) or (tag_2_val == tag) or (tag_3_val == tag))

    # Ensure that we hit in the next cycle.
    simulation.step({
        'req_new': 1,
        'req_addr': addr,
        'req_type': 0,
        'req_data': 0,
    })

    assert(trace.trace["resp_hit"][-1] == 1)
    assert(trace.trace["resp_data"][-1] == 0) 

    print("Passed Correct Index Test!")

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

TestNoRequest(sim, sim_trace)
TestMiss(sim, sim_trace)
TestHit(sim, sim_trace)
TestWrite(sim, sim_trace)
TestCorrectIndex(sim, sim_trace)

# Print trace
# sim_trace.render_trace(symbol_len=8)