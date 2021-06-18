# 剪绳子
def div(l):
    best_son = [0, 1, 2]
    tmp = []
    for i in range(3, l + 1):
        for j in range(1, i):
            tmp.append(i)
            x = best_son[j] * best_son[i - j]
            tmp.append(x)
        best_son.append(max(tmp))
        tmp = []
    return best_son[l]


print(div(8))
