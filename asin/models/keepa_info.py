from django.db import models
from datetime import datetime


# keepa取得情報
class KeepaInfo(models.Model):
    account_id = models.CharField(max_length=30,verbose_name="アカウントID", null=False) 
    asin_group_id = models.CharField(max_length=100, verbose_name="asinグループID", null=False)
    asin = models.CharField(max_length=10, default="", verbose_name="ASIN")

    lowest_price =  models.IntegerField(verbose_name="最安値_価格")
    lowest_shipping =  models.IntegerField(verbose_name="最安値_送料")
    lowest_price_fbm =  models.IntegerField(verbose_name="最安値_価格_FBM")
    lowest_shipping_fbm =  models.IntegerField(verbose_name="最安値_送料_FBM")
    lowest_history_fbm =  models.TextField(verbose_name="最安値_履歴_FBM")
    lowest_price_fba =  models.IntegerField(verbose_name="最安値_価格_FBA")
    lowest_history_fba =  models.TextField(verbose_name="最安値_履歴_FBA")
    buy_box_price =  models.IntegerField(verbose_name="カート価格")
    buy_box_shipping =  models.IntegerField(verbose_name="カート価格_送料")
    buy_box_history =  models.TextField(verbose_name="カート価格_履歴")
    count_new =  models.IntegerField(verbose_name="出品者数")
    count_new_history =  models.TextField(verbose_name="出品者数_履歴")
    top_category_id = models.CharField(max_length=11, verbose_name="最上位：カテゴリID")
    top_category_name = models.TextField(verbose_name="最上位：カテゴリ名")
    sub_category_id = models.CharField(max_length=11, verbose_name="最下位：カテゴリID")
    sub_category_name = models.TextField(verbose_name="最下位：カテゴリ名")
    sub_category_rank = models.CharField(max_length=11, verbose_name="最下位：ランキング")
    product_group = models.TextField(verbose_name="商品グループ")
    title = models.TextField(verbose_name="商品名")
    manufacturer = models.TextField(verbose_name="メーカー名")
    model = models.TextField(verbose_name="メーカー型番")
    brand = models.TextField(verbose_name="ブランド名")
    imagesCSV = models.TextField(verbose_name="画像CSV")
    image = models.CharField(max_length=20, verbose_name="画像")
    packageWeight = models.IntegerField(verbose_name="商品重量")
    packageHeight = models.IntegerField(verbose_name="サイズ（高さ）")
    packageLength = models.IntegerField(verbose_name="サイズ（長さ）")
    packageWidth = models.IntegerField(verbose_name="サイズ（幅）")
    releaseDate = models.CharField(max_length=8, verbose_name="発売日")
    list_price = models.IntegerField(verbose_name="定価")
    is_adult_product = models.BooleanField(verbose_name="アダルトフラグ")
    variations = models.TextField(verbose_name="バリエーション情報")
    new_price_history = models.TextField(verbose_name="新品_価格_履歴")
    used_price_history = models.TextField(verbose_name="中古_価格_履歴")
    create_date = models.DateTimeField(default=datetime.now, verbose_name="登録日")

    def __str__(self):
        return self.asin+self.title
