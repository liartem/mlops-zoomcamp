import pandas as pd
from train import make_label_encoding
from pandas.testing import assert_frame_equal


def test_make_label_encoding():
    '''
    Makes the unit test for the function "make_label_encoding"
    returns None if the expected result is equivalent to the actual result,
    returns difference otherwise
    '''
    row = pd.DataFrame({"Gender": "Male", "Age": 20, "AnnualSalary": 1000}, index=[0])
    actual_result = make_label_encoding(row)
    
    expected_result = pd.DataFrame({"Gender": 0, "Age": 20, "AnnualSalary": 1000}, index=[0])
    assertion = assert_frame_equal(actual_result,  expected_result)
    assert None is assertion

