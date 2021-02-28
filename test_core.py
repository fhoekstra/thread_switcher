from core import Core
import unittest


class TestCoreFriendlyNumber(unittest.TestCase):
    def test_no_hyperthreading_core_1(self):
        result = Core(total_num=12, index=0, hyper_threading=False)
        self.assertEqual(1, result.friendly_number)

    def test_no_hyperthreading_core_2(self):
        result = Core(total_num=12, index=1, hyper_threading=False)
        self.assertEqual(2, result.friendly_number)

    def test_ht_core_2(self):
        result = Core(total_num=12, index=1, hyper_threading=True)
        self.assertEqual(2, result.friendly_number)


class TestCoreThreads(unittest.TestCase):
    def test_threads_core1_no_ht(self):
        core = Core(total_num=4, index=0, hyper_threading=False)
        result = core.thread_indices
        self.assertSetEqual(set((0,)), set(result))

    def test_threads_core2_no_ht(self):
        core = Core(total_num=4, index=1, hyper_threading=False)
        result = core.thread_indices
        self.assertSetEqual(set((1,)), set(result))

    def test_threads_core1_with_ht(self):
        core = Core(total_num=4, index=0, hyper_threading=True)
        result = core.thread_indices
        self.assertSetEqual(set((0, 1)), set(result))

    def test_threads_core2_with_ht(self):
        core = Core(total_num=4, index=1, hyper_threading=True)
        result = core.thread_indices
        self.assertSetEqual(set((2, 3)), set(result))

    def test_threads_core4_with_ht(self):
        core = Core(total_num=4, index=3, hyper_threading=True)
        result = core.thread_indices
        self.assertSetEqual(set((6, 7)), set(result))


class TestAffinityMask(unittest.TestCase):
    def test_core1_no_ht(self):
        core = Core(total_num=4, index=0, hyper_threading=False)
        mask = core.affinity_mask
        self.assertEqual("1", mask)

    def test_core2_no_ht(self):
        core = Core(total_num=4, index=1, hyper_threading=False)
        mask = core.affinity_mask
        self.assertEqual("2", mask)

    def test_core32_no_ht(self):
        """ This is a workaround for a limitation of the PowerShell function I use """
        core = Core(total_num=32, index=31, hyper_threading=False)
        mask = core.affinity_mask
        self.assertEqual(str(2**30), mask)

    def test_core1_with_ht(self):
        expected = str(int("11", base=2))
        core = Core(total_num=4, index=0, hyper_threading=True)
        mask = core.affinity_mask
        self.assertEqual(expected, mask)

    def test_core2_with_ht(self):
        expected = str(int("1100", base=2))
        core = Core(total_num=4, index=1, hyper_threading=True)
        mask = core.affinity_mask
        self.assertEqual(expected, mask)

    def test_core16_with_ht(self):
        expected = str(2**30)
        core = Core(total_num=16, index=15, hyper_threading=True)
        mask = core.affinity_mask
        self.assertEqual(expected, mask)


if __name__ == '__main__':
    unittest.main()
