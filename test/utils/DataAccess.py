import unittest
from datetime import datetime

from finance.test import FinanceTest
from finance.utils import DataAccess

class DataAccessTest(FinanceTest):

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(DataAccessTest('test_get_data'))
        suite.addTest(DataAccessTest('test_save_load_custom_name'))
        return suite

    def test_get_data(self):
        '''
        Tests the length the data frame
        Tets the number of columns and their names

        Note 1: File downloads are managed by finance.utils.FileManager
                Test for that on FileManagerTest.py
        Note 2: Other tests were done on the benchmark
        '''
        self.setUpDataAccess()

        start_date = datetime(2015, 1, 1)
        end_date = datetime(2017, 12, 31)

        # Single symbol, single field
        symbols = "AAPL"
        fields = 'close'
        df = self.data_access.get_data(symbols, start_date, end_date, fields)
        self.assertEqual(len(df), 755)
        self.assertEqual(len(df.columns), 1)
        names = [fields]
        self.assertEqual(list(df.columns), names)

        # Multiple symbols, single field
        symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
        fields = 'close'
        df = self.data_access.get_data(symbols, start_date, end_date, fields)
        self.assertEqual(len(df), 755)
        self.assertEqual(len(df.columns), 5)
        names = symbols
        self.assertEqual(list(df.columns), names)

        # Single symbol, multiple fields
        symbols = "AAPL"
        fields = ['close', 'volume']
        df = self.data_access.get_data(symbols, start_date, end_date, fields)
        self.assertEqual(len(df), 755)
        self.assertEqual(len(df.columns), 2)
        names = ['close', 'volume']
        self.assertEqual(list(df.columns), names)

        # Multiple symbol, multiple fields
        symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
        fields = ['close', 'volume']
        df = self.data_access.get_data(symbols, start_date, end_date, fields)
        self.assertEqual(len(df), 755)
        self.assertEqual(len(df.columns), 10)
        names = ['AAPL close', 'AAPL volume', 'GLD close', 'GLD volume', 'GOOG close',
                    'GOOG volume', 'SPY close', 'SPY volume', 'XOM close', 'XOM volume']
        self.assertEqual(list(df.columns), names)

    def test_save_load_custom_name(self):
        self.setUpDataAccess()

        symbols = ["AAPL", "GLD", "GOOG", "SPY", "XOM"]
        start_date = datetime(2015, 1, 1)
        end_date = datetime(2017, 12, 31)
        fields = 'close'
        
        close = self.data_access.get_data(symbols, start_date, end_date, fields, save=False)
        self.data_access.save(close, "customName", extension='.custom')

        close_loaded = self.data_access.load("customName", extension='.custom')

        self.assertEqual(list(close.columns), list(close_loaded.columns))
        self.assertEqual(len(close), len(close_loaded))


def benchmark():
    from time import clock, time
    da = DataAccess('./data')
    da.empty_dirs(delete=False)

    print ('Directory empty: Download and save 5 stocks')
    t1, t2 = clock(), time()
    symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2017, 12, 31)
    fields = 'close'
    da.get_data(symbols, start_date, end_date, fields)
    t1_f, t2_f = clock(), time()
    print ("   ", t1_f - t1, t2_f - t2)

    print ('Load 5 stocks from .csv')
    t1, t2 = clock(), time()
    symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2017, 12, 31)
    fields = 'close'
    da.get_data(symbols, start_date, end_date, fields, useCache=False)
    t1_f, t2_f = clock(), time()
    print ("   ", t1_f - t1, t2_f - t2)

    print ('Load 5 stocks from serialized')
    t1, t2 = clock(), time()
    symbols = ["AAPL","GLD","GOOG","SPY","XOM"]
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2017, 12, 31)
    fields = 'close'
    da.get_data(symbols, start_date, end_date, fields, useCache=True)
    t1_f, t2_f = clock(), time()
    print ("   ", t1_f - t1, t2_f - t2)

if __name__ == '__main__':
    suite = DataAccessTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    # benchmark()
    FinanceTest.delete_data()
