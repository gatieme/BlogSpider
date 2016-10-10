#!/usr/bin/env python
# encoding: utf-8



import time

if __name__ == "__main__" :
    count = 0
    while True :
        count += 1
        print str(count)
        print """Given an array S of n integers, are there elements a, b, c, and d in S such that a + b + c + d = target? Find all unique quadruplets in the array which gives the sum of target.

        Note:
            Elements in a quadruplet (a,b,c,d) must be in non-descending order. (ie, a ≤ b ≤ c ≤ d)
            The solution set must not contain duplicate quadruplets.
            For example, given array S = {1 0 -1 0 -2 2}, and target = 0.

            A solution set is:
                (-1, 0, 0, 1)
                (-2, -1, 1, 2)
                (-2, 0, 0, 2)"""
        time.sleep(1)
