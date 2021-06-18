# import heapq
# a = [1,6,2,3,4,5,7]
# print(heapq.nlargest(3,a))
#最长上升子列
nums = [1,0,0,1,1]
nums = [8,9,1,2,3,4]
# dp = [1 for i in range(len(nums))]
# maxresult = 0
# for i in range(1, len(nums)):
#     for j in range(0, i):
#         if (nums[j] <= nums[i]):
#             dp[i] = max(dp[i], dp[j] + 1)
#     maxresult = max(dp[i], maxresult)
# print(maxresult)

nums = [8,9,1,2,3,4]
def findLengthOfLCIS(nums):
    ans = 0
    anchor = 0
    for i in range(len(nums)):
        if i and nums[i] <= nums[i - 1]:
            anchor = i
        ans = max(ans, i - anchor + 1)
    print(ans)
findLengthOfLCIS(nums)
