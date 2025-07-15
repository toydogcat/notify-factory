import streamlit as st
import json
from encryptor import Master
from main_script import Puppy

puppy = Puppy()
st.title("今日訊息編輯器")

with open("data/today.json", "r", encoding="utf-8") as f:
    data = json.load(f)

room = st.selectbox("選擇房間", list(data["rooms"].keys()))
source = st.selectbox("選擇來源", list(data["rooms"][room].keys()))
entries = data["rooms"][room][source]

for entry in entries:
    st.subheader(entry["title"])
    if entry.get("encrypted"):
        password = st.text_input("輸入密碼", type="password")
        if st.button("解密"):
            decrypted = puppy.master.decrypt_content(entry["content"])
            st.write(decrypted)
    else:
        st.write(entry["content"])
