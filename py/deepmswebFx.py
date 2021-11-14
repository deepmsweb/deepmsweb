import numpy as np


FILETYPES = set(['png', 'jpg', 'jpeg'])
ColorSet = [(1.0, 1.0, 0.0), (0.5, 1.0, 0.0),  (1.0, 0.0, 0.0),
            (0.0, 0.5, 1.0), (1, 1, 1)]

olcekMetin = {}
olcekMetin["DC"] = "DC is a criterion calculated according to the overlap amount of the region placed on the pre-selected regions"
olcekMetin["VOE"] = "The VOE metric shows the error rate between the expert opinion and the masked region"
olcekMetin["LTPR"] = "Lesion True Positive Rate"
olcekMetin["LFPR"] = "Lesion False Positive Rate"
def uzanti_kontrol(dosyaadi):
    return '.' in dosyaadi and \
        dosyaadi.rsplit('.', 1)[1].lower() in FILETYPES


def uzanti_kontrolJson(dosyaadi):
    return '.' in dosyaadi and \
        dosyaadi.rsplit('.', 1)[1].lower() in ['json']


def maskCompound(mArr):
    col = mArr.shape
    s = col[2]
    if s > 1:
        mArr1 = mArr[:, :, 0]
        i = 1
        while i < s:
            mArr2 = mArr[:, :, i]
            mArr1 = np.logical_or(mArr1, mArr2)
            i = i+1
        m = mArr1
        m2 = m[:, :, np.newaxis]

        return m2
    else:
        return mArr

def colorSetting(colorM, ColorSet):
    colors = []
    for i in range(len(colorM)):
        colors.append(ColorSet[int(colorM[i])])

    return colors
