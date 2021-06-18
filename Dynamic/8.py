n,m=[int(i) for i in input().split()]
seqs=input()
l=[int(i) for i in list(seqs)]
def longestIncreasingSubsequence(nums):
    # write your code here
    dp = [1 for i in range(len(nums))]
    maxresult = 0
    for i in range(1, len(nums)):
        for j in range(0, i):
            if (nums[j] <= nums[i]):
                dp[i] = max(dp[i], dp[j] + 1)
        maxresult = max(dp[i], maxresult)
    return maxresult
for i in range(m):
    g=[i for i in input().split()]
    if len(g)>1:
        g=list(g)
        s=int(g[1])
        e=int(g[2])
        for j in range(s-1,e):
            if l[j]==0:
                l[j]=1
            else:
                l[j]=0

    if g[0]=='q':
        print(longestIncreasingSubsequence(l))