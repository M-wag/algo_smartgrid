import unittest
import os
import .test

class TestExporter(unittest.TestCase):
    def __init__(self):
        output_params = {
            'cwd' : self.get_parent_path(2),
            'algorithm' : 'hillclimber',
            'wijk_num' : '2',
            'iterations' : 100,
            'reset_thresh_hc' : 25,
            'temperature' : 9999,
            'file_name' : 'unittest',
            'path_method' : 'straight'
        }
        exporter = Exporter(output_params)

    """Test destination directory"""

    """Test destination"""


    def get_parent_path(self, levels):
        path = os.path.abspath(__file__)
        for i in range(levels + 1):
            path = os.path.dirname(path)
        return path + '/'

if __name__ == '__main__':
    unittest.main()
