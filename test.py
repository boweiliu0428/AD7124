# Copyright (C) 2019 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

import adi
# from scipy import signal
# import multiprocessing
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set up AD7124 
ad7124 = adi.ad7124(uri="ip:localhost")
# ad_channel = 0

def foo():
    # sc = ad7124.scale_available

    # ad7124.channel[ad_channel].scale = sc[-1]  # get highest range
    ad7124.rx_output_type = "SI"
    # sets sample rate for all channels
#     ad7124.sample_rate = 1600
    ad7124.rx_enabled_channels = [0,1,2,3,4,5,6,7]
    ad7124.rx_buffer_size = 2000
    ad7124._ctx.set_timeout(100000)
    
#     ad7124.rx()
    
    reg0 = pd.read_json('1 Ch.json')['Registers']
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

    s = '000001100000000000000001' # sps 19200
#     s = '000001100000000000001100' # sps 1600
#     s = '000001100000000110000000' # sps 50
    ad7124.sample_rate = 19200 / (int(s, 2) % (2**11))
    for addr in range(33, 41):
        val0 = int(reg0[addr]['Value'], 16)
        reg = ad7124._ctrl.reg_read(addr) # read it back
        print('EVAL-SDP-CB1Z board is {0:24b}\n while Pi is {1:34b} for address {2:d}: {3:s}\n'
              .format(val0, reg, addr, reg0[addr]['Name']))
        ad7124._ctrl.reg_write(addr, int(s, 2))
        print('EVAL-SDP-CB1Z board is {0:24b}\n while Pi is {1:34b} for address {2:d}: {3:s}\n'
              .format(val0, ad7124._ctrl.reg_read(addr), addr, reg0[addr]['Name']))
    print('asdfasd')

    # raw = ad7124.channel[0].raw
    data = np.array(ad7124.rx()) 
#     print([bin(i) for i in data.flatten()])
#     scale = 0.000298023
#     offset = -2500
#     data = data * scale + offset
    print(data[3])
#     print(data)
    print(max(data[0]),max(data[1]),max(data[2]),max(data[3]),max(data[4]),max(data[5]),max(data[6]),max(data[7]))
    print(min(data[0]),min(data[1]),min(data[2]),min(data[3]),min(data[4]),min(data[5]),min(data[6]),min(data[7]))
    
#     with open("test_data.csv", "a") as f:
#         start_time = time.time()
#         i=0
#         while time.time() - start_time < 300:
#             data = np.array(ad7124.rx()) 
#             np.savetxt(f, data.T, delimiter=",")
#             i += 1
#             print(i)
#     print("---%d runs use %s seconds ---" % (i, time.time() - start_time))
    
    for addr in range(57):
        val0 = int(reg0[addr]['Value'], 16)
        reg = ad7124._ctrl.reg_read(addr) # read it back
        if val0 - reg != 0:
#             ad7124._ctrl.reg_write(addr, val0)
            print('EVAL-SDP-CB1Z board is {0:24b}\n while Pi is {1:34b} for address {2:d}: {3:s}\n'
              .format(val0, reg, addr, reg0[addr]['Name'])) 
            
    print(ad7124.channel[0].scale, ad7124.channel[0].offset)
    print(ad7124.rx_enabled_channels)
    
    fig, (ax0, ax1) = plt.subplots(2, 1)
#     plt.plot(data)
    ax0.plot(data[0], label='0')
    ax0.plot(data[1], label='1')
    ax0.plot(data[2], label='2')
    ax0.plot(data[3], label='3')
    ax0.plot(data[4], label='4')
    ax0.plot(data[5], label='5')
    ax0.plot(data[6], label='6')
    ax0.plot(data[7], label='7')
    ax0.grid()
    ax0.set_xlabel('sample')
    ax0.set_ylabel('mV')
    ax0.legend(bbox_to_anchor=(1., 1.))
    
    ax1.psd(data[3], ad7124.rx_buffer_size, ad7124.sample_rate/32)
    print(ad7124.sample_rate/32)
    plt.tight_layout()
    plt.savefig('fig/60Hz'+s+'.png')
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