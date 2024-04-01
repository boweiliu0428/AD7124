# Copyright (C) 2019 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

import adi
# from scipy import signal
# import multiprocessing
import time
import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd

# Set up AD7124
ad7124 = adi.ad7124(uri="ip:localhost")
# ad_channel = 0

def foo():
    # sc = ad7124.scale_available

    # ad7124.channel[ad_channel].scale = sc[-1]  # get highest range
    ad7124.rx_output_type = "SI"
    # sets sample rate for all channels
    ad7124.sample_rate = 1600
    ad7124.rx_enabled_channels = [0,1,2,3,4,5,6,7]
    ad7124.rx_buffer_size = 100
    ad7124._ctx.set_timeout(100000)
    
#     ad7124.rx()
    
#     reg0 = pd.read_json('1 Ch.json')['Registers']
#     f = open('map.csv', 'w')
#     # set address 1: ADC_Control
# #     ad7124._ctrl.reg_write(1, int(reg0[1]['Value'], 16))
# #     print(bin(int(reg0[1]['Value'], 16)))
#     
# #     ad7124.rx()
# #     ad7124.rx()
# #     ad7124.rx()
#     
#     for addr in range(57):
#         val0 = int(reg0[addr]['Value'], 16)
#         reg = ad7124._ctrl.reg_read(addr) # read it back
#         if val0 - reg != 0:
# #             ad7124._ctrl.reg_write(addr, val0)
#             print('EVAL-SDP-CB1Z board is {0:24b}\n while Pi is {1:34b} for address {2:d}: {3:s}\n'
#               .format(val0, reg, addr, reg0[addr]['Name']))
#         f.write("{0:b}, {1:b}\n".format(addr, reg))
#     f.close()
    
    # raw = ad7124.channel[0].raw
#     data = np.array(ad7124.rx()) 
#     print([bin(i) for i in data.flatten()])
#     scale = 0.000298023
#     offset = -2500
#     data = data * scale + offset
#     print(data[5])
#     print(data)
    
    with open("test_data.csv", "a") as f:
        start_time = time.time()
        i=0
        while time.time() - start_time < 300:
            data = np.array(ad7124.rx()) 
            np.savetxt(f, data.T, delimiter=",")
            i += 1
            print(i)
    print("---%d runs use %s seconds ---" % (i, time.time() - start_time))
    
#     for addr in range(57):
#         val0 = int(reg0[addr]['Value'], 16)
#         reg = ad7124._ctrl.reg_read(addr) # read it back
#         if val0 - reg != 0:
# #             ad7124._ctrl.reg_write(addr, val0)
#             print('EVAL-SDP-CB1Z board is {0:24b}\n while Pi is {1:34b} for address {2:d}: {3:s}\n'
#               .format(val0, reg, addr, reg0[addr]['Name']))
            
    print(ad7124.channel[0].scale, ad7124.channel[0].offset)
    print(ad7124.rx_enabled_channels)
    
#     plt.plot(data)
    plt.plot(data[0], label='0')
    plt.plot(data[1], label='1')
    plt.plot(data[2], label='2')
    plt.plot(data[3], label='3')
    plt.plot(data[4], label='4')
    plt.plot(data[5], label='5')
    plt.plot(data[6], label='6')
    plt.plot(data[7], label='7')
    plt.grid()
    plt.xlabel('sample')
    plt.ylabel('mV')
    plt.legend(bbox_to_anchor=(1., 1.))
#     plt.savefig('fig/4-5_6-7_2.png')
    plt.show()

if __name__ == '__main__':
     foo()
     
#     # Start foo as a process
#     p = multiprocessing.Process(target=foo, name="Foo", args=())
#     p.start()
# 
#     # Wait a maximum of 10 seconds for foo
#     # Usage: join([timeout in seconds])
#     p.join(50)
# 
#     # If thread is active
#     if p.is_alive():
#         print ("foo is running... let's kill it...")
# 
#         # Terminate foo
#         p.terminate()
#         p.join()
