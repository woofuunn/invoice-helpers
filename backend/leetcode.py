from typing import List
import sys
import math

from app import index


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        maxsum = float("-inf")
        curnum = 0
        for num in nums[1:]:
            curnum = max(num, num + curnum)
            maxsum = max(maxsum, curnum)
        return maxsum

    def divide(self, dividend: int, divisor: int) -> int:
        is_positive_dividend = dividend > 0
        dividend = dividend if (dividend > 0) else -dividend
        is_positive_divisor = divisor > 0
        divisor = divisor if (divisor > 0) else -divisor

        dividend_str = str(dividend)
        dividend_index = len(str(dividend))
        divisor_index = len(str(divisor))
        if divisor_index > dividend_index: return 0
        res = ""
        index = 0

        while dividend_index >= divisor_index:
            cur = int(dividend_str[: divisor_index + index])

            count = 0
            while cur - divisor >= 0:
                cur -= divisor
                count += 1
            res += str(count)

            dividend_str = str(cur).zfill(divisor_index + index) + dividend_str[divisor_index + index:]
            index += 1
            dividend_index -= 1

        return (int(res)-1 if int(res)>2**31 else int(res)) \
            if ((not is_positive_dividend and not is_positive_divisor)
            or (is_positive_dividend and is_positive_divisor)) else -int(res)

    def divide_text(self, dividend: int, divisor: int) -> int:
        if divisor == 1: return dividend
        if dividend == -2**31 and divisor == -1: return 2**31-1


        sign = (dividend > 0 and divisor > 0) or (dividend < 0 and divisor < 0)

        dividend = dividend if dividend > 0 else -dividend
        divisor = divisor if divisor > 0 else -divisor

        ans=0
        while dividend >= divisor:
            temp = divisor
            count = 1
            while dividend >= (temp << 1):
                temp <<= 1
                count <<= 1
            dividend -= temp
            ans += count
        return ans if sign else -ans




s = Solution()
print(s.divide_text(64,4))

