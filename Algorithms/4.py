from typing import List, Tuple

class EventScheduler:
    def __init__(self):
        pass

    def maxValue(self, events: List[List[int]], k: int) -> int:
        events.sort(key=lambda x: x[1])
        n = len(events)
        dp = [[0] * (k + 1) for _ in range(n + 1)]
        ends = [event[1] for event in events]

        for i in range(1, n + 1):
            start, end, value = events[i - 1]
            j = 0
            for m in range(i - 1, -1, -1):
                if events[m][1] < start:
                    j = m + 1
                    break

            for t in range(1, k + 1):
                if dp[i - 1][t] > dp[j][t - 1] + value:
                    dp[i][t] = dp[i - 1][t]
                else:
                    dp[i][t] = dp[j][t - 1] + value

        return dp[n][k]


scheduler = EventScheduler()
inp = input().split("= ")
events = eval(inp[1][:-4])
k = eval(inp[2])
print(scheduler.maxValue(events, k))
