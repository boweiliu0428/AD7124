# debugging
import pandas as pd
import numpy as np

fclk = 614400
reg0 = pd.read_json('1 Ch.json')['Registers']

# Convert frequency to FS[10:0] value
def freq2fs(freq):
    return int(fclk / (32 * freq))

print(freq2fs(1600))