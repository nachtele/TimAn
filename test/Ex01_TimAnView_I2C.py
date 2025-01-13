import sys
sys.path.append('../src/')
import json
import wx
import wx.grid
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.figure
import matplotlib.backends.backend_wxagg
from wave_I2C import *
from TimAnMakeFig import *

zs = zoomScales(1E-7)

class dict2class():
    def __init__(self, dic):
        self.__dict__ = dic

class DataTable(wx.grid.GridTableBase):
    def __init__(self, data, clabel):
        super().__init__()
        self.headerRows = 1
        self.data = data
        self.clabel = clabel
    def updateData(self, data):
        self.data = data
    def GetNumberRows(self):
        return len(self.data)
    def GetNumberCols(self):
        return len(self.clabel)
    def GetValue(self, row, col):
        return self.data[row][col]
    def SetValue(self, row, col, value):
        self.data[row][col] = value
    def GetColLabelValue(self, col):
        return self.clabel[col]
    def GetTypeName(self, row, col):
        return wx.grid.GRID_VALUE_STRING

class MyFrame(wx.Frame):
    def __init__(self, title, dat, taj):
        wx.Frame.__init__(self, None, -1, title, size=(1200,500))
        self.ta = dict2class(taj['ta']) #タイミング解析結果
        self.tas = dict2class(taj['tas'])   #タイミング解析設定
        self.chs = taj['chs']   #チャネル情報
        self.tagd = [None, None]    #Gridデータ
        self.tags = [   #Grid設定
            [200, ['name', 'n']]
            ,[250, ['value', 't0', 't1']]
        ]
        self.InitializeComponents()
        plt.rcParams['font.family'] = 'MS Gothic'
        self.dat = dat
        self.tim = np.arange(0, len(self.dat[0])*self.tas.timestep, self.tas.timestep)
        self.wave(self.dat, self.tim)

    def taGrid(self, ta, tas):
        self.tagd[1] = [[list(map(engFmt, [v, *g])) for v, g in zip(self.ta.hv[name], self.ta.hg[name])] for name, *d in self.tas.disp]
        self.tag1sel = [0 if len(d1) else -1 for d1 in self.tagd[1]]
        self.tag1zmin = [zs[np.searchsorted(zs, np.amin(np.abs(self.ta.hv[name]))*6)] for name, *d in self.tas.disp]
        self.tagd[0] = [[name, str(len(d1))] for [name, *_], d1 in zip(self.tas.disp, self.tagd[1])]
        self.table = [DataTable(d, l) for d, [_, l] in zip([self.tagd[0], self.tagd[1][0]], self.tags)] 
        self.tag = [wx.grid.Grid(self, wx.ID_ANY, size=(w, 450)) for w, *_ in self.tags]
        [gr.SetRowLabelSize(30) for gr in self.tag]
        [tag.SetTable(t) for tag, t in zip(self.tag, self.table)]
        [gr.AutoSize() for gr in self.tag]
        [gr.SetSelectionMode(wx.grid.Grid.GridSelectionModes.GridSelectRows) for gr in self.tag]
        [gr.EnableEditing(False) for gr in self.tag]
        [gr.DisableDragRowSize() for gr in self.tag]
        self.tag[0].Bind(wx.grid.EVT_GRID_SELECT_CELL, self.ev_tag0sel)
        self.tag[1].Bind(wx.grid.EVT_GRID_SELECT_CELL, self.ev_tag1sel)
        self.tag[0].SelectRow(0)

    def ev_tag0sel(self, evt):
        self.tag0sel = evt.GetRow()
        self.tag[0].SelectRow(self.tag0sel)
        self.table[1].updateData(self.tagd[1][self.tag0sel])
        self.tag[1].SetTable(self.table[1])
        self.tag[1].AutoSizeColumns()
        self.name, caption, self.ch, sel = self.tas.disp[self.tag0sel]
        self.tag[1].SetGridCursor(self.tag1sel[self.tag0sel], 0)
        plt.suptitle(caption)
        self.afig.hlines(self.ch)

    def ev_tag1sel(self, evt):
        sel = evt.GetRow()
        self.tag[1].SelectRow(sel)
        self.tag1sel[self.tag0sel] = sel
        afig_zoom(self.afig, self.ta, self.tas, self.ch, zs, self.tag1zmin[self.tag0sel], self.name, sel)
        self.canvas.draw()

    def InitializeComponents(self):
        self.sz0 = wx.FlexGridSizer(rows=1, cols=2, gap=(1, 1))
        self.taGrid(self.ta, self.tas)
        [self.sz0.Add(tag, flag=wx.GROW) for tag in self.tag]
        self.sz0.AddGrowableRow(0)
        self.fig = matplotlib.figure.Figure()
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, wx.ID_ANY, self.fig)
        self.sz1 = wx.FlexGridSizer(rows=1, cols=2, gap=(1, 1))
        self.sz1.Add(self.sz0)
        self.sz1.Add(self.canvas, flag=wx.GROW)
        self.sz1.AddGrowableRow(0)
        self.sz1.AddGrowableCol(1)
        self.SetSizer(self.sz1)

    def wave(self, dat, tim):
        self.afig= makeFig(self.fig, tim, dat, self.tas, self.chs)
        self.afig.setStr(self.ta, self.tas.strs)
        self.canvas.draw()
        # self.canvas.flush_events()

if __name__ == '__main__':
    title = sys.argv[0]
    jifile = sys.argv[1] + '.json'
    with open(jifile) as f:
        taj = json.load(f)    
    dat = wave_dat(taj['wave'])
    app = wx.App()
    fr = MyFrame(title, dat, taj)
    fr.Show(True)
    app.MainLoop()