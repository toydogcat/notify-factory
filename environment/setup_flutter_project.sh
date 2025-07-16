#!/bin/bash

# === 可自訂變數 ===
FACTORY="/workspaces/notify-factory"
PROJECT_NAME="flutter_uiux"
SOURCE_FOLDER="$FACTORY/flutter_project/flutter_code"
PUBSPEC_SOURCE="$FACTORY/flutter_project/pubspec.yaml"
DATA_FOLDER="$FACTORY/factory/data"

# === 自動推導路徑 ===
PROJECT_PATH="$FACTORY/$PROJECT_NAME"
ASSETS_PATH="$PROJECT_PATH/assets"

# === 建立 Flutter 專案 ===
flutter create "$PROJECT_PATH"

# === 移除 flutter_uiux/.git ===
rm -rf "$PROJECT_PATH/.git"

# === 清空 flutter_uiux/lib/ ===
rm -rf "$PROJECT_PATH/lib"

# === 建立 lib 的軟連結 ===
ln -sfn "$SOURCE_FOLDER" "$PROJECT_PATH/lib"

# === 移除 flutter_uiux/pubspec.yaml 並建立軟連結 ===
rm -f "$PROJECT_PATH/pubspec.yaml"
ln -sfn "$PUBSPEC_SOURCE" "$PROJECT_PATH/pubspec.yaml"

# === 建立 assets 的軟連結 ===
# mkdir -p "$ASSETS_PATH"
ln -sfn "$DATA_FOLDER" "$ASSETS_PATH"

# === 執行 flutter pub get ===
cd "$PROJECT_PATH"
flutter pub get

echo "✅ Flutter 專案 '$PROJECT_NAME' 已建立並連結到 '$SOURCE_FOLDER'"

