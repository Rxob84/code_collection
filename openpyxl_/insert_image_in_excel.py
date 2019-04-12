"""
2019/04/12

 @HirotakaK

https://qiita.com/HirotakaK/items/a42e3e94273247199b9a
"""

import openpyxl as px
from openpyxl.drawing.image import Image

# 実行用にexcelファイルを用意
wb = px.Workbook()
ws = wb.active

img = Image("test.png")
img2 = Image("sample.jpg")  # jpgはうまくいかない？

ws.add_image(img, "A1")
ws.add_image(img2, "I1")

wb.save("test_insert_image_in_excel.xlsx")