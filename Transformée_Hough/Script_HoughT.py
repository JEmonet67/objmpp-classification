#!/home/jerome/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:28:08 2019

Script permettant de tester un grand nombre de
combinaison des 3 paramètres (résolution, paramètre 2
et min distance) de l'algorithme de transformée de
Hough

@author: jerome
"""

from HoughTransform import Hough_transform
import decimal

i=0

int_reso = 1
Par2=0
P=20
mindist=220

while int_reso<28 and Par2<220:
    for int_reso in range(13,41,4):
        resolution = decimal.Decimal('0.1')*int_reso
        for Par2 in range(P,P+40,10):
            i+=1
            print(f"Image n°{i} mindist=220 dp={resolution} Par2={Par2}")
            name=f"Img{i}_mindist_220_dp_{resolution}_P2_{Par2}.png"
            try:
                Hough_transform(resolution, Par2, 220, name)
            except:
                print(f"Echec image n°{i} mindist=220 Par2={Par2} dp={resolution}")
                i-=1
                continue
        P+=40

