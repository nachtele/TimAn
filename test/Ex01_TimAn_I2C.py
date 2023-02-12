import re
import numpy as np
import datetime
from TimAn import *
from TimAnSettings import *
from TimAnMakeFig import *

def sampleDat():
    v = 0.0; r = [v := v * 0.8 + 3.3 * 0.2 for i in range(20)]
    v = 3.3; f = [v := v * 0.5 + 0.0 * 0.5 for i in range(20)]
    l = np.full(20, 0.0)
    h = np.full(20, 3.3)
    pt = 'S92K01KS93K72KA0NPS'
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

if __name__ == '__main__':
    dat = sampleDat()
    type = 'I2C'
    logicLevel = 3.3
    ths = [[logicLevel * 0.3, logicLevel * 0.7] for i in range(2)]
    chn = [0, 1]    #トレースチャネル番号
    chs = [
        ['SCL', 'SDA']     #信号名
        ,['red', 'orange']  #ライン色
    ]
    tas = TASettings(type, logicLevel, ths, chn)
    ta = TimingAnalyzer(tas.tas)
    tdat = np.array(dat).T
    timestep = 20E-9
    tim = np.arange(0, len(tdat)*timestep, timestep)
    for tm, dt in zip(tim, tdat):
        ta.datain(tm, dt)
    dstDir = 'ta_'+ type + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    zs = zoomScales(1E-7)
    dispList = plotTa(tim, dat, ta, tas, chs, zs, dstDir)
    info = [
        ['Test Data', type, '']
        ,['Time Step', timestep, '##0E+0']
        ,['Record Length', len(tdat), '']
    ]
    taXlsx(ta, tas, dispList, info, dstDir)
