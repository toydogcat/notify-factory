#!/bin/bash

# === 可自訂變數 ===
PROJECT_NAME="flutter_uiux"
SOURCE_FOLDER="flutter_code"
DATA_FOLDER="/workspaces/notify-factory/factory/data"

# === 自動推導路徑 ===
ROOT_DIR="/workspaces/notify-factory"
PROJECT_PATH="$ROOT_DIR/$PROJECT_NAME"
SOURCE_PATH="$ROOT_DIR/$SOURCE_FOLDER"
ASSETS_PATH="$PROJECT_PATH/assets"

# === 建立 Flutter 專案 ===
flutter create "$PROJECT_PATH"

# === 移除 flutter_uiux/.git ===
rm -rf "$PROJECT_PATH/.git"

# === 清空 flutter_uiux/lib/ ===
rm -rf "$PROJECT_PATH/lib"

# === 建立 lib 的軟連結 ===
ln -sfn "$SOURCE_PATH" "$PROJECT_PATH/lib"
ln -sfn "$DATA_FOLDER" "$ASSETS_PATH"

echo "✅ Flutter 專案 '$PROJECT_NAME' 已建立並連結到 '$SOURCE_FOLDER'"


