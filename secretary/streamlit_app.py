import json
import streamlit as st
from main_script import Puppy
from streamlit_tools import *

puppy = Puppy()


def main():
    st.title("今日訊息編輯器")
    menu = st.sidebar.radio("功能選單", ["訊息", "設定"])

    if menu == "設定":
        show_yaml_editor()
    else:
        today_path   = puppy.paths.TODAY_DATA_PATH
        with open(today_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        room = st.sidebar.selectbox("選擇房間", list(puppy.settings.keys()))
        source = st.selectbox("選擇來源", list(data["rooms"][room].keys()))
        entries = data["rooms"][room][source]

        for entry in entries:
            show_entry(entry)


if __name__ == '__main__':
    main()


