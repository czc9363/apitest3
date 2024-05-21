import os
import unittest
from datetime import datetime
from BeautifulReport import BeautifulReport

DIR = os.path.dirname(os.path.abspath(__file__))
Environ = 'offline'


if __name__ == '__main__':
    run_pattern = 'all'

    if run_pattern == 'all':
        pattern = 'test*.py'
    elif run_pattern == 'smoking':
        pattern = 'test_major*.py'
    else:
        run_pattern = run_pattern + '.py'
    str_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    suite = unittest.TestLoader().discover('./testCase', 'test*.py')
    result = BeautifulReport(suite)
    result.report(filename=f"report_{run_pattern}_{str_time}.html", description="report", report_dir='./')
