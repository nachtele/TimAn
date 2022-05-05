import struct

TBScales = [float(str(a)+'e'+str(b)) for b in range(-9,3) for a in [1,2,5]][1:34]
VScales = [float(str(a)+'e'+str(b)) for b in range(-3,1) for a in [1,2,5]][1:12]

class vdsDat:
    sizHed = 32 #ヘッダーのサイズ
    sizChI = 67 #チャネル情報(1ch分)のサイズ
    sizTbI = 27 #タイムベース情報のサイズ
    class chInfo:
        def __init__(self, src):
            self.dat = src
            name, self.sizInfo, self.inv, d0, self.samplesPerScreen, d1, d2, d3, d4, \
             self.sizDat, d6, self.vOffset, self.scaleCode, self.probeRateCode, d7, d8, self.ofsDat \
             = struct.unpack('>3s16i', src)
            self.name = name.decode()
            self.probeRate = 10**self.probeRateCode
            self.scale = VScales[self.scaleCode] * self.probeRate
            self.VPP = self.scale / 25

    def __init__(self, src):
        self.header = src[0:self.sizHed]
        model, self.sizFile, self.sizDat = struct.unpack('>10s13x1i1x1i', self.header)
        self.model = model.decode

        pt = self.sizHed + self.sizDat  #データポインター
        self.tbInfo = src[pt:pt+self.sizTbI]
        self.tbScaleCode, self.tbOffset, self.sizChIs = struct.unpack('>17x1b1i3x1H', self.tbInfo)
        self.tbScale = TBScales[self.tbScaleCode]
        self.numCh = self.sizChIs // self.sizChI
        pt += self.sizTbI
        self.chI = [self.chInfo(src[p:p+self.sizChI]) for p in range(pt, pt+self.sizChIs, self.sizChI)]

        self.sizChD = self.sizDat // self.numCh
        pt = self.sizHed
        f = str(self.sizChD) + 'b'
        self.chDat = [struct.unpack(f, src[p:p+self.sizChD]) for p in range(pt, pt + self.sizDat, self.sizChD)]
