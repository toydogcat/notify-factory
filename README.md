# notify-factory
The notify factory for home use.

## env

```bash
bash environment/setup_demo_env.sh
```

# python part

## run 

```bash
cd factory/
uv run secretary/main_script.py
uv run streamlit run secretary/streamlit_app.py
```

# Bugs

* yaml 直接設定有問題

# flutter part

## env

```bash
# install
bash environment/flutter_install.sh

# Test hello world case
export PATH="$HOME/development/flutter/bin:$PATH"
flutter doctor
cd flutter_web_hello
flutter run -d web-server
```

## run

```bash
cd factory_ui

flutter build web
flutter build apk
flutter build appbundle

flutter build macos    # macOS
flutter build windows  # Windows
flutter build linux    # Linux

# tmp
flutter run -d chrome
flutter run -d linux

# run
flutter run -d web-server
```
