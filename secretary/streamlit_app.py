import json
import yaml
import streamlit as st
from main_script import Puppy
from code_editor import code_editor

puppy = Puppy()
SETTINGS_PATH = "configs/settings.yaml"

def show_entry(entry):
    if "summary" in entry:
        st.subheader(entry["summary"])
    else:
        st.subheader(entry["title"])

    if entry.get("encrypted"):
        _password = st.text_input("輸入密碼", type="password")
        if st.button("解密"):
            if _password:
                decrypted = puppy.master.decrypt_content_by_key(
                    entry["content"], 
                    _password
                )
            else:
                decrypted = puppy.master.decrypt_content(
                    entry["content"]
                )
            st.write(decrypted)
    else:
        if "content" in entry:
            st.write(entry["content"])
        else:
            st.write(entry["temperature"])


def show_yaml_editor():
    st.header("設定編輯器")

    # 每次進入都重新讀取 YAML
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            yaml_content = f.read()
    except FileNotFoundError:
        yaml_content = "# 尚未建立設定檔"

    # 顯示 YAML 編輯器
    # edited_content = code_editor(
    #     yaml_content,
    #     lang="yaml",
    #     height=400,
    #     theme="vs-dark",  # 可選：vs-light, vs-dark, etc.
    #     key="yaml_editor"
    # )
    # edited_content = st.text_area("編輯 YAML 設定", yaml_content, height=400)

    
    # 直接將設定展開傳入
    edited_result = code_editor(
        yaml_content,
        height=400,
        lang="yaml",       # 語言設定直接放這
        theme="vs-dark",       # 主題也放這
        key="yaml_editor"
    )

    # st.code(edited_result["text"], language="yaml")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 儲存設定"):
            # try:
            #     yaml_text = edited_content.get("text", "")
            #     yaml.safe_load(yaml_text)  # 驗證 YAML 格式
            #     with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            #         f.write(yaml_text)
            #     st.success("設定已儲存！")
            # except yaml.YAMLError as e:
            #     st.error(f"YAML 格式錯誤：{e}")

            try:
                yaml.safe_load(yaml_content)  # 驗證 YAML 格式
                with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                    f.write(yaml_content)
                st.success("設定已儲存！")
            except yaml.YAMLError as e:
                st.error(f"YAML 格式錯誤：{e}")
    with col2:
        if st.button("🔄 重新載入"):
            st.write("重新載入中...")
            st.rerun()


def main_my():
    st.title("今日訊息編輯器")

    today_path   = puppy.paths.TODAY_DATA_PATH
    week_path    = puppy.paths.WEEK_DATA_PATH
    archive_path = puppy.paths.ARCHIVE_DATA_PATH

    with open(today_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    room = st.sidebar.selectbox("選擇房間", list(puppy.settings.keys()))

    source = st.selectbox("選擇來源", list(data["rooms"][room].keys()))
    entries = data["rooms"][room][source]

    for entry in entries:
        show_entry(entry)


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

    # # 每次進入都重新讀取 YAML
    # try:
    #     with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
    #         yaml_content = f.read()
    # except FileNotFoundError:
    #     yaml_content = "# 尚未建立設定檔"

    # # 顯示 YAML 編輯器
    # edited_content = code_editor(
    #     yaml_content,
    #     lang="yaml",
    #     height=400,
    #     theme="vs-dark",  # 可選：vs-light, vs-dark, etc.
    #     key="yaml_editor"
    # )
    # breakpoint()




