import sys
import re
import pandas as pd
import numpy as np
sys.path.append('../lib')
import ntzreg

#####################
# 同じグループの縦セルをつまんでいくコードのためのインデックス作成
###
# play_anchor_index
# 処理開始のアンカーとなる配列の作成
# セルを縦につまむ際のトリガーになるインデックスをdf["番号"]から導き出す。
def pickcell(df_column, option= "s"):
    # anchor_index = df_column
    play_anchor_index = []
    for i, num in enumerate(df_column):
        if pd.isnull(num):
            continue
        else:
            play_anchor_index.append(i)
    
    ###
    # pause_anchor_index
    # 処理ここまでと合図するアンカーの配列の作成
    if "s" in option:
        # startはインデックス番号、pauseは最初から何番目を割り出したいときはこちら。
        pause_anchor_index = [n for n in play_anchor_index[1:]]
        pause_anchor_index.append(len(df_column))
    else:
        # start, pauseのインデックス番号をきっちりと割り出したいときはこちら。
        pause_anchor_index = [n - 1 for n in play_anchor_index[1:]]
        pause_anchor_index.append(len(df_column) - 1)

    ###
    # anchor_index
    anchor_index = []
    for play, pause in zip(play_anchor_index, pause_anchor_index):
        anchor_index.append([play, pause])
    
    return anchor_index



def tumamu(df_column, refer_column):
    categories = np.unique(refer_column, return_index=True)
    c_start = list(np.unique(categories[1]))
    c_puase = c_start[1:] + [len(df_column)]

    slice_scape = []
    for start, pause in zip(c_start, c_puase):
        slice_scape.append([start, pause])

    tmp_arr = [np.nan] * len(df_column)
    for scope in slice_scape:
        tmp_arr[scope[0]] = "、".join(df_column[scope[0]: scope[1]])

    return tmp_arr