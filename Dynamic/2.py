# 击鼓传花
def drinkingGame():
    n = 3  # 人数
    m = 3  # 次数
    dp = [[0] * (m + 1) for _ in range(n)]
    dp[0][0] = 1
    dp[n - 1][1] = 1
    dp[1][1] = 1
    for j in range(1, m + 1): #每多传递一次，链条肯定就不一样了啊，这个题的推进点是把左右的种类加起来就是自己的种类数
        for i in range(n):
            if i == 0:
                dp[0][j] = dp[1][j - 1] + dp[n - 1][j - 1]
            if i == n - 1:
                dp[n - 1][j] = dp[n - 2][j - 1] + dp[0][j - 1]
            else:
                dp[i][j] = dp[i][j] + dp[i + 1][j - 1]
    print(dp[0][m])


drinkingGame()
