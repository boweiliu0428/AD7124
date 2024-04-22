# debugging
import pandas as pd

fclk = 614400
reg0 = pd.read_json('1 Ch.json')['Registers']

ft = 'sinc4'
# set filter of ADC. Only sinc4 or sinc3 filter (without averaging block) are implemented.
if ft != 'sinc4' and ft != 'sinc3':
    raise NotImplementedError('Choose sinc4 or sinc3 filter! Other filters not implemented')
# s = '000001100000000000000001' # sps 19200
# s = '000001100000000000001100' # sps 1600
# s = '000001100000000110000000' # sps 50
for addr in range(33, 41):
    reg = int('111101100000000000001100', 2)
    print('Register {0:d}: {1:s} has value {2:24b}'.format(addr, reg0[addr]['Name'], reg))
    if ft == 'sinc4':
        print('Setting sinc4 filter')
        reg = reg % (2**21) + 2 ** 21 * 0
    elif ft == 'sinc3':
        print('Setting sinc3 filter')
        reg = reg % (2**21) + 2 ** 21 * 2
    # ad7124._ctrl.reg_write(addr, reg)
    print('Register {0:d}: {1:s} has value {2:24b}'.format(addr, reg0[addr]['Name'], reg))