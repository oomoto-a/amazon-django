class Const:
    # keepaAPIのステータス：未処理
    KEEPA_API_STATUS_INIT = "0"
    # keepaAPIのステータス：処理中
    KEEPA_API_STATUS_PROCESSING = "1"
    # keepaAPIのステータス：完了
    KEEPA_API_STATUS_COMPLETE = "9"
    # keepaAPIのステータス：除外ASIN (KEEEPA送信無し)
    KEEPA_API_STATUS_EXCLUSION = "3"
    # keepaAPIのステータス：除外WORD (KEEEPA送信有り)
    KEEPA_API_STATUS_EXCLUSION_WORD = "4"
    # keepaAPIのステータス：指定数オーバー
    KEEPA_API_STATUS_LIMIT_OVER = "5"
    # asinの登録上限:1万件
    ASIN_MAX_LIMIT = 10000

    # 表示用KEEPAステータス
    kEEPA_STATUS = {
        "0":"未処理",
        "1":"処理中",
        "3":"除外ASIN対象",
        "4":"除外ワード対象",
        "5":"累計数オーバー",
        "9":"完了",
    }

    # テーブルの1ページあたりのデフォルト件数
    PAGE_PER_DEFAULT = 10