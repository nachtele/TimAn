# サンプル波形生成(I2C)
import re
import numpy as np

def wave_dat(pt):
    v = 0.0; r = [v := v * 0.8 + 3.3 * 0.2 for i in range(20)]
    v = 3.3; f = [v := v * 0.5 + 0.0 * 0.5 for i in range(20)]
    l = np.full(20, 0.0)
    h = np.full(20, 3.3)
    dat = [[], []]
    lastbit = None
    rept = re.compile('[0-9a-fA-F]')
    ptb = ''
    for p in pt:
        if rept.match(p):
            ptb += format(int('0x'+p, 0), '04b')
        else:
            ptb += p
    for p in ptb:
        if p == 'S':    #Start
            dat[0] += [h,h,h,h,f] if (lastbit == None) else [l,l,r,h,h,h,f]
            dat[1] += [h,h,f,l,l] if (lastbit != '0')  else [r,h,h,h,f,l,l]
            lastbit = '0'
        elif p == 'P':  #Stop
            dat[0] += [l,l,r,h,h]
            dat[1] += [l,l,l,l,r] if (lastbit == '0')  else [f,l,l,l,r]
            lastbit = None
        elif p == '0' or p == 'K':  #0 or Ack
            dat[0] += [l,l,r,h,f]
            dat[1] += [l,l,l,l,l] if (lastbit == '0') else [f,l,l,l,l]
            lastbit = '0'
        elif p == '1' or p == 'N':  #1 or Nack
            dat[0] += [l,l,r,h,f]
            dat[1] += [h,h,h,h,h] if (lastbit == '1') else [r,h,h,h,h]
            lastbit = '1'
    return([np.hstack(d) for d in dat])
