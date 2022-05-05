class TimingAnalyzer:
    def __init__(self, settings):
        self.settings = settings
        self.datCnt = 0 #データカウント
        self.v = {}     #現在値
        self.t = {}     #最終イベント時刻
        self.e = {}     #イベント発生フラグ
        self.hv = {}    #履歴(値)
        self.ht = {}    #履歴(時刻)
        self.hg = {}    #計算対象の値
        for sts in self.settings:
            for name, init, cnds in sts:
                self.v[name] = init[0]  #値
                self.t[name] = init[1]  #遷移時刻
                self.hv[name] = []      #履歴(値)
                self.ht[name] = []      #履歴(遷移時刻)
                self.hg[name] = []      #履歴(計算対象の値)
    def tgChk(self, r, tim, dat):  #演算対象割り当て
        if type(r) == list: #インデックス指定
            i = r[1]
            try:
                if r[0][0] == '$':
                    return(self.ht[r[0][1:]][i])   #対象の遷移時刻
                elif r[0][0] == '@':
                    return(self.ht[r[0][1:]][i])  #対象の遷移時刻
                else:
                    return(self.hv[r[0]][i])   #対象の値
            except:
                return None
        elif type(r) != str:
            return(r)               #即値
        elif r[0] == '$':
            return(dat[int(r[1:])]) #入力データ
        elif r[0] == '@':
            if len(r) == 1:
                return(tim)         #現在時刻
            else:
                return(self.t[r[1:]])  #対象の最新遷移時刻
        elif r[0] == '!':
            return(self.e[r[1:]])       #イベント発生フラグ
        else:
            return(self.v[r])       #対象の値
    def datain(self, tim, dat):
        noEv = True #このデータでこれまでにイベント発生無し
        for iSts, sts in enumerate(self.settings):
            if (iSts > 0) and noEv and (self.datCnt > 0):   #解析スキップ条件
                break
            for name, init, cnds in sts:
                self.e[name] = 0
                for cnd, vs in cnds:
                    for op, *rt in cnd:
                        matched = False
                        tg = []
                        for r in rt:
                            tgc = self.tgChk(r, tim, dat)
                            if tgc is None: break
                            tg.append(tgc)
                        if len(tg) < 2: break
                        if op == '==':
                            if not (tg[0] == tg[1]): break
                        elif op == '!=':
                            if not (tg[0] != tg[1]): break
                        elif op == '<':
                            if not (tg[0] < tg[1]): break
                        elif op == '>':
                            if not (tg[0] > tg[1]): break
                        else:
                            break
                        matched = True
                    if matched:
                        noEv = False    #イベント発生有り
                        op, *rt = vs
                        tg = []
                        for r in rt:
                            tg.append(self.tgChk(r, tim, dat))
                        self.t[name] = tim
                        self.ht[name].append(tim)
                        if op == '=':
                            va = tg[0]
                        elif op == '+':
                            va = tg[0] + tg[1]
                        elif op == '-':
                            va = tg[0] - tg[1]
                        else:
                            va = None
                        self.v[name] = va
                        self.hv[name].append(va)
                        self.hg[name].append(tg)
                        self.e[name] = 1
                        break
        self.datCnt += 1