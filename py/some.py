import numpy as np


def compareM(masks1, masks2):
    if(masks1.shape[0] == masks2.shape[0] and masks1.shape[1] == masks2.shape[1]):
        message = ""
        ix = masks1.shape[2]
        iy = masks2.shape[2]

        bMatrix = np.zeros((ix, iy))
        i = 0
        r1 = []
        r2 = []
        for i in range(ix):
            mask1 = masks1[:, :, i]
            for t in range(iy):
                mask2 = masks2[:, :, t]
                mask1Norm = mask1 / np.sqrt(np.sum(mask1**2))
                mask2Norm = mask2 / np.sqrt(np.sum(mask2**2))
                simScore = np.sum(mask2Norm*mask1Norm)
                if(simScore > 0):
                    sScore = mask2.sum()/mask1.sum()
                    bMatrix[i, t] = sScore
                t = t+1
            i = i+1
    return bMatrix


ColorSet = [(1.0, 1.0, 0.0), (0.5, 1.0, 0.0),  (1.0, 0.0, 0.0),
            (0.0, 0.5, 1.0), (1, 1, 1)]


def colorSetting(colorM, ColorSet):
    colors = []
    for i in range(len(colorM)):
        colors.append(ColorSet[int(colorM[i])])

    return colors


def compareMessage(bMatrix, treshold):
    ix = bMatrix.shape[1]
    iy = bMatrix.shape[2]
    zN = np.zeros(iy).astype(int)+4
    zO = np.zeros(ix).astype(int)

    ratesR1 = np.zeros(ix)
    ratesR2 = np.zeros(iy)

    zNew = bMatrix.sum(axis=0)
    zOld = bMatrix.sum(axis=1)
    exC = zOld.size-np.count_nonzero(zOld)
    newC = zNew.size-np.count_nonzero(zNew)
    altesik = 1-treshold
    ustesik = 1+treshold

    message = {"message": "", "type": ""}

    messages = {}
    for i in range(ix):
        for t in range(iy):
            sScore = bMatrix[i, t]
            if (sScore > altesik and sScore < ustesik):
                likeC = likeC+1
                zN[t] = 3
                zO[i] = 3
                ratesR1[i] = 0
                ratesR2[t] = 0
            elif (sScore <= altesik):
                tinyC = tinyC+1
                zN[t] = 1
                zO[i] = 1
                rate = (1 - sScore)*100
                ratesR1[i] = rate
                ratesR2[t] = rate
                message = {
                    "message": " 1 plak  %{:.2f} küçülmüştür. ".format(rate), "type": "success"}
                messages = messages+{"kuculen"+tinyC: message}
            elif (sScore >= ustesik):
                bigC = bigC+1
                zN[t] = 2
                zO[i] = 2
                rate = (sScore - 1)*100
                ratesR1[i] = rate
                ratesR2[t] = rate
                # flash(" 1 plakda %{:.2f} büyüme gözlenmiştir. ".format(rate), "danger")

    for i in range(ix):
        if (zOld[i] == 0):
            ratesR1[i] = 0
    for i in range(iy):
        if (zNew[i] == 0):
            ratesR2[i] = 0

    if(likeC == 0 and bigC == 0 and tinyC == 0):
        message = {
            "message": "değerlendirme için yeterli benzerlik bulunamadı. ", "type": "info"}
        messages = messages+{"benzemiyor": message}
       # flash("değerlendirme için yeterli benzerlik bulunamadı. ", "info")
    elif(likeC == iy and likeC == ix):
        message = "lezyonlarda değişim olmamıştır."
        message = {
            "message": "lezyonlarda değişim olmamıştır. ", "type": "success"}
        messages = {"hicDegismemis": message}
       # flash("lezyonlarda değişim olmamıştır.", "success")
    else:
        if(likeC > 0):
            message = {
                "message": "{} plakda değişim olmamıştır.".format(likeC), "type": "info"}
            messages = messages+{"toplamBenzer": message}
        #    flash("{} plakda değişim olmamıştır.".format(likeC), "info")
        if(tinyC > 0):
            message = {
                "message": " {} plak küçülmüştür.".format(tinyC), "type": "info"}
            messages = messages+{"toplamKücülen": message}
        if(bigC > 0):
            message = {
                "message": " {} plakda büyüme gözlenmiştir.".format(bigC), "type": "info"}
            messages = messages+{"toplamBüyüyen": message}
        if(exC > 0):
            message = {
                "message": " {: .0f} plak gözlenmemiştir.".format(exC), "type": "warning"}
            messages = messages+{"toplamYokolan": message}
        if(newC > 0):

            message = {
                "message":  " {: .0f} yeni plak tespit edilmiştir.".format(newC), "type": "light"}
            messages = messages+{"toplamYeni": message}

    colorsR2 = colorSetting(zN, ColorSet)
    colorsR1 = colorSetting(zO, ColorSet)
    return
