# 背包问题
weight = [2, 2, 6, 5, 4]
value = [6, 3, 5, 4, 6]
dp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(0, 5):
    print(dp)
    j = 10
    while j >= weight[i]:
        dp[j] = max(dp[j], dp[j - weight[i]] + value[i])
        j -= 1
print(dp)

# for(i=1; i<=n; i++)
#     for(j=w[i]; j<=v; j++)
#         dp[j]=max(dp[j],dp[j-w[i]]+h[i]);
