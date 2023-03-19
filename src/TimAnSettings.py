def TASettings_SPI(
    ths     #閾値
    ,chn    #チャネル番号
):
    thCS, thSCK, thMOSI, thMISO = ths
    cCS, cSCK, cMOSI, cMISO = chn
    chCS = '$' + str(cCS)
    chSCK = '$' + str(cSCK)
    chMOSI = '$' + str(cMOSI)
    chMISO = '$' + str(cMISO)
    tas = [
        [   #全データポイント解析
        ['CS', [3, None], [
            [[['>', 'CS', 1], ['<', chCS, thCS[0]]], ['=', 0]]
            ,[[['<', 'CS', 2], ['>', chCS, thCS[1]]], ['=', 3]]
            ,[[['==', 'CS', 0], ['>', chCS, thCS[0]]], ['=', 1]]
            ,[[['==', 'CS', 3], ['<', chCS, thCS[1]]], ['=', 2]]
        ]]
        ,['SCK', [0, None], [
            [[['>', 'SCK', 1], ['<', chSCK, thSCK[0]]], ['=', 0]]
            ,[[['<', 'SCK', 2], ['>', chSCK, thSCK[1]]], ['=', 3]]
            ,[[['==', 'SCK', 0], ['>', chSCK, thSCK[0]]], ['=', 1]]
            ,[[['==', 'SCK', 3], ['<', chSCK, thSCK[1]]], ['=', 2]]
        ]]
        ,['MOSI', [0, None], [
            [[['>', 'MOSI', 1], ['<', chMOSI, thMOSI[0]]], ['=', 0]]
            ,[[['<', 'MOSI', 2], ['>', chMOSI, thMOSI[1]]], ['=', 3]]
            ,[[['==', 'MOSI', 0], ['>', chMOSI, thMOSI[0]]], ['=', 1]]
            ,[[['==', 'MOSI', 3], ['<', chMOSI, thMOSI[1]]], ['=', 2]]
        ]]
        ,['MISO', [3, None], [
            [[['>', 'MISO', 1], ['<', chMISO, thMISO[0]]], ['=', 0]]
            ,[[['<', 'MISO', 2], ['>', chMISO, thMISO[1]]], ['=', 3]]
            ,[[['==', 'MISO', 0], ['>', chMISO, thMISO[0]]], ['=', 1]]
            ,[[['==', 'MISO', 3], ['<', chMISO, thMISO[1]]], ['=', 2]]
        ]]
        ]
        ,[  #イベント有データポイントのみ解析
        ['tSCK', [0, None], [ #SCK period
            [[['==', 'wtSCK', 1], ['==', '!SCK', 1], ['==', 'SCK', 0]], ['-', '@', '@wtSCK']]
        ]]
        ,['wtSCK', [0, None], [ #Waiting for SCK period
            [[['==', 'wtSCK', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'CS', 0], ['==', '!SCK', 1], ['==', 'SCK', 0]], ['=', 1]]
        ]]
        ,['tCSS', [0, None], [ #CS setup time
            [[['==', 'wtCSS', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['-', '@', '@wtCSS']]
        ]]
        ,['wtCSS', [0, None], [ #Waiting for CS setup time
            [[['==', 'wtCSS', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['=', 0]]
            ,[[['==', 'wtCSS', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtCSS', 0], ['==', '!CS', 1], ['==', 'CS', 0]], ['=', 1]]
        ]]
        ,['tCSH', [0, None], [ #CS hold time
            [[['==', 'wtCSH', 1], ['==', '!CS', 1], ['==', 'CS', 3]], ['-', '@', '@wtCSH']]
        ]]
        ,['wtCSH', [0, None], [ #Waiting for CS hold time
            [[['==', 'wtCSH', 1], ['==', '!CS', 1], ['==', 'CS', 3]], ['=', 0]]
            ,[[['==', 'CS', 0],['==', '!SCK', 1], ['==', 'SCK', 3]], ['=', 1]]
        ]]
        ,['tCLD', [0, None], [ #Clock delay Time
            [[['==', 'wtCLD', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['-', '@', '@wtCLD']]
        ]]
        ,['wtCLD', [0, None], [ #Waiting for clock eelay time
            [[['==', 'wtCLD', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['=', 0]]
            ,[[['==', 'wtCLD', 1], ['<', 'CS', 3]], ['=', 0]]
            ,[[['==', 'wtCLD', 0], ['==', '!CS', 1], ['==', 'CS', 3]], ['=', 1]]
        ]]
        ,['tCLE', [0, None], [ #Clock enable time
            [[['==', 'wtCLE', 1], ['==', '!CS', 1], ['==', 'CS', 0]], ['-', '@', '@wtCLE']]
        ]]
        ,['wtCLE', [0, None], [ #Waiting for clock enable time
            [[['==', 'wtCLE', 1], ['==', '!CS', 1], ['==', 'CS', 0]], ['=', 0]]
            ,[[['==', 'CS', 3],['==', '!SCK', 1], ['==', 'SCK', 3]], ['=', 1]]
        ]]
        ,['tHIGH', [0, None], [ #SCK high time
            [[['==', 'wtHIGH', 1], ['==', '!SCK', 1], ['<', 'SCK', 3], ['==', ['SCK',-2], 3]], ['-', '@', ['@SCK',-2]]]
        ]]
        ,['wtHIGH', [0, None], [ #Waiting for SCK high time
            [[['==', 'wtHIGH', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtHIGH', 1], ['<', 'SCK', 3]], ['=', 0]]
            ,[[['==', 'wtHIGH', 0], ['==', 'CS', 0], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['=', 1]]
        ]]
        ,['tLOW', [0, None], [ #SCK Low time
            [[['==', 'wtLOW', 1], ['==', '!SCK', 1], ['>', 'SCK', 0], ['==', ['SCK',-2], 0]], ['-', '@', ['@SCK',-2]]]
        ]]
        ,['wtLOW', [0, None], [ #Waiting for SCK low time
            [[['==', 'wtLOW', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtLOW', 1], ['>', 'SCK', 0]], ['=', 0]]
            ,[[['==', 'wtLOW', 0], ['==', 'CS', 0], ['==', '!SCK', 1], ['==', 'SCK', 0]], ['=', 1]]
        ]]
        ,['tRSK', [0, None], [ #SCK rise time
            [[['==', '!SCK', 1], ['==', 'SCK', 3], ['==', ['SCK',-2], 1]], ['-', '@', ['@SCK',-2]]]
            ,[[['==', '!SCK', 1], ['==', 'SCK', 3]], ['-', '@', '@']]
        ]]
        ,['tFSK', [0, None], [ #SCK fall time
            [[['==', '!SCK', 1], ['==', 'SCK', 0], ['==', ['SCK',-2], 2]], ['-', '@', ['@SCK',-2]]]
            ,[[['==', '!SCK', 1], ['==', 'SCK', 0]], ['-', '@', '@']]
        ]]
        ,['tDS_R', [0, None], [ #Data input setup time(rise)
            [[['==', 'wtDS_R', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['-', '@', '@wtDS_R']]
        ]]
        ,['wtDS_R', [0, None], [ #Waiting for data input setup time(rise)
            [[['==', 'wtDS_R', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtDS_R', 1], ['<', 'MOSI', 3]], ['=', 0]]
            ,[[['==', 'wtDS_R', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['=', 0]]
            ,[[['==', 'wtDS_R', 0], ['==', 'CS', 0], ['==', '!MOSI', 1], ['==', 'MOSI', 3]], ['=', 1]]
        ]]
        ,['tDS_F', [0, None], [ #Data input setup time(fall)
            [[['==', 'wtDS_F', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['-', '@', '@wtDS_F']]
        ]]
        ,['wtDS_F', [0, None], [ #Waiting for data input setup time(fall)
            [[['==', 'wtDS_F', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtDS_F', 1], ['>', 'MOSI', 0]], ['=', 0]]
            ,[[['==', 'wtDS_F', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['=', 0]]
            ,[[['==', 'wtDS_F', 0], ['==', 'CS', 0], ['==', '!MOSI', 1], ['==', 'MOSI', 0]], ['=', 1]]
        ]]
        ,['tDH_R', [0, None], [ #Data input hold time(rise)
            [[['==', 'wtDH_R', 1], ['==', '!MOSI', 1], ['>', 'MOSI', 0]], ['-', '@', '@wtDH_R']]
        ]]
        ,['wtDH_R', [0, None], [ #Waiting for data input hold time(rise)
            [[['==', 'wtDH_R', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtDH_R', 1], ['>', 'MOSI', 0]], ['=', 0]]
            ,[[['==', 'CS', 0], ['==', '!SCK', 1], ['==', 'SCK', 3], ['==', 'MOSI', 0]], ['=', 1]]
        ]]
        ,['tDH_F', [0, None], [ #Data input hold time(fall)
            [[['==', 'wtDH_F', 1], ['==', '!MOSI', 1], ['<', 'MOSI', 3]], ['-', '@', '@wtDH_F']]
        ]]
        ,['wtDH_F', [0, None], [ #Waiting for Data input hold time(fall)
            [[['==', 'wtDH_F', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtDH_F', 1], ['<', 'MOSI', 3]], ['=', 0]]
            ,[[['==', 'CS', 0], ['==', '!SCK', 1], ['==', 'SCK', 3], ['==', 'MOSI', 3]], ['=', 1]]
        ]]
        ,['tOH_R', [0, None], [ #Data output hold time(rise)
            [[['==', 'wtOH_R', 2], ['==', '!SCK', 1], ['>', 'SCK', 0]], ['-', '@wtOH_R', ['@SCK',-2]]]
            ,[[['==', 'wtOH_R', 2], ['==', '!CS', 1], ['>', 'CS', 0]], ['-', '@wtOH_R', '@SCK']]
        ]]
        ,['wtOH_R', [0, None], [ #Waiting for Data output hold time(rise)
            [[['==', '!tOH_R', 1]], ['=', 0]]
            ,[[['==', 'wtOH_R', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'CS', 0], ['==', 'SCK', 3], ['==', 'MISO', 0]], ['=', 1]]
            ,[[['==', 'wtOH_R', 1], ['>', 'MISO', 0]], ['=', 2]]
        ]]
        ,['tOH_F', [0, None], [ #Data output hold time(fall)
            [[['==', 'wtOH_F', 2], ['==', '!SCK', 1], ['>', 'SCK', 0]], ['-', '@wtOH_F', ['@SCK',-2]]]
            ,[[['==', 'wtOH_F', 2], ['==', '!CS', 1], ['>', 'CS', 0]], ['-', '@wtOH_F', '@SCK']]
        ]]
        ,['wtOH_F', [0, None], [ #Waiting for Data output hold time(fall)
            [[['==', '!tOH_F', 1]], ['=', 0]]
            ,[[['==', 'wtOH_F', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'CS', 0], ['==', 'SCK', 3], ['==', 'MISO', 3]], ['=', 1]]
            ,[[['==', 'wtOH_F', 1], ['<', 'MISO', 3]], ['=', 2]]
        ]]
        ,['tOD_R', [0, None], [ #Data output delay time(rise)
            [[['==', 'wtOD_R', 2], ['==', '!SCK', 1], ['>', 'SCK', 0]], ['-', '@wtOD_R', ['@SCK',-2]]]
            ,[[['==', 'wtOD_R', 2], ['==', '!CS', 1], ['>', 'CS', 0]], ['-', '@wtOD_R', '@SCK']]
        ]]
        ,['wtOD_R', [0, None], [ #Waiting for data output delay time(rise)
            [[['==', '!tOD_R', 1]], ['=', 0]]
            ,[[['==', 'wtOD_R', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'CS', 0], ['==', 'SCK', 3], ['==', 'MISO', 0]], ['=', 1]]
            ,[[['==', 'wtOD_R', 1], ['==', 'MISO', 3]], ['=', 2]]
        ]]
        ,['tOD_F', [0, None], [ #Data output delay time(fall)
            [[['==', 'wtOD_F', 2], ['==', '!SCK', 1], ['>', 'SCK', 0]], ['-', '@wtOD_F', ['@SCK',-2]]]
            ,[[['==', 'wtOD_F', 2], ['==', '!CS', 1], ['>', 'CS', 0]], ['-', '@wtOD_F', '@SCK']]
        ]]
        ,['wtOD_F', [0, None], [ #Waiting for data output delay time(fall)
            [[['==', '!tOD_F', 1]], ['=', 0]]
            ,[[['==', 'wtOD_F', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'CS', 0], ['==', 'SCK', 3], ['==', 'MISO', 3]], ['=', 1]]
            ,[[['==', 'wtOD_F', 1], ['==', 'MISO', 0]], ['=', 2]]
        ]]
        ,['tMISOS_R', [0, None], [ #MISO input setup time(rise)
            [[['==', 'wtMISOS_R', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['-', '@', '@wtMISOS_R']]
        ]]
        ,['wtMISOS_R', [0, None], [ #Waiting for MISO input setup time(rise)
            [[['==', 'wtMISOS_R', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtMISOS_R', 1], ['<', 'MISO', 3]], ['=', 0]]
            ,[[['==', 'wtMISOS_R', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['=', 0]]
            ,[[['==', 'wtMISOS_R', 0], ['==', 'CS', 0], ['==', '!MISO', 1], ['==', 'MISO', 3]], ['=', 1]]
        ]]
        ,['tMISOS_F', [0, None], [ #MISO input setup time(fall)
            [[['==', 'wtMISOS_F', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['-', '@', '@wtMISOS_F']]
        ]]
        ,['wtMISOS_F', [0, None], [ #Waiting for MISO input setup time(fall)
            [[['==', 'wtMISOS_F', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtMISOS_F', 1], ['>', 'MISO', 0]], ['=', 0]]
            ,[[['==', 'wtMISOS_F', 1], ['==', '!SCK', 1], ['==', 'SCK', 3]], ['=', 0]]
            ,[[['==', 'wtMISOS_F', 0], ['==', 'CS', 0], ['==', '!MISO', 1], ['==', 'MISO', 0]], ['=', 1]]
        ]]
        ,['tMISOH_R', [0, None], [ #MISO input hold time(rise)
            [[['==', 'wtMISOH_R', 1], ['==', '!MISO', 1], ['>', 'MISO', 0]], ['-', '@', '@wtMISOH_R']]
        ]]
        ,['wtMISOH_R', [0, None], [ #Waiting for MISO input hold time(rise)
            [[['==', 'wtMISOH_R', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtMISOH_R', 1], ['>', 'MISO', 0]], ['=', 0]]
            ,[[['==', 'CS', 0], ['==', '!SCK', 1], ['==', 'SCK', 3], ['==', 'MISO', 0]], ['=', 1]]
        ]]
        ,['tMISOH_F', [0, None], [ #MISO input hold time(fall)
            [[['==', 'wtMISOH_F', 1], ['==', '!MISO', 1], ['<', 'MISO', 3]], ['-', '@', '@wtMISOH_F']]
        ]]
        ,['wtMISOH_F', [0, None], [ #Waiting for MISO input hold time(fall)
            [[['==', 'wtMISOH_F', 1], ['>', 'CS', 0]], ['=', 0]]
            ,[[['==', 'wtMISOH_F', 1], ['<', 'MISO', 3]], ['=', 0]]
            ,[[['==', 'CS', 0], ['==', '!SCK', 1], ['==', 'SCK', 3], ['==', 'MISO', 3]], ['=', 1]]
        ]]
        ]
    ]
    return tas

def DispSettings_SPI(
    ths     #閾値
    ,chn    #チャネル番号
):
    thCS, thSCK, thMOSI, thMISO = ths
    cCS, cSCK, cMOSI, cMISO = chn
    return [
        ['tSCK', 'tSCK: SCK period', [[cSCK, thSCK[0]], [cSCK, thSCK[0]]], ['min', 'max']]
        ,['tCSS', 'tCSS: CS setup time', [[cSCK, thSCK[0]], [cCS, thCS[0]]], ['all']]
        ,['tCSH', 'tCSH: CS hold time', [[cCS, thCS[0]], [cSCK, thSCK[1]]], ['all']]
        ,['tCLD', 'tCLD: Clock delay time', [[cSCK, thSCK[1]], [cCS, thCS[1]]], ['all']]
        ,['tCLE', 'tCLE: Clock enable time', [[cCS, thCS[0]], [cSCK, thSCK[1]]], ['all']]
        ,['tHIGH', 'tHIGH: SCK high time', [[cSCK, thSCK[0]], [cSCK, thSCK[0]]], ['min', 'max']]
        ,['tLOW', 'tLOW: SCK low time', [[cSCK, thSCK[0]], [cSCK, thSCK[0]]], ['min', 'max']]
        ,['tRSK', 'tRSK: SCK rise time', [[cSCK, thSCK[1]], [cSCK, thSCK[0]]], ['min', 'max']]
        ,['tFSK', 'tFSK: SCK fall time', [[cSCK, thSCK[0]], [cSCK, thSCK[1]]], ['min', 'max']]
        ,['tDS_R', 'tDS_R: Data input setup time(rise)', [[cSCK, thSCK[0]], [cMOSI, thMOSI[1]]], ['all']]
        ,['tDS_F', 'tDS_F: Data input setup time(fall)', [[cSCK, thSCK[0]], [cMOSI, thMOSI[0]]], ['all']]
        ,['tDH_R', 'tDH_R: Data input hold time(rise)', [[cMOSI, thMOSI[0]], [cSCK, thSCK[1]]], ['all']]
        ,['tDH_F', 'tDH_F: Data input hold time(fall)', [[cMOSI, thMOSI[1]], [cSCK, thSCK[1]]], ['all']]
        ,['tOH_R', 'tOH_R: Data output hold time(rise)', [[cMISO, thMISO[0]], [cSCK, thSCK[0]]], ['all']]
        ,['tOH_F', 'tOH_F: Data output hold time(fall)', [[cMISO, thMISO[1]], [cSCK, thSCK[0]]], ['all']]
        ,['tOD_R', 'tOD_R: Data output delay time(rise)', [[cMISO, thMISO[1]], [cSCK, thSCK[0]]], ['all']]
        ,['tOD_F', 'tOD_F: Data output delay time(fall)', [[cMISO, thMISO[0]], [cSCK, thSCK[0]]], ['all']]
        ,['tMISOS_R', 'tMISOS_R: MISO input setup time(rise)', [[cSCK, thSCK[1]], [cMISO, thMISO[1]]], ['all']]
        ,['tMISOS_F', 'tMISOS_F: MISO input setup time(fall)', [[cSCK, thSCK[1]], [cMISO, thMISO[0]]], ['all']]
        ,['tMISOH_R', 'tDH_R: MISO input hold time(rise)', [[cMISO, thMISO[0]], [cSCK, thSCK[1]]], ['all']]
        ,['tMISOH_F', 'tDH_F: MISO input hold time(fall)', [[cMISO, thMISO[1]], [cSCK, thSCK[1]]], ['all']]
]

def StrSettings_SPI(
    chn    #チャネル番号
):
    return [
    ]

def TASettings_I2C(
    ths     #閾値
    ,chn    #チャネル番号
):
    thSCL, thSDA = ths
    cSCL, cSDA = chn
    chSCL = '$' + str(cSCL)
    chSDA = '$' + str(cSDA)
    tas = [
        [   #全データポイント解析
        ['SCL', [3, None], [
            [[['>', 'SCL', 1], ['<', chSCL, thSCL[0]]], ['=', 0]]
            ,[[['<', 'SCL', 2], ['>', chSCL, thSCL[1]]], ['=', 3]]
            ,[[['==', 'SCL', 0], ['>', chSCL, thSCL[0]]], ['=', 1]]
            ,[[['==', 'SCL', 3], ['<', chSCL, thSCL[1]]], ['=', 2]]
        ]]
        ,['SDA', [3, None], [
            [[['>', 'SDA', 1], ['<', chSDA, thSDA[0]]], ['=', 0]]
            ,[[['<', 'SDA', 2], ['>', chSDA, thSDA[1]]], ['=', 3]]
            ,[[['==', 'SDA', 0], ['>', chSDA, thSDA[0]]], ['=', 1]]
            ,[[['==', 'SDA', 3], ['<', chSDA, thSDA[1]]], ['=', 2]]
        ]]
        ]
        ,[  #イベント有データポイントのみ解析
        ['tSCL', [0, None], [ #SCL period
            [[['==', 'wtSCL', 1], ['==', '!SCL', 1], ['==', 'SCL', 0]], ['-', '@', '@wtSCL']]
        ]]
        ,['wtSCL', [0, None], [ #Waiting for SCL period
            [[['==', 'wtSCL', 1], ['==', 'St', 1]], ['=', 0]]
            ,[[['==', 'wtSCL', 1], ['==', 'Sp', 1]], ['=', 0]]
            ,[[['==', '!SCL', 1], ['==', 'SCL', 0]], ['=', 1]]
        ]]
        ,['tR_SCL', [0, None], [ #SCL rise time
            [[['==', '!SCL', 1], ['==', 'SCL', 3], ['==', ['SCL',-2], 1]], ['-', '@', ['@SCL',-2]]]
            ,[[['==', '!SCL', 1], ['==', 'SCL', 3]], ['-', '@', '@']]
        ]]
        ,['tF_SCL', [0, None], [ #SCL fall time
            [[['==', '!SCL', 1], ['==', 'SCL', 0], ['==', ['SCL',-2], 2]], ['-', '@', ['@SCL',-2]]]
            ,[[['==', '!SCL', 1], ['==', 'SCL', 0]], ['-', '@', '@']]
        ]]
        ,['tLOW', [0, None], [  #SCL low time
            [[['==', '!SCL', 1], ['>', 'SCL', 0], ['==', ['SCL',-2], 0]], ['-', '@', ['@SCL',-2]]]
        ]]
        ,['tHIGH', [0, None], [ #SCL high time
            [[['==', '!SCL', 1], ['<', 'SCL', 3], ['==', ['SCL',-2], 3], ['==', 'St', 0]], ['-', '@', ['@SCL',-2]]]
        ]]
        ,['tR_SDA', [0, None], [    #SDA rise time
            [[['==', '!SDA', 1], ['==', 'SDA', 3], ['==', ['SDA',-2], 1]], ['-', '@', ['@SDA',-2]]]
            ,[[['==', '!SDA', 1], ['==', 'SDA', 3]], ['-', '@', '@']]
        ]]
        ,['tF_SDA', [0, None], [ #SDA fall time
            [[['==', '!SDA', 1], ['==', 'SDA', 0], ['==', ['SDA',-2], 2]], ['-', '@', ['@SDA',-2]]]
            ,[[['==', '!SDA', 1], ['==', 'SDA', 0]], ['-', '@', '@']]
        ]]
        ,['tSU_STA', [0, None], [ #Start condition setup time
            [[['==', 'wtSU_STA', 1], ['<', 'SDA', 3]], ['-', '@', '@wtSU_STA']]
        ]]
        ,['wtSU_STA', [0, None], [ #Waiting for Start condition setup time
            [[['==', 'wtSU_STA', 0], ['==', '!SCL', 1], ['==', 'SCL', 3], ['==', 'SDA', 3]], ['=', 1]]
            ,[[['==', 'wtSU_STA', 1], ['<', 'SCL', 3]], ['=', 0]]
            ,[[['==', 'wtSU_STA', 1], ['<', 'SDA', 3]], ['=', 0]]
        ]]
        ,['tHD_STA', [0, None], [ #Start condition hold time
            [[['==', 'StC0', 1], ['==', 'St', 1], ['<', 'SCL', 3]], ['-', '@', '@St']]
        ]]
        ,['tBUF', [0, None], [  #Bus free time
            [[['==', 'wtBUF', 1], ['<', 'SDA', 3]], ['-', '@', '@wtBUF']]
        ]]
        ,['wtBUF', [0, None], [ #Waiting for Bus free time
            [[['==', 'wtBUF', 0], ['==', 'SpC0', 1], ['==', 'SDA', 3]], ['=', 1]]
            ,[[['==', 'wtBUF', 1], ['<', 'SCL', 3]], ['=', 0]]
            ,[[['==', 'wtBUF', 1], ['<', 'SDA', 3]], ['=', 0]]
            ]]
        ,['StC0', [0, None], [  #State before Start condition(SCL:H, SDA:H)
            [[['==', 'StC0', 0], ['==', 'SCL', 3], ['==', 'SDA', 3]], ['=', 1]]
            ,[[['==', 'StC0', 1], ['<', 'SCL', 3]], ['=', 0]]
        ]]
        ,['St', [0, None], [ #Start condition
            [[['==', 'St', 0], ['==', 'SCL', 3], ['==', 'StC0', 1], ['==', 'SDA', 0]], ['=', 1]]
            ,[[['==', 'St', 1], ['==', 'SDA', 3]], ['=', 0]]
            ,[[['==', 'St', 1], ['==', 'SCL', 0]], ['=', 0]]
        ]]
        ,['SpC0', [0, None], [ #State before Stop condition(SCL:H, SDA:L)
            [[['==', 'SpC0', 0], ['==', 'SCL', 3], ['==', 'SDA', 0]], ['=', 1]]
            ,[[['==', 'SpC0', 1], ['<', 'SCL', 3]], ['=', 0]]
        ]]
        ,['tSU_STO', [0, None], [ #Stop condition setup time
            [[['==', 'wtSU_STO', 1], ['==', '!SDA', 1], ['>', 'SDA', 0]], ['-', '@', '@SpC0']]
        ]]
        ,['wtSU_STO', [0, None], [ #Waiting for Stop condition setup time
            [[['==', '!SpC0', 1], ['==', 'SpC0', 1]], ['=', 1]]
            ,[[['==', '!SpC0', 1], ['==', 'SpC0', 0]], ['=', 0]]
            ,[[['==', 'wtSU_STO', 1], ['==', '!SDA', 1], ['>', 'SDA', 0]], ['=', 0]]
        ]]
        ,['Sp', [0, None], [ #Stop condition
            [[['==', 'Sp', 0], ['==', 'SCL', 3], ['==', 'SpC0', 1], ['==', 'SDA', 3]], ['=', 1]]
            ,[[['==', 'Sp', 1], ['==', 'SDA', 0]], ['=', 0]]
            ,[[['==', 'Sp', 1], ['==', 'SCL', 0]], ['=', 0]]
        ]]
        ,['Read', [0, None], [ #Read
            [[['==', 'wDataBit', 2], ['<', 'SCL', 3], ['==', 'ByteCnt', 0], ['==', 'BitCnt', 1], ['==', 'SDA', 3]], ['=', 1]]
            ,[[['==', 'wDataBit', 1], ['<', 'SCL', 3], ['==', 'ByteCnt', 0], ['==', 'BitCnt', 1], ['==', 'SDA', 0]], ['=', 0]]
        ]]
        ,['Ack', [0, None], [ #Ack
            [[['==', 'wDataBit', 1], ['<', 'SCL', 3], ['==', 'BitCnt', 0], ['==', 'SDA', 0]], ['=', 1]]
            ,[[['==', 'wDataBit', 2], ['<', 'SCL', 3], ['==', 'BitCnt', 0], ['==', 'SDA', 3]], ['=', 0]]
        ]]
        ,['DataBit', [0, None], [ #Data bit
            [[['==', 'wDataBit', 1], ['<', 'SCL', 3], ['==', 'SDA', 0], ['==', '!Read', 0], ['==', '!Ack', 0]], ['=', 0]]
            ,[[['==', 'wDataBit', 2], ['<', 'SCL', 3] , ['==', 'SDA', 3], ['==', '!Read', 0], ['==', '!Ack', 0]], ['=', 1]]
        ]]
        ,['wDataBit', [0, None], [ #Waiting for Data bit
            [[['>', 'wDataBit', 0], ['<', 'SCL', 3]], ['=', 0]]
            ,[[['>', 'wDataBit', 0], ['==', '!Sp', 1]], ['=', 0]]
            ,[[['==', 'wDataBit', 0], ['==', '!tR_SCL', 1], ['==', 'SDA', 0]], ['=', 1]]
            ,[[['==', 'wDataBit', 0], ['==', '!tR_SCL', 1], ['==', 'SDA', 3]], ['=', 2]]
        ]]
        ,['ByteCnt', [0, None], [ #Byte number
            [[['==', '!St', 1], ['==', 'St', 0]], ['=', 0]]
            ,[[['==', '!tF_SCL', 1], ['==', 'BitCnt', 0]], ['+','ByteCnt', 1]]
        ]]
        ,['BitCnt', [0, None], [ #Bit number
            [[['==', '!St', 1], ['==', 'St', 0]], ['=', 8]]
            ,[[['==', '!tF_SCL', 1], ['==', 'BitCnt', 0]], ['=', 8]]
            ,[[['==', '!tF_SCL', 1], ['>', 'BitCnt', 0]], ['-', 'BitCnt', 1]]
        ]]
        ,['tSU_DAT_R', [0, None], [ #Data input setup time(slave input)(rise)
            [[['==', '1tSU_DAT_R', 1], ['==', 'dir_DAT', 0], ['==', '!SCL', 1], ['==', 'SCL', 0]], ['-', '@0tSU_DAT', '@1tSU_DAT_R']]
        ]]
        ,['tSU_DAT_MI_R', [0, None], [ #Data input setup time(master input)(rise)
            [[['==', '1tSU_DAT_R', 1], ['==', 'dir_DAT', 1], ['==', '!SCL', 1], ['==', 'SCL', 0]], ['-', '@0tSU_DAT', '@1tSU_DAT_R']]
        ]]
        ,['1tSU_DAT_R', [0, None], [ #Data input setup time(rise) SDA rise
            [[['==', '1tSU_DAT_R', 1], ['==', '!SCL', 1], ['==', 'SCL', 0]], ['=', 0]]
            ,[[['==', '1tSU_DAT_R', 1], ['==', '!SDA', 1], ['!=', 'SDA', 3]], ['=', 0]]
            ,[[['==', '1tSU_DAT_R', 1], ['==', 'St', 1]], ['=', 0]]
            ,[[['==', '1tSU_DAT_R', 0], ['==', '!SDA', 1], ['==', 'SDA', 3]], ['=', 1]]
        ]]
        ,['tSU_DAT_F', [0, None], [ #Data input setup time(slave input)(fall)
            [[['==', '1tSU_DAT_F', 1], ['==', 'dir_DAT', 0], ['==', '!SCL', 1], ['==', 'SCL', 0]], ['-', '@0tSU_DAT', '@1tSU_DAT_F']]
        ]]
        ,['tSU_DAT_MI_F', [0, None], [ #Data input setup time(master input)(fall)
            [[['==', '1tSU_DAT_F', 1], ['==', 'dir_DAT', 1], ['==', '!SCL', 1], ['==', 'SCL', 0]], ['-', '@0tSU_DAT', '@1tSU_DAT_F']]
        ]]
        ,['1tSU_DAT_F', [0, None], [ #Data input setup time(fall) SDA fall
            [[['==', '1tSU_DAT_F', 1], ['==', '!SCL', 1], ['==', 'SCL', 0]], ['=', 0]]
            ,[[['==', '1tSU_DAT_F', 1], ['==', '!SDA', 1], ['!=', 'SDA', 0]], ['=', 0]]
            ,[[['==', '1tSU_DAT_F', 0], ['==', '!SDA', 1], ['==', 'SDA', 0], ['!=', 'St', 1]], ['=', 1]]
        ]]
        ,['0tSU_DAT', [0, None], [ #Data input setup time's origin
            [[['==', '0tSU_DAT', 1], ['==', '!SCL', 1], ['==', 'SCL', 0]], ['=', 0]]
            ,[[['==', '0tSU_DAT', 0], ['==', '!SCL', 1], ['>', 'SCL', 0]], ['=', 1]]
        ]]
        ,['tHD_DAT_R', [0, None], [ #Data input hold time(slave input)(rise)
            [[['==', '1tHD_DAT_R', 2], ['==', 'dir_DAT_H', 0], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['-', '@1tHD_DAT_R', '@0tHD']]
        ]]
        ,['tHD_DAT_MI_R', [0, None], [ #Data input hold time(master input)(rise)
            [[['==', '1tHD_DAT_R', 2], ['==', 'dir_DAT_H', 1], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['-', '@1tHD_DAT_R', '@0tHD']]
        ]]
        ,['1tHD_DAT_R', [0, None], [ #Data input hold time(rise) SDA rise
            [[['>', '1tHD_DAT_R', 0], ['==', '!St', 1], ['==', 'St', 0]], ['=', 0]]
            ,[[['==', '!SCL', 1], ['==', 'SCL', 3], ['==', 'SDA', 0]], ['=', 1]]
            ,[[['>', '1tHD_DAT_R', 0], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['=', 0]]
            ,[[['==', '1tHD_DAT_R', 1], ['==', '!SDA', 1], ['>', 'SDA', 0]], ['=', 2]]
        ]]
        ,['tHD_DAT_F', [0, None], [ #Data input hold time(slave input)(fall)
            [[['==', '1tHD_DAT_F', 2], ['==', 'dir_DAT_H', 0], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['-', '@1tHD_DAT_F', '@0tHD']]
        ]]
        ,['tHD_DAT_MI_F', [0, None], [ #Data input hold time(master input)(fall)
            [[['==', '1tHD_DAT_F', 2], ['==', 'dir_DAT_H', 1], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['-', '@1tHD_DAT_F', '@0tHD']]
        ]]
        ,['1tHD_DAT_F', [0, None], [ #Data input hold time(fall) SDA fall
            [[['>', '1tHD_DAT_F', 0], ['==', '!St', 1], ['==', 'St', 0]], ['=', 0]]
            ,[[['==', '!SCL', 1], ['==', 'SCL', 3], ['==', 'SDA', 3]], ['=', 1]]
            ,[[['>', '1tHD_DAT_F', 0], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['=', 0]]
            ,[[['==', '1tHD_DAT_F', 1], ['==', '!SDA', 1], ['<', 'SDA', 3]], ['=', 2]]
        ]]
        ,['tAA_R', [0, None], [ #SDA Output valid from clock(rise)
            [[['==', '1tAA_R', 2], ['==', 'dir_DAT', 1], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['-', '@1tAA_R', '@0tHD']]
        ]]
        ,['1tAA_R', [0, None], [ #SDA Output valid from clock(rise) SDA rise
            [[['>', '1tAA_R', 0], ['==', '!St', 1], ['==', 'St', 0]], ['=', 0]]
            ,[[['==', '!SCL', 1], ['==', 'SCL', 3], ['==', 'SDA', 0]], ['=', 1]]
            ,[[['>', '1tAA_R', 0], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['=', 0]]
            ,[[['==', '1tAA_R', 1], ['==', '!SDA', 1], ['==', 'SDA', 3]], ['=', 2]]
        ]]
        ,['tAA_F', [0, None], [ #SDA Output valid from clock(fall)
            [[['==', '1tAA_F', 2], ['==', 'dir_DAT', 1], ['!=', 'BitCnt', 8], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['-', '@1tAA_F', '@0tHD']]
        ]]
        ,['1tAA_F', [0, None], [ #SDA Output valid from clock(fall) SDA fall
            [[['>', '1tAA_F', 0], ['==', '!St', 1], ['==', 'St', 0]], ['=', 0]]
            ,[[['==', '!SCL', 1], ['==', 'SCL', 3], ['==', 'SDA', 3]], ['=', 1]]
            ,[[['>', '1tAA_F', 0], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['=', 0]]
            ,[[['==', '1tAA_F', 1], ['==', '!SDA', 1], ['==', 'SDA', 0]], ['=', 2]]
        ]]
        ,['tDH_R', [0, None], [ #SDA output hold time(rise)
            [[['==', '1tDH_R', 2], ['==', 'dir_DAT_H', 1], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['-', '@1tDH_R', '@0tHD']]
        ]]
        ,['1tDH_R', [0, None], [ #SDA output hold time(rise) SDA rise
            [[['>', '1tDH_R', 0], ['==', '!St', 1], ['==', 'St', 0]], ['=', 0]]
            ,[[['==', '!SCL', 1], ['==', 'SCL', 3], ['==', 'SDA', 0]], ['=', 1]]
            ,[[['>', '1tDH_R', 0], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['=', 0]]
            ,[[['==', '1tDH_R', 1], ['==', '!SDA', 1], ['>', 'SDA', 0]], ['=', 2]]
        ]]
        ,['tDH_F', [0, None], [ #SDA output hold time(fall)
            [[['==', '1tDH_F', 2], ['==', 'dir_DAT_H', 1], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['-', '@1tDH_F', '@0tHD']]
        ]]
        ,['1tDH_F', [0, None], [ #SDA SDA output hold time(fall) SDA fall
            [[['>', '1tDH_F', 0], ['==', '!St', 1], ['==', 'St', 0]], ['=', 0]]
            ,[[['==', '!SCL', 1], ['==', 'SCL', 3], ['==', 'SDA', 3]], ['=', 1]]
            ,[[['>', '1tDH_F', 0], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['=', 0]]
            ,[[['==', '1tDH_F', 1], ['==', '!SDA', 1], ['<', 'SDA', 3]], ['=', 2]]
        ]]
        ,['0tHD', [0, None], [ #SDA output hold time's origin
            [[['==', '0tHD', 1], ['==', '!SCL', 1], ['==', 'SCL', 3]], ['=', 0]]
            ,[[['==', '0tHD', 0], ['==', '!SCL', 1], ['==', 'SCL', 0]], ['=', 1]]
        ]]
        ,['dir_DAT', [0, None], [ #data direction
            [[['==', '!BitCnt', 1], ['==', 'ByteCnt', 0], ['==', 'BitCnt', 0]], ['=', 1]]
            ,[[['==', '!BitCnt', 1], ['==', 'Read', 0], ['==', 'BitCnt', 0]], ['=', 1]]
            ,[[['==', '!BitCnt', 1], ['>', 'ByteCnt', 0], ['==', 'Read', 1], ['>', 'BitCnt', 0]], ['=', 1]]
            ,[[['==', '!BitCnt', 1]], ['=', 0]]
        ]]
        ,['dir_DAT_H', [0, None], [ #data direction for hold analysis
            [[['==', '!tR_SCL', 1]], ['=', 'dir_DAT']]
        ]]
        ]
    ]
    return tas

def DispSettings_I2C(
    ths     #閾値
    ,chn    #チャネル番号
):
    thSCL, thSDA = ths
    cSCL, cSDA = chn
    return [
         ['tSCL', 'tSCL: SCL period', [[cSCL, thSCL[0]], [cSCL, thSCL[0]]], ['min', 'max']]
        ,['tR_SCL', 'tR_SCL: SCL rise time', [[cSCL, thSCL[1]], [cSCL, thSCL[0]]], ['min', 'max']]
        ,['tF_SCL', 'tF_SCL: SCL fall time', [[cSCL, thSCL[0]], [cSCL, thSCL[1]]], ['min', 'max']]
        ,['tLOW', 'tLOW: SCL low time', [[cSCL, thSCL[0]], [cSCL, thSCL[0]]], ['min', 'max']]
        ,['tHIGH', 'tHIGH: SCL high time', [[cSCL, thSCL[1]], [cSCL, thSCL[1]]], ['min', 'max']]
        ,['tR_SDA', 'tR_SDA: SDA rise time', [[cSDA, thSDA[1]] , [cSDA, thSDA[0]]], ['min', 'max']]
        ,['tF_SDA', 'tF_SDA: SDA fall time', [[cSDA, thSDA[0]] , [cSDA, thSDA[1]]], ['min', 'max']]
        ,['tSU_STA', 'tSU_STA: Start condition setup time', [[cSDA, thSDA[1]], [cSCL, thSCL[1]]], ['all']]
        ,['tHD_STA', 'tHD_STA: Start condition hold time', [[cSCL, thSCL[1]], [cSDA, thSDA[0]]], ['all']]
        ,['tBUF', 'tBUF: Bus free time', [[cSDA, thSDA[1]], [cSDA, thSDA[1]]], ['all']]
        ,['tSU_STO', 'tSU_STO: Stop condition setup time', [[cSDA, thSDA[0]], [cSCL, thSCL[1]]], ['all']]
        ,['tSU_DAT_R', 'tSU_DAT_R: Data input setup time(rise)', [[cSCL, thSCL[0]], [cSDA,thSDA[1]]], ['all']]
        ,['tSU_DAT_F', 'tSU_DAT_F: Data input setup time(fall)', [[cSCL, thSCL[0]], [cSDA,thSDA[0]]], ['all']]
        ,['tHD_DAT_R', 'tHD_DAT_R: Data input hold time(rise)', [[cSDA, thSDA[0]], [cSCL, thSCL[0]]], ['all']]
        ,['tHD_DAT_F', 'tHD_DAT_F: Data input hold time(fall)', [[cSDA, thSDA[1]], [cSCL, thSCL[0]]], ['all']]
        ,['tSU_DAT_MI_R', 'tSU_DAT_MI_R: Data input setup time(master input)(rise)', [[cSCL, thSCL[0]], [cSDA,thSDA[1]]], ['all']]
        ,['tSU_DAT_MI_F', 'tSU_DAT_MI_F: Data input setup time(master input)(fall)', [[cSCL, thSCL[0]], [cSDA,thSDA[0]]], ['all']]
        ,['tHD_DAT_MI_R', 'tHD_DAT_MI_R: Data input hold time(master input)(rise)', [[cSDA, thSDA[0]], [cSCL, thSCL[0]]], ['all']]
        ,['tHD_DAT_MI_F', 'tHD_DAT_MI_F: Data input hold time(master input)(fall)', [[cSDA, thSDA[1]], [cSCL, thSCL[0]]], ['all']]
        ,['tAA_R', 'tAA_R: SDA Output valid from clock(rise)', [[cSDA, thSDA[1]], [cSCL, thSCL[0]]], ['all']]
        ,['tAA_F', 'tAA_F: SDA Output valid from clock(fall)', [[cSDA, thSDA[0]], [cSCL, thSCL[0]]], ['all']]
        ,['tDH_R', 'tDH_R: SDA output hold time(rise)', [[cSDA, thSDA[0]], [cSCL, thSCL[0]]], ['all']]
        ,['tDH_F', 'tDH_F: SDA output hold time(fall)', [[cSDA, thSDA[1]], [cSCL, thSCL[0]]], ['all']]
    ]

def StrSettings_I2C(
    chn    #チャネル番号
):
    cSCL, cSDA = chn
    return [
        ['St', 1, 'S', cSDA, 3.5]
        ,['Sp', 1, 'P', cSDA, 3.5]
        ,['Read', 1, 'R', cSDA, 3.5]
        ,['Read', 0, 'W', cSDA, 3.5]
        ,['Ack', 1, 'K', cSDA, 3.5]
        ,['Ack', 0, 'N', cSDA, 3.5]
        ,['DataBit', 1, '1', cSDA, 3.5]
        ,['DataBit', 0, '0', cSDA, 3.5]
    ]

class TASettings:
    def __init__(self, type, logicLevel, ths, chn):
        if type == 'SPI':
            self.tas = TASettings_SPI(ths, chn)
            self.disp = DispSettings_SPI(ths, chn)
            self.strs = StrSettings_SPI(chn)
        elif type == 'I2C':
            self.tas = TASettings_I2C(ths, chn)
            self.disp = DispSettings_I2C(ths, chn)
            self.strs = StrSettings_I2C(chn)
        self.hratios = [1, 2, 0.5]
        self.ylim = [[-logicLevel*0.3, logicLevel*1.52], [-logicLevel*0.2, logicLevel*1.2], [0, 1]]
        self.yticks = [[0, int(logicLevel)] for i in range(2)]
        self.lny = [[1.4, 0.7], [1.4, 0.4]]
        self.vly = 0.3
        self.vty = 0.0
        self.zipos = [(-50, 18), (-50, 1)]
        self.mainZoom = None
        self.figsize = (6.4, 4.8)
        self.dpi = 100
