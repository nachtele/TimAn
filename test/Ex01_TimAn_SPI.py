import re
import numpy as np
import datetime
from TimAn import *
from TimAnSettings import *
from TimAnMakeFig import *

def sampleDat():
    v = 0.0; r = [v := v * 0.5 + 3.3 * 0.5 for i in range(20)]
    v = 3.3; f = [v := v * 0.5 + 0.0 * 0.5 for i in range(20)]
    l = np.full(20, 0.0)
    h = np.full(20, 3.3)
    pt = [
        ' 031000!!02105A ',
        ' FFFF59  FFFFFF '
    ]
    dat = [[] for i in range(4)]
    lastbit = ['1', '0', '0', '1']
    rept = re.compile('[0-9a-fA-F]')
    ptb = ['', '']
    for pp in zip(pt[0], pt[1]):
        for i, p in enumerate(pp):
            if rept.match(p):
                ptb[i] += format(int('0x'+p, 0), '04b')
            else:
                ptb[i] += p
    for pp in zip(ptb[0], ptb[1]):
        if pp[0] == ' ' or pp[0] == '!':
            dat[0] += [h,h] if (lastbit[0] == '1') else [r,h] #CS
            lastbit[0] = '1'
            dat[2] += [f,l] if (lastbit[2] == '1') else [l,l] #MOSI
            lastbit[2] = '0'
            dat[3] += [h,h] if (lastbit[3] == '1') else [r,h] #MISO
            lastbit[3] = '1'
            if pp[0] == ' ':    #SCK
                dat[1] += [f,l] if (lastbit[1] == '1') else [l,l]
                lastbit[1] = '0'
            else:
                dat[1] += [f,r] if (lastbit[1] == '1') else [l,r]
                lastbit[1] = '1'
        else:
            dat[0] += [f,l] if (lastbit[0] == '1') else [l,l]
            lastbit[0] = '0'
            dat[1] += [f,r] if (lastbit[1] == '1') else [l,r]
            lastbit[1] = '1'
            for i, p in enumerate(pp):
                if p == '0':
                    dat[i+2] += [f,l] if (lastbit[i+2] == '1') else [l,l]
                else:
                    dat[i+2] += [h,h] if (lastbit[i+2] == '1') else [r,h]
                lastbit[i+2] = p
    return([np.hstack(d) for d in dat])

if __name__ == '__main__':
    dat = sampleDat()
    type = 'SPI'
    logicLevel = 3.3
    ths = [[logicLevel * 0.3, logicLevel * 0.7] for i in range(4)]
    chn = [0, 1, 2, 3]    #トレースチャネル番号
    chs = [
        ['CS', 'SCK', 'MOSI', 'MISO']     #信号名
        ,['red', 'orange', 'blue', 'purple']  #ライン色
    ]
    tas = TASettings(type, logicLevel, ths, chn)
    ta = TimingAnalyzer(tas.tas)
    tdat = np.array(dat).T
    timestep = 20E-9
    tas.timestep = timestep
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
