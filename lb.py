import sys
import time
from random import uniform


def print_loading_bar(total, prefix='', suffix='', length=50, fill='█'):
    for single_loading_bar in range(total + 1):
        percent = f"{100 * (single_loading_bar / total):.1f}"
        filled_length = int(length * single_loading_bar // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
        sys.stdout.flush()
        time.sleep(uniform(0.0, 0.06))
    sys.stdout.write("\n")
