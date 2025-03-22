import streamlit as st
from PIL import Image
import io

# セッション状態を初期化（初回実行時）
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
    st.session_state.file_name = "変換後ファイル名"
    st.session_state.file_uploader_key = 0  # ← リセット用のキー

st.title("JPG → PDF 変換アプリ")

# ファイルアップロード（キーを変更することでリセット可能に！）
uploaded_files = st.file_uploader("PDFにしたいJPG画像をアップロードしてください（複数可）", 
                                  type=["jpg", "jpeg"], 
                                  accept_multiple_files=True, 
                                  key=st.session_state.file_uploader_key)

# アップロード内容をセッションに保存
if uploaded_files:
    st.session_state.uploaded_files = uploaded_files

# アップロードされた画像の表示
if st.session_state.uploaded_files:
    st.write("アップロードされた画像")
    images = []
    for uploaded_file in st.session_state.uploaded_files:
        img = Image.open(uploaded_file).convert("RGB")
        images.append(img)
        st.image(img, caption=uploaded_file.name, use_column_width=True)

    # PDFのファイル名入力
    file_name = st.text_input("保存するPDFのファイル名", st.session_state.file_name)

    # PDF変換 & ダウンロード
    if st.button("PDFに変換"):
        if images:
            # PDFをメモリ上に保存
            pdf_bytes = io.BytesIO()
            images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes.seek(0)

            # ダウンロードボタン
            st.download_button(label="📥 PDFをダウンロード", 
                               data=pdf_bytes, 
                               file_name=f"{file_name}.pdf", 
                               mime="application/pdf")

    # リセットボタン
    if st.button("リセット"):
        st.session_state.uploaded_files = []
        st.session_state.file_name = "converted"
        st.session_state.file_uploader_key += 1  # ← key を変更するとfile_uploaderがリセットされる！
        st.rerun()
