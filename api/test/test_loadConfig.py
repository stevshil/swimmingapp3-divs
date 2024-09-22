import pytest
import sys
sys.path.insert(0, './modules')
from fetch import *
def test_loadConfig_longitude():
    all_data=loadConfig()
    assert all_data["longitude"] == '1.1743'

def test_loadConfig_areaids():
    all_data=loadConfig()
    assert all_data["areaids"] == ['12567', '12568']