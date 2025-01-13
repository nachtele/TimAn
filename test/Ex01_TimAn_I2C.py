import sys
sys.path.append('../src/')
import datetime
import json
from wave_I2C import *
from TimAn import *
from TimAnSettings import *
from TimAnMakeFig import *

if __name__ == '__main__':
    pt = 'S92K01KS93K72KA0NPS'
    dat = wave_dat(pt)
    timestep = 20E-9
    type = 'I2C'
    logicLevel = 3.3
    ths = [[logicLevel * 0.3, logicLevel * 0.7] for i in range(2)]
    chn = [0, 1]    #トレースチャネル番号
    chs = [
        ['SCL', 'SDA']     #信号名
        ,['red', 'orange']  #ライン色
    ]
    tas = TASettings(type, logicLevel, ths, chn)
    tas.timestep = timestep
    ta = TimingAnalyzer(tas.tas)
    tdat = np.array(dat).T
    tim = np.arange(0, len(tdat)*timestep, timestep)
    for tm, dt in zip(tim, tdat):
        ta.datain(tm, dt)
    dstDir = 'ta_'+ type + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    jlist = [
        ['tas', tas]
        , ['ta', ta]
    ]
    jd = {'wave':pt, 'chs':chs}
    jd |= {mk:{k:v for k,v in c.__dict__.items()} for mk, c in jlist}
    with open(dstDir+'.json', 'wt') as f:
        json.dump(jd, f)

    zs = zoomScales(1E-7)
    dispList = plotTa(tim, dat, ta, tas, chs, zs, dstDir)
    info = [
        ['Test Data', type, '']
        ,['Time Step', timestep, '##0E+0']
        ,['Record Length', len(tdat), '']
    ]
    taXlsx(ta, tas, dispList, info, dstDir)
