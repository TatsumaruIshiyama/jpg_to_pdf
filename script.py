# %%
from PIL import Image
import os

# %%
# 画像が保存されているフォルダのパス
image_folder = r"C:\Users\tatsu\OneDrive\画像\anime\kanokari"
output_pdf = "output.pdf"

# 画像ファイルのリストを取得（拡張子がjpgのもの）
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(".jpg")])

# 画像を開く
image_list = [Image.open(os.path.join(image_folder, f)).convert("RGB") for f in image_files]

# 先頭の画像を基準にしてPDFを作成
if image_list:
    image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])

print(f"PDFが作成されました: {output_pdf}")

'test'