import matplotlib.pyplot as plt
import random
import time
import math
import copy
from lib import *

random.seed(0) #seed値固定

n = 400

MIN_X = -1000
MAX_X = 1000

MIN_Y = -1000
MAX_Y = 1000

# ユークリッド距離を計算する
def CalcDist(x1, y1, x2, y2):
    d2 = (x1-x2)**2 + (y1-y2)**2
    return pow(d2, 0.5)

def CalcDist2(idx1, idx2):
    x1, y1 = xy[idx1]
    x2, y2 = xy[idx2]
    d2 = (x1-x2)**2 + (y1-y2)**2
    return pow(d2, 0.5)

# 都市を生成
def init():
    xy = []
    xy.append([0, 0]) # 0番目は必ず(0,0)
    while len(xy) < n:
        rand_x = random.randint(MIN_X, MAX_X)
        rand_y = random.randint(MIN_Y, MAX_Y)

        min_dist = 10**9
        for x, y in xy: min_dist = min(min_dist, CalcDist(rand_x, rand_y, x, y))
        if min_dist <= 10: continue # 近すぎるなら再生成

        xy.append([rand_x, rand_y])
    
    return xy

# 図を生成
def figure(lis = []):
    x, y = [], []
    for a,b in xy:
        x.append(a)
        y.append(b)
    if lis:
        pre = xy[lis[0]]
        for idx in lis[1:]:
            a,b = xy[idx]
            plt.plot([pre[0], a], [pre[1], b], c="b", lw = 1)
            pre = [a,b]
        # 最後に0に戻る
        a,b = xy[0]
        plt.plot([pre[0], a], [pre[1], b], c="b", lw = 1)


    plt.scatter(0, 0, s = 10, c = "r")
    plt.scatter(x, y, s = 5, c = "k")
    plt.xlim(MIN_X, MAX_X)
    plt.ylim(MIN_Y, MAX_Y)

    plt.savefig("fig.png")
    plt.show()

# 訪れた場所順のリストから合計距離を計算
def CalcLength(tourList):
    ret = 0
    now = xy[tourList[0]]
    for idx in tourList[1:]:
        x,y = xy[idx]
        ret += CalcDist(*now, x, y)
        now = [x,y]
    # 最後に0に戻る
    ret += CalcDist(*now, 0, 0)
    return ret

def Greedy(xy):
    tourList = []
    now = 0
    tourList.append(0) # 最初は0番目にいる
    use = [0]*n
    use[0] = 1

    while 1:
        lis = []
        for j,[x,y] in enumerate(xy):
            if use[j]: continue
            lis.append([j, CalcDist(*xy[now], x,y)])
        lis.sort(key= lambda val : val[1])
        if len(lis) == 0: break
        use[lis[0][0]] = 1
        now = lis[0][0]
        tourList.append(now)
    return tourList

def Greedy2(xy):

    distLis = []
    l = len(xy)

    for i in range(l-1):
        x1,y1 = xy[i]
        for j in range(i+1, l):
            x2,y2 = xy[j]
            d = CalcDist(x1,y1,x2,y2)
            distLis.append([d, i, j])

    distLis.sort(key= lambda val : val[0])
    G = [[] for i in range(l)]
    edgeNum = 0
    uf = UnionFind(l)
    for _,u,v in distLis:
        if len(G[u]) == 2: continue
        if len(G[v]) == 2: continue
        if edgeNum < l-1:
            if uf.same(u,v): continue

        G[u].append(v)
        G[v].append(u)

        uf.union(u,v)
        edgeNum += 1
    
    tourList = []
    now = 0
    reach = [0]*l
    reach[0] = 1
    tourList.append(now)
    for i in range(l-1):
        for to in G[now]:
            if reach[to] == 1: continue
            reach[now] = 1
            now = to
            tourList.append(now)
    return tourList

def Swap(idx1, idx2):
    x, y = idx1 + 1, idx2
    while x < y:
        tourList[x],tourList[y] = tourList[y], tourList[x]
        x += 1
        y -= 1

def TwoOptSub(idx1, idx2):
    if idx1 == idx2 : return
    if idx2 < idx1: idx1, idx2 = idx2, idx1

    l = len(tourList)
    distPre = CalcDist2(tourList[idx1], tourList[idx1+1]) + CalcDist2(tourList[idx2], tourList[(idx2+1)%l])
    distAft = CalcDist2(tourList[idx1], tourList[idx2]) + CalcDist2(tourList[idx1+1], tourList[(idx2+1)%l])

    if distAft < distPre: # TODO:高速化したい
        Swap(idx1, idx2)
        return True
    return False

def TwoOpt():
    flg = 1
    l = len(tourList)
    while flg:
        flg = 0
        for i in range(1, l-1):
            for j in range(i+1, l):
                flg |= TwoOptSub(i, j)
    return


bestAns = float("Inf")
bestTourList = []
def Memory(value, lis):
    global bestAns, bestTourList
    if value < bestAns:
        bestTourList = copy.deepcopy(lis)
        bestAns = value

def AnnealingOptimize(T=100, cool=0.999):
    global bestAns
    
    random.seed() # シード値を固定していたので初期化しておく
    l = len(tourList)

    cost = CalcLength(tourList)
    c = 0
    ite = 0

    while time.time() - tStart < 20:
        idx1 = random.randint(0, l-1)
        idx2 = random.randint(0, l-1)
        if idx1 > idx2: idx1, idx2 = idx2, idx1
        if idx1 == idx2: continue

        # コスト計算
        distPre = CalcDist2(tourList[idx1], tourList[idx1+1])\
             + CalcDist2(tourList[idx2], tourList[(idx2+1)%l])
        distAft = CalcDist2(tourList[idx1], tourList[idx2])\
             + CalcDist2(tourList[idx1+1], tourList[(idx2+1)%l])

         # 温度から確率を定義する。
        newCost = cost - distPre + distAft
        p = pow(math.e, -abs(distPre - distAft) / T)

        # 変更後のコストが小さければ採用する。
        # コストが大きい場合は確率的に採用する。
        if distAft < distPre or random.random() < p:
            Swap(idx1, idx2)
            #cost = CalcLength(tourList)
            cost = newCost
            #print(p, cost, bestAns)
            if distAft > distPre:
                #print(p, cost, bestAns)
                pass
            c += 1

            # 現在の最良の解よりよければ保存する
            Memory(cost, tourList)
        ite += 1

        # 温度を下げる
        T = T * cool
    print("count", c, ite)

xy = init()

tStart = time.time()

#tourList = Greedy(xy)
tourList = Greedy2(xy)

Memory(CalcLength(tourList), tourList)

print(CalcLength(bestTourList))

#TwoOpt()
#Memory(CalcLength(tourList), tourList)

AnnealingOptimize()

#TwoOpt()
#Memory(CalcLength(tourList), tourList)

print(CalcLength(bestTourList))
figure(bestTourList)

