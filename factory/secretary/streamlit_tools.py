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
    
    # 初始化 session state
    if "yaml_content" not in st.session_state:
        st.session_state.yaml_content = yaml_content
    if "editor_mode" not in st.session_state:
        st.session_state.editor_mode = "code"  # "code" 或 "text"

    # 模式切換按鈕
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💻 程式編輯器模式" if st.session_state.editor_mode == "text" else "📝 文字編輯器模式"):
            st.session_state.editor_mode = "text" if st.session_state.editor_mode == "code" else "code"
            st.rerun()
    
    with col2:
        if st.button("🔄 重新載入檔案"):
            try:
                with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                    st.session_state.yaml_content = f.read()
                st.success("檔案已重新載入！")
                st.rerun()
            except FileNotFoundError:
                st.session_state.yaml_content = "# 尚未建立設定檔"
                st.rerun()

    if st.session_state.editor_mode == "code":
        # 程式編輯器模式 - 只用來顯示和編輯（不儲存）
        st.subheader("程式編輯器 (語法高亮)")
        
        edited_result = code_editor(
            st.session_state.yaml_content,
            height=400,
            lang="yaml",
            theme="vs-dark",
            key="yaml_code_editor"
        )
        
        # 提供複製按鈕
        if st.button("📋 複製到文字編輯器"):
            if edited_result and edited_result.get("text"):
                st.session_state.yaml_content = edited_result["text"]
                st.session_state.editor_mode = "text"
                st.success("內容已複製到文字編輯器！")
                st.rerun()
            else:
                st.warning("編輯器內容為空或無法讀取")
        
        st.info("💡 提示：在程式編輯器中編輯後，點擊「複製到文字編輯器」按鈕來儲存內容")
    
    else:
        # 文字編輯器模式 - 可以儲存
        st.subheader("文字編輯器 (可儲存)")
        
        # 使用 text_area 進行編輯
        edited_content = st.text_area(
            "YAML 內容",
            value=st.session_state.yaml_content,
            height=400,
            key="yaml_text_editor"
        )
        
        # 即時更新 session state
        if edited_content != st.session_state.yaml_content:
            st.session_state.yaml_content = edited_content
        
        # 儲存和驗證按鈕
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 儲存設定"):
                try:
                    # 驗證 YAML 格式
                    yaml.safe_load(edited_content)
                    
                    # 儲存到檔案
                    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                        f.write(edited_content)
                    
                    st.success("設定已儲存！")
                    
                    # 重新載入 puppy 設定（如果有這個方法）
                    if hasattr(puppy, 'load_settings'):
                        puppy.load_settings()
                    
                except yaml.YAMLError as e:
                    st.error(f"YAML 格式錯誤：{e}")
                except Exception as e:
                    st.error(f"儲存失敗：{e}")
        
        with col2:
            if st.button("✅ 驗證 YAML"):
                try:
                    yaml.safe_load(edited_content)
                    st.success("YAML 格式正確！")
                except yaml.YAMLError as e:
                    st.error(f"YAML 格式錯誤：{e}")
        
        with col3:
            # 使用 HTML + JS 實現複製到剪貼簿
            copy_js = f"""
            <script>
            function copyToClipboard() {{
                navigator.clipboard.writeText(`{edited_content.replace('`', '\\`')}`).then(function() {{
                    alert('內容已複製到剪貼簿！');
                }}).catch(function(err) {{
                    console.error('複製失敗: ', err);
                }});
            }}
            </script>
            <button onclick="copyToClipboard()" style="
                background-color: #ff6b6b;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                cursor: pointer;
                font-size: 14px;
            ">📋 複製到剪貼簿</button>
            """
            st.html(copy_js)
    
    # 顯示內容預覽
    if st.checkbox("顯示內容預覽"):
        st.subheader("內容預覽")
        st.code(st.session_state.yaml_content[:500] + "..." if len(st.session_state.yaml_content) > 500 else st.session_state.yaml_content, language="yaml")
