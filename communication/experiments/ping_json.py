import re
import json

reference_string = '''
 172.27.0.1 
172.27.0.1 : [0], 64 bytes, 0.094 ms (0.094 avg, 0% loss)
172.27.0.0 : [0], 64 bytes, 23.3 ms (23.3 avg, 0% loss)
172.27.0.1 : [1], 64 bytes, 0.076 ms (0.085 avg, 0% loss)
172.27.0.2 : [0], timed out (NaN avg, 100% loss)
172.27.0.3 : [0], timed out (NaN avg, 100% loss)
172.27.0.0 : [1], 64 bytes, 38.3 ms (30.8 avg, 0% loss)
172.27.0.4 : [0], timed out (NaN avg, 100% loss)
172.27.0.5 : [0], timed out (NaN avg, 100% loss)
172.27.0.0 : [2], 64 bytes, 8.84 ms (23.5 avg, 0% loss)
172.27.0.1 : [2], 64 bytes, 0.080 ms (0.083 avg, 0% loss)
172.27.0.2 : [1], timed out (NaN avg, 100% loss)
172.27.0.3 : [1], timed out (NaN avg, 100% loss)
172.27.0.4 : [1], timed out (NaN avg, 100% loss)
172.27.0.5 : [1], timed out (NaN avg, 100% loss)
172.27.0.0 : [3], 64 bytes, 4.94 ms (18.9 avg, 0% loss)
172.27.0.1 : [3], 64 bytes, 0.074 ms (0.081 avg, 0% loss)
172.27.0.2 : [2], timed out (NaN avg, 100% loss)
172.27.0.3 : [2], timed out (NaN avg, 100% loss)
172.27.0.4 : [2], timed out (NaN avg, 100% loss)
172.27.0.5 : [2], timed out (NaN avg, 100% loss)
172.27.0.0 : [4], 64 bytes, 5.15 ms (16.1 avg, 0% loss)
172.27.0.1 : [4], 64 bytes, 0.075 ms (0.080 avg, 0% loss)
172.27.0.2 : [3], timed out (NaN avg, 100% loss)
172.27.0.3 : [3], timed out (NaN avg, 100% loss)
172.27.0.4 : [3], timed out (NaN avg, 100% loss)
172.27.0.5 : [3], timed out (NaN avg, 100% loss)
172.27.0.0 : [5], 64 bytes, 5.01 ms (14.3 avg, 0% loss)
172.27.0.1 : [5], 64 bytes, 0.074 ms (0.079 avg, 0% loss)
172.27.0.2 : [4], timed out (NaN avg, 100% loss)
172.27.0.3 : [4], timed out (NaN avg, 100% loss)
172.27.0.4 : [4], timed out (NaN avg, 100% loss)
172.27.0.5 : [4], timed out (NaN avg, 100% loss)
172.27.0.1 : [6], 64 bytes, 0.078 ms (0.079 avg, 0% loss)
172.27.0.2 : [5], timed out (NaN avg, 100% loss)
172.27.0.3 : [5], timed out (NaN avg, 100% loss)
172.27.0.0 : [6], 64 bytes, 33.4 ms (17.0 avg, 0% loss)
172.27.0.4 : [5], timed out (NaN avg, 100% loss)
172.27.0.5 : [5], timed out (NaN avg, 100% loss)
172.27.0.0 : [7], 64 bytes, 5.14 ms (15.5 avg, 0% loss)
172.27.0.1 : [7], 64 bytes, 0.071 ms (0.078 avg, 0% loss)
172.27.0.2 : [6], timed out (NaN avg, 100% loss)
172.27.0.3 : [6], timed out (NaN avg, 100% loss)
172.27.0.4 : [6], timed out (NaN avg, 100% loss)
172.27.0.5 : [6], timed out (NaN avg, 100% loss)
172.27.0.0 : [8], 64 bytes, 6.40 ms (14.5 avg, 0% loss)
172.27.0.1 : [8], 64 bytes, 0.066 ms (0.076 avg, 0% loss)
172.27.0.2 : [7], timed out (NaN avg, 100% loss)
172.27.0.3 : [7], timed out (NaN avg, 100% loss)
172.27.0.4 : [7], timed out (NaN avg, 100% loss)
172.27.0.5 : [7], timed out (NaN avg, 100% loss)
172.27.0.1 : [9], 64 bytes, 0.077 ms (0.076 avg, 0% loss)
172.27.0.2 : [8], timed out (NaN avg, 100% loss)
172.27.0.3 : [8], timed out (NaN avg, 100% loss)
172.27.0.0 : [9], 64 bytes, 38.3 ms (16.9 avg, 0% loss)
172.27.0.4 : [8], timed out (NaN avg, 100% loss)
172.27.0.5 : [8], timed out (NaN avg, 100% loss)
172.27.0.2 : [9], timed out (NaN avg, 100% loss)
172.27.0.3 : [9], timed out (NaN avg, 100% loss)
172.27.0.4 : [9], timed out (NaN avg, 100% loss)
172.27.0.5 : [9], timed out (NaN avg, 100% loss)
'''

data = reference_string.split("\n")

print(data)