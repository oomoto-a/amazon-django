from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta


def calc_range(register_date:datetime, today):
    # 計算用に本日の時間を切り捨てる
    today = datetime(today.year, today.month, today.day,tzinfo=today.tzinfo)
    # 計算用に登録日の時間を切り捨てる
    register_date_cal = datetime(register_date.year, register_date.month, 
                        register_date.day,tzinfo=register_date.tzinfo)
    # 先月
    last_month = today - relativedelta(months=1)
    # 翌月
    next_month = today + relativedelta(months=1)
    # 結果・開始
    result_start = None
    # 結果・終了
    result_end = None
    # チェック用の日付
    check_date = None

    try:
        check_date = register_date_cal.replace(year=int(datetime.strftime(today, '%Y')) 
                                            ,month=int(datetime.strftime(today, '%m')))
    except ValueError as e:
        # 2/31のような場合エラー
        check_date = (today + relativedelta(months=1)).replace(day=1) - timedelta(days=1)

    if today < check_date:
        try:
            result_start = register_date_cal.replace(year=int(datetime.strftime(last_month, '%Y')) 
                                                ,month=int(datetime.strftime(last_month, '%m')))
        except ValueError as e:
            result_start = (last_month + relativedelta(months=1)).replace(day=1) - timedelta(days=1)

        result_end = check_date

    else:
        result_start = check_date
        try:
            result_end = register_date_cal.replace(year=int(datetime.strftime(next_month, '%Y')) 
                                                ,month=int(datetime.strftime(next_month, '%m')))
        except ValueError as e:
            result_end = (next_month + relativedelta(months=1)).replace(day=1) - timedelta(days=1)

    return [result_start, result_end]