"""
module for read_time function
"""

import math

time_dict = {'day': 86400,
            'hour': 3600,
            'minute': 60,
            'second' : 1}

def read_time(diff):
    # arg should be float - difference between two time objects (unix time difference)
    # returns time difference in readable string format, rounded to nearest second
    temp = {}
    for key, value in time_dict.items():
        n = math.floor(diff/value)
        if n == 1:
            temp[key] = n
            diff -= n*value
        if n > 1:
            temp[key + 's'] = n
            diff -= n*value
    return ', '.join((' '.join((str(item), key)) for key, item in temp.items()))


if __name__ == '__main__':

    pass
