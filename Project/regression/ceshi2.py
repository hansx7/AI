import string
import numpy as np

def number_of_the_day(y, m, d):
	days_in_a_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	days = 0
	if y == 2012:
		days += 365
		days_in_a_month[1] = 29
	for mm in range(0, m-1):
		days += days_in_a_month[mm]
	days += d
	return days

print number_of_the_day(2011, 12, 25)