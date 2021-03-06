class Solution:
    def longestIncreasingSubsequence(self, nums):
        # write your code here
        dp = [1 for i in range(len(nums))]
        maxresult = 0
        for i in range(1, len(nums)):
            for j in range(0, i):
                if (nums[j] < nums[i]):
                    dp[i] = max(dp[i], dp[j] + 1)
            maxresult = max(dp[i], maxresult)
        return maxresult

s = Solution()
n=int(input())
nums=[int(i) for i in input().split()]
print(s.longestIncreasingSubsequence(nums))