import matplotlib.pyplot as plt

from tsp.generator import Tsp

def visualize(tsp: Tsp, tour_list: list[int]):
    assert tsp.size == len(tour_list)

    x, y = [], []
    for a,b in tsp.positions:
        x.append(a)
        y.append(b)

    pre = tsp.positions[tour_list[0]]
    for idx in tour_list[1:]:
        a,b = tsp.positions[idx]
        plt.plot([pre[0], a], [pre[1], b], c="b", lw = 1)
        pre = [a,b]
    # 最後に0に戻る
    a,b = tsp.positions[0]
    plt.plot([pre[0], a], [pre[1], b], c="b", lw = 1)

    plt.scatter(x, y, s = 5, c = "k")
    plt.xlim(tsp.min_x, tsp.max_x)
    plt.ylim(tsp.min_y, tsp.max_y)

    plt.savefig("fig.png")
    plt.show()
