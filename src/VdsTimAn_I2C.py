import sys
import os
import numpy as np
import datetime
from TimAn import *
from TimAnSettings import *
from TimAnMakeFig import *
from vdsDat import *
from getArgs import *

argSettings = { #指定子: [キー, 必須, 複数可, 名称]
    '': ['srcFile', True, False, 'ソースファイル']
    ,'-s': ['mainSplit', False, False, 'メイン領域分割数']
}
args = getArgs(argSettings)
if args == None: exit()

type = 'I2C'
logicLevel = 3.3
ths = [[logicLevel * 0.3, logicLevel * 0.7] for i in range(2)]
chn = [0, 1]    #トレースチャネル番号
chs = [
    ['SCL', 'SDA']     #信号名
    ,['red', 'orange']  #ライン色
]

# 波形データ取得
srcFile = args['srcFile'][0]
with open(srcFile, 'rb') as f:
    srcDat = f.read()
dat0 = vdsDat(srcDat)
timestep = 20 * dat0.tbScale / dat0.chI[0].samplesPerScreen
xmin = timestep * (dat0.chI[0].samplesPerScreen * dat0.tbOffset / 1000  - dat0.chI[0].sizDat / 2)
xmax = timestep * dat0.chI[0].sizDat + xmin
tim = np.arange(xmin, xmax, timestep)
dat = []
for chi, chd in zip(dat0.chI, dat0.chDat):
    dat.append((np.array(chd) - chi.vOffset) * chi.VPP)

# 解析
tas = TASettings(type, logicLevel, ths, chn)
tas.timestep = timestep
ta = TimingAnalyzer(tas.tas)
tdat = np.array(dat).T
dlen = len(tdat)
for idx in range(0,dlen,10000):
    to = idx + 10000
    if to > dlen: to = dlen
    print('\r', to, '/', dlen, end='')
    for tm, dt in zip(tim[idx:to], tdat[idx:to]):
        ta.datain(tm, dt)

# 波形画像生成
dstDir = 'ta_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
zs = zoomScales(timestep*20)
#mainZoom算出
minmax = [1E9, -1E9]
for ds in tas.disp:
    hg = ta.hg[ds[0]]
    if len(hg):
        if minmax[0] > hg[0][1]: minmax[0] = hg[0][1]
        if minmax[1] < hg[-1][0]: minmax[1] = hg[-1][0]
mainSplit = int(args['mainSplit'][0]) if len(args['mainSplit']) else 1
tRange = (minmax[1] - minmax[0]) / mainSplit
tas.mainZoom = [[minmax[0] - tRange*0.05 + i*tRange, minmax[0] + tRange*1.05 + i*tRange] for i in range(mainSplit)]
dispList = plotTa(tim, dat, ta, tas, chs, zs, dstDir)

# xlsx生成
info = [
    ['Data File', srcFile, '']
    ,['Time Step', timestep, '##0E+0']
    ,['Record Length', len(tdat), '']
]
taXlsx(ta, tas, dispList, info, dstDir)
