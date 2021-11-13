#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
metrics

holds metric function definitions

Author: Jacob Reinhold (jacob.reinhold@jhu.edu)

Created on: Mar. 10, 2020
"""

__all__ = ['dice',
           'jaccard',
           'ppv',
           'tpr',
           'lfpr',
           'ltpr',
           'avd',
           'assd',
           'corr',
           'isbi15_score']

import numpy as np
from scipy.stats import pearsonr
from skimage.measure import label


def dice(pred, truth):
    """ dice coefficient between predicted and true binary masks """
    p, t = (pred > 0), (truth > 0)
    intersection = (p & t).sum()
    cardinality = p.sum() + t.sum()
    if cardinality == 0.: return np.nan
    return 2 * intersection / cardinality


def jaccard(pred, truth):
    """ jaccard index (IoU) between predicted and true binary masks """
    p, t = (pred > 0), (truth > 0)
    intersection = (p & t).sum()
    union = (p | t).sum()
    if union == 0.: return np.nan
    return intersection / union


def ppv(pred, truth):
    """ positive predictive value (precision) between predicted and true binary masks """
    p, t = (pred > 0), (truth > 0)
    intersection = (p & t).sum()
    denom = p.sum()
    if denom == 0.: return np.nan
    return intersection / denom


def tpr(pred, truth):
    """ true positive rate (sensitivity) between predicted and true binary masks """
    p, t = (pred > 0), (truth > 0)
    intersection = (p & t).sum()
    denom = t.sum()
    if denom == 0.: return np.nan
    return intersection / denom


def lfpr(pred, truth):
    """ lesion false positive rate between predicted and true binary masks """
    p, t = (pred > 0), (truth > 0)
    cc, n = label(p, return_num=True)
    if n == 0: return np.nan
    count = 0
    for i in range(1, n+1):
        if ((cc == i) & t).sum() == 0:
            count += 1
    return count / n


def ltpr(pred, truth):
    """ lesion true positive rate between predicted and true binary masks """
    p, t = (pred > 0), (truth > 0)
    cc, n = label(t, return_num=True)
    if n == 0: return np.nan
    count = 0
    for i in range(1, n+1):
        if ((cc == i) & p).sum() > 0:
            count += 1
    return count / n


def avd(pred, truth):
    """ absolute volume difference between predicted and true binary masks """
    p, t = (pred > 0), (truth > 0)
    numer = np.abs(p.sum() - t.sum())
    denom = t.sum()
    if denom == 0.: return np.nan
    return numer / denom


def assd(pred, truth):
    """ average symmetric surface difference between predicted and true binary masks """
    raise NotImplementedError


def corr(pred_vols, truth_vols):
    """ pearson correlation coefficient between list of predicted and true binary volumes """
    return pearsonr(pred_vols, truth_vols)[0]


def isbi15_score(pred, truth, reweighted=True):
    """
    report the score (minus volume correlation)
    for a given prediction as described in [1]

    reweighted flag puts the score (minus
    volume correlation) between 0 and 1

    References:
        [1] Carass, Aaron, et al. "Longitudinal multiple sclerosis
            lesion segmentation: resource and challenge." NeuroImage
            148 (2017): 77-102.
    """
    score = (dice(pred, truth) / 8 +
             ppv(pred, truth) / 8 +
             (1 - lfpr(pred, truth)) / 4 +
             ltpr(pred, truth) / 4)
    if reweighted:
        score *= (4 / 3)
    return score
