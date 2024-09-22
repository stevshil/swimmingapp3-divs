import pytest
import sys
import os
import time
from fetch import *

@pytest.fixture(scope="session")
def theFile():
    filename="testfile"
    thefile=open(filename,"w")
    thefile.write("abc")
    thefile.close()
    yield thefile
    os.remove(filename)

@pytest.fixture(scope="session")
def badFile():
    filename="badfile"
    thefile=open(filename,"w")
    thefile.write("abc")
    thefile.close()
    os.utime(filename,(os.stat(filename)[8]-720000,os.stat(filename)[8]-720000))
    yield thefile
    os.remove(filename)

def test_checkFileState_hour_ok(theFile):
    filename="testfile"
    freq=1
    assert checkFileState(filename,freq) == "OK"

def test_checkFileState_day_ok(theFile):
    filename="testfile"
    freq=24
    assert checkFileState(filename,freq) == "OK"

def test_checkFileState_hour_nok(badFile):
    filename="badfile"
    freq=1
    assert checkFileState(filename,freq) == "UPDATE"

def test_checkFileState_day_nok(badFile):
    filename="badfile"
    freq=24
    assert checkFileState(filename,freq) == "UPDATE"