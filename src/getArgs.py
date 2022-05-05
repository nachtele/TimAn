import sys

def argNumCheck(argSettings, args):
    numErr = 0
    for op, [akey, req, plu, name] in argSettings.items():
        if req and len(args[akey]) == 0:
            print(f'{name}({op})を指定してください')
            numErr += 1
        if not plu and len(args[akey]) > 1:
            print(f'{name}({op})は1つだけ指定してください')
            numErr += 1
    return numErr

def getArgs(argSettings):
    defaultKey = argSettings[''][0] if '' in argSettings else None
    key = defaultKey
    res = {v:[] for v, *d in argSettings.values()}
    for a in sys.argv[1:]:
        if key == defaultKey:
            if a[0] == '-':
                if a in argSettings:
                    key = argSettings[a][0]
                    continue
                else:
                    print(a, 'は無効な指定子です')
                    return None
            elif defaultKey == None:
                print('指定子のない引数は指定できません')
                return None
        res[key].append(a)
        key = defaultKey
    numErr = argNumCheck(argSettings, res)
    return None if numErr else res

if __name__ == '__main__':
    argSettings = { #指定子: [キー, 必須, 複数可, 名称]
        '': ['srcFile', True, False, 'ソースファイル']
        ,'-o1': ['option1', False, False, 'オプション1']
        ,'-o2': ['option2', False, True, 'オプション2']
        ,'-o3': ['option3', True, False, 'オプション3']
        ,'-o4': ['option4', True, True, 'オプション4']
    }
    args = getArgs(argSettings)
    print(args)
