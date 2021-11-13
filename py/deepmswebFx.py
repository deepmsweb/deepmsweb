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


def compareMasks(r1, r2):
    masks1 = r1['masks']
    masks2 = r2['masks']
    return compareM(masks1, masks2)


def compareM(masks1, masks2):
    messagesX = {}
    if(masks1.shape[0] == masks2.shape[0] and masks1.shape[1] == masks2.shape[1]):

        ix = masks1.shape[2]
        iy = masks2.shape[2]
        zN = np.zeros(iy).astype(int)+4
        zO = np.zeros(ix).astype(int)
        ratesR1 = np.zeros(ix)
        ratesR2 = np.zeros(iy)
        cMatrix = np.zeros((ix, iy))
        bMatrix = np.zeros((ix, iy))
        likeC = 0
        tinyC = 0
        bigC = 0
        i = 0

        for i in range(ix):
            mask1 = masks1[:, :, i]
            for t in range(iy):
                mask2 = masks2[:, :, t]
                mask1Norm = mask1 / np.sqrt(np.sum(mask1**2))
                mask2Norm = mask2 / np.sqrt(np.sum(mask2**2))
                simScore = np.sum(mask2Norm*mask1Norm)
                if(simScore > 0):
                    bMatrix[i, t] = mask2.sum()/mask1.sum()
                    if (bMatrix[i, t] > 0.98 and bMatrix[i, t] < 1.02):
                        likeC = likeC+1
                        zN[t] = 3
                        zO[i] = 3
                        ratesR1[i] = 0
                        ratesR2[t] = 0
                    elif (bMatrix[i, t] <= 0.98):
                        tinyC = tinyC+1
                        zN[t] = 1
                        zO[i] = 1
                        rate = (1 - bMatrix[i, t])*100
                        ratesR1[i] = rate
                        ratesR2[t] = rate
                        messagesX["kuculmus"+str(tinyC)] = {
                            "message": "1 plaque is %{: .2f} smaller than before. ".format(rate), "type": "success"}
                        # flash(" 1 plak  %{:.2f} küçülmüştür. ".format(rate), "success")
                    elif (bMatrix[i, t] >= 1.02):
                        bigC = bigC+1
                        zN[t] = 2
                        zO[i] = 2
                        rate = (bMatrix[i, t] - 1)*100
                        ratesR1[i] = rate
                        ratesR2[t] = rate
                        messagesX["buyumus"+str(bigC)] = {
                            "message": " 1 plaque is %{:.2f} larger than before.".format(rate), "type": "danger"}
                        # flash(" 1 plakda %{:.2f} büyüme gözlenmiştir. ".format(rate), "danger")

                cMatrix[i, t] = simScore
                t = t+1
            i = i+1

        print(zO)
        print(zN)

        colorsR2 = colorSetting(zN, ColorSet)
        colorsR1 = colorSetting(zO, ColorSet)

        zNew = bMatrix.sum(axis=0)
        # print("zNew")
        # print(zNew)

        zOld = bMatrix.sum(axis=1)
        # print("zOld")
        # print(zOld)

        exC = zOld.size-np.count_nonzero(zOld)
        newC = zNew.size-np.count_nonzero(zNew)

        for i in range(ix):
            if (zOld[i] == 0):
                ratesR1[i] = 0
        for i in range(iy):
            if (zNew[i] == 0):
                ratesR2[i] = 0

        if(likeC == 0 and bigC == 0 and tinyC == 0):
            messagesX["notEvulate"] = {
                "message": "Not enough similarity found for evaluation.", "type": "info"}
           # flash("değerlendirme için yeterli benzerlik bulunamadı. ", "info")
        elif(likeC == iy and likeC == ix):
            messagesX["degismemis"] = {
                "message": "There is no change in the plaque(s).", "type": "success"}
           # flash("lezyonlarda değişim olmamıştır.", "success")
        else:
            if(likeC > 0):
                messagesX["benzerSayisi"] = {
                    "message": "There was no change in {:.0f} plaque(s).".format(likeC), "type": "info"}
            #    flash("{:.0f} plakda değişim olmamıştır.".format(likeC), "info")
            if(tinyC > 0):
                #message = " {:.0f} plak küçülmüştür.".format(tinyC)
                messagesX["kuculensayisi"] = {
                    "message": " {:.0f} plaque(s) smaller than before.".format(tinyC), "type": "success"}
            if(bigC > 0):
              #  message = message +  " {:.0f} plakda büyüme gözlenmiştir.".format(bigC)
                messagesX["buyuyenSayisi"] = {
                    "message": " {:.0f} plaque(s) bigger than before.".format(bigC), "type": "danger"}

            if(exC > 0):
               # message = message + \  " {: .0f} plak gözlenmemiştir.".format(exC)
                messagesX["yokOlan"] = {
                    "message": " {: .0f} plaque(s) not observed".format(exC), "type": "warning"}
             #   flash(" {: .0f} plak gözlenmemiştir.".format(exC), "warning")
            if(newC > 0):
               # message = message + \                    " {: .0f} yeni plak tespit edilmiştir.".format(newC)
                messagesX["yeniler"] = {
                    "message": " {: .0f} new plaque(s) detected.".format(newC), "type": "light"}
             #   flash(" {: .0f} yeni plak tespit edilmiştir.".format(newC), "light")

    else:
        #message = "mismatched size was detected."
        messagesX["yokOlan"] = {
            "message": "mismatched size was detected.", "type": "danger"}
        #flash("uyumsuz boyut", "danger")
        zN = zO = 0

    return messagesX, colorsR1, colorsR2, ratesR1, ratesR2, zO, zN


def colorSetting(colorM, ColorSet):
    colors = []
    for i in range(len(colorM)):
        colors.append(ColorSet[int(colorM[i])])

    return colors
