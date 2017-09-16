import unittest

from system.CPUCheck import CPUCheck


class CPUCheckTestCase(unittest.TestCase):
    def test_something(self):
        cpu_check = CPUCheck().totalCpu()
        self.assertIsNotNone(cpu_check, "Check is performed")


if __name__ == '__main__':
    unittest.main()
