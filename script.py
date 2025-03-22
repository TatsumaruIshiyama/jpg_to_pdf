import streamlit as st
from PIL import Image, ImageOps
import io

# --- セッション状態の初期化（初回のみ実行） ---
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
    st.session_state.file_name = "converted"
    st.session_state.file_uploader_key = 0  # ← リセット用のキー
    st.session_state.pdf_bytes = None  # PDFデータをキャッシュ

st.title("JPG → PDF 変換アプリ")

# --- ファイルアップロード（キーを変更してリセット可能に） ---
uploaded_files = st.file_uploader("PDFにしたいJPG画像をアップロードしてください（複数可）", 
                                  type=["jpg", "jpeg"], 
                                  accept_multiple_files=True, 
                                  key=st.session_state.file_uploader_key)

# 新しいファイルがアップロードされた場合のみセッションに保存
if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.session_state.pdf_bytes = None  # 新しい画像をアップロードしたらPDFを再生成する必要あり

# --- アップロードされた画像の表示 ---
if st.session_state.uploaded_files:
    st.write("アップロードされた画像")
    images = []
    for uploaded_file in st.session_state.uploaded_files:
        img = Image.open(uploaded_file)
        img = ImageOps.exif_transpose(img)  # ← ここでExif情報を考慮して正しい向きに変換！
        img = img.convert("RGB")  # PDF用にRGB変換
        images.append(img)
        st.image(img, caption=uploaded_file.name, use_container_width=True)

    # PDFのファイル名入力
    file_name = st.text_input("保存するPDFのファイル名", st.session_state.file_name)

    # --- PDF変換（再実行を最小限にするため、キャッシュする） ---
    if st.button("PDFに変換してダウンロード"):
        if images and st.session_state.pdf_bytes is None:
            pdf_bytes = io.BytesIO()
            images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes.seek(0)
            st.session_state.pdf_bytes = pdf_bytes  # PDFをセッションに保存（キャッシュ）

    # --- ダウンロードボタン（PDFが生成されている場合のみ表示） ---
    if st.session_state.pdf_bytes:
        st.download_button(label="📥 PDFをダウンロード", 
                           data=st.session_state.pdf_bytes, 
                           file_name=f"{file_name}.pdf", 
                           mime="application/pdf")

    # --- リセットボタン（file_uploaderをクリア） ---
    if st.button("リセット"):
        st.session_state.uploaded_files = []
        st.session_state.file_name = "converted"
        st.session_state.pdf_bytes = None  # PDFデータもリセット
        st.session_state.file_uploader_key += 1  # ← key を変更して file_uploader をクリア
        st.rerun()
