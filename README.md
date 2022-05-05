# TimAn
## 概要

+ オシロスコープ等の波形データについてタイミング解析するツールです。(Setup Time、Hold Time、等)
+ matplotlibにより、解析結果に基づいた波形画像を作成することができます。
+ openpyxlにより、解析結果一覧と画像を張り付けたxlsxファイルを生成することができます。(LibreOffice Calc等でも開けます)
+ リスト形式の設定を作成することで、各種通信プロトコルなどに対応できます。とりあえずI2CとSPIの設定を作ってみました。
+ OWON VDSシリーズのバイナリーデータに対応したデータ読み取りモジュールを用意しています。これを差し替えれば他のオシロスコープにも対応できます。

## 対象環境

python3

## ファイル構成

+ /src
  + VdsTimAn_I2C.py (実行ファイル)VDSシリーズ用I2Cタイミング解析
  + TimAn.py  タイミング解析
  + TimAnSettings.py  解析・画像生成設定
  + TimAnMakeFig.py 波形画像生成
  + vdsDat.py   VDSシリーズ用データ読み取り
  + getArgs.py  コマンドライン引数取得
+ /test
  + Ex01_TimAn_I2C.py 波形解析テスト用(I2C)
  + Ex01_TimAn_SPI.py 波形解析テスト用(SPI)


## 使用方法

### VdsTimAn_I2C.py

OWONのVDSシリーズでバイナリーデータとして保存したI2C波形をタイミング解析する例です。
Ch1にSCL、Ch2にSDAを割り当てています。違う割り当ての場合は適宜書き換えてください。

---
    python VdsTimAn_I2C.py (データファイル名) [-s (メイン領域分割数)]
---

### Ex01_TimAn_I2C.py, Ex01_TimAn_SPI.py

波形解析のテスト用。疑似データを生成して解析・画像生成をテストするツールです(I2C, SPI用)。

---
    python Ex01_TimAn_I2C.py
---
