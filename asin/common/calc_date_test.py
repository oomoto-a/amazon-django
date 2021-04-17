from asin.common import calc_date
from datetime import datetime

def test_calc_range1():
    # 同日
    # 登録日：20151231　固定
    # 1: 1日前　20170131　20170227（today）　20170228
    relative_date = datetime(2015, 12, 31)
    today = datetime(2017, 2, 27)
    dates = calc_date.calc_range(relative_date, today)

    start = dates[0]
    end = dates[1]
    assert start.strftime("%Y%m%d") == "20170131"
    assert end.strftime("%Y%m%d") == "20170228"

    # 2: 同日 　20170228　20170228（today）　20170331
    relative_date = datetime(2015, 12, 31)
    today = datetime(2017, 2, 28)
    dates = calc_date.calc_range(relative_date, today)

    start = dates[0]
    end = dates[1]
    assert start.strftime("%Y%m%d") == "20170228"
    assert end.strftime("%Y%m%d") == "20170331"

    # 3: 1日後　20170228　20170301（today）　20170331
    relative_date = datetime(2015, 12, 31)
    today = datetime(2017, 3, 1)
    dates = calc_date.calc_range(relative_date, today)

    start = dates[0]
    end = dates[1]
    assert start.strftime("%Y%m%d") == "20170228"
    assert end.strftime("%Y%m%d") == "20170331"

def test_calc_range2():
    # 年またぎ
    # 登録日：20151201　固定
    # 1 : 年前 20161201  20161201(today)  20170101
    relative_date = datetime(2015, 12, 1)
    today = datetime(2016, 12, 1)
    dates = calc_date.calc_range(relative_date, today)

    start = dates[0]
    end = dates[1]
    assert start.strftime("%Y%m%d") == "20161201"
    assert end.strftime("%Y%m%d") == "20170101"

    # 2 : 年またぎ 20161201  20161231(today)  20170101
    relative_date = datetime(2015, 12, 1)
    today = datetime(2016, 12, 31)
    dates = calc_date.calc_range(relative_date, today)

    start = dates[0]
    end = dates[1]
    assert start.strftime("%Y%m%d") == "20161201"
    assert end.strftime("%Y%m%d") == "20170101"


    # 3 : 年またぎ 20170101  20170101(today)  20170201
    relative_date = datetime(2015, 12, 1)
    today = datetime(2017, 1, 1)
    dates = calc_date.calc_range(relative_date, today)

    start = dates[0]
    end = dates[1]
    assert start.strftime("%Y%m%d") == "20170101"
    assert end.strftime("%Y%m%d") == "20170201"

    # 4 : 年後 20170101  20170102(today)  20170201
    relative_date = datetime(2015, 12, 1)
    today = datetime(2017, 1, 2)
    dates = calc_date.calc_range(relative_date, today)

    start = dates[0]
    end = dates[1]
    assert start.strftime("%Y%m%d") == "20170101"
    assert end.strftime("%Y%m%d") == "20170201"

def test_calc_range3():
    # うるう年
    # 登録日：20151231　固定
    # 1 : 年前 20200131  20200205(today)  20200229
    relative_date = datetime(2015, 12, 31)
    today = datetime(2020, 2, 5)
    dates = calc_date.calc_range(relative_date, today)

    start = dates[0]
    end = dates[1]
    assert start.strftime("%Y%m%d") == "20200131"
    assert end.strftime("%Y%m%d") == "20200229"
