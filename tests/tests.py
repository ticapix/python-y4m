#!/usr/bin/env python

import sys
import y4m
import zipfile
import unittest
import os

file = 'akiyo_qcif.y4m'
sample = os.path.join(os.path.dirname(__file__), file)
sample_num_frames = 300


class TestReader(unittest.TestCase):

    def test_read_simple(self):
        self.cpt = 0

        def process_frame(frame):
            self.cpt += 1
        parser = y4m.Reader(process_frame, verbose=False)
        with zfd.open(file, 'r') as f:
            parser.decode(f.read())
        self.assertEqual(self.cpt, sample_num_frames)

    def test_read_simple_1k(self):
        self.cpt = 0

        def process_frame(frame):
            self.cpt += 1
        parser = y4m.Reader(process_frame, verbose=False)
        with zfd.open(file, 'r') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                parser.decode(data)
        self.assertEqual(self.cpt, sample_num_frames)


class TestLoop(unittest.TestCase):

    def test_loop_simple(self):
        def process_frame(frame):
            generator.encode(frame)
        parser = y4m.Reader(process_frame, verbose=False)
        generator = y4m.Writer(open(os.devnull, 'wb'))
        with zfd.open(file, 'r') as f:
            parser.decode(f.read())


if __name__ == '__main__':
    print(sys.version)
    zfd = zipfile.ZipFile(sample + '.zip')

    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(TestReader))
    suites.append(unittest.TestLoader().loadTestsFromTestCase(TestLoop))
    suite = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(suite)
