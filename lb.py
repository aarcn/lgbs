import sys
import time
from random import uniform


def loading_bar(total, prefix='', suffix='', length=50, fill='█'):
    for bar in range(total + 1):
        percent = f"{100 * (bar / total):.1f}"
        fill_length = int(length * bar // total)
        bar = fill * fill_length + '-' * (length - fill_length)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
        sys.stdout.flush()
        time.sleep(uniform(0.0, 0.06))  # how long u wanna stall
    sys.stdout.write("\n")
