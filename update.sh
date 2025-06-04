#!/bin/bash

# 检查并克隆或更新仓库脚本
# 作者：智能助手
# 日期：2025-06-04

# 定义仓库URL
REPO_URL="https://github.com/ddz16/TSFpaper"
TARGET_DIR="src"

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo "目标目录 $TARGET_DIR 不存在，开始克隆仓库..."
    
    # 克隆仓库
    git clone "$REPO_URL" "$TARGET_DIR"
    
    # 检查克隆是否成功
    if [ $? -ne 0 ]; then
        echo "错误：克隆仓库失败！"
        exit 1
    fi
    
    echo "仓库克隆成功！"
else
    echo "目标目录 $TARGET_DIR 已存在，尝试更新..."
    
    # 进入目录并拉取更新
    cd "$TARGET_DIR"
    
    # 检查git pull是否成功
    if ! git pull; then
        echo "警告：拉取更新失败，尝试清理后重试..."
        
        # 尝试重置本地修改
        git reset --hard HEAD
        git clean -fd
        
        # 再次尝试拉取
        if ! git pull; then
            echo "错误：无法拉取更新！"
            exit 2
        fi
    fi
    
    echo "仓库更新成功！"
    cd ..
fi

# 检查downloader.py是否存在
if [ ! -f "downloader.py" ]; then
    echo "错误：当前目录中未找到 downloader.py 文件！"
    exit 3
fi

# 执行Python下载器
echo "开始执行下载器..."
python downloader.py

# 检查Python执行结果
if [ $? -ne 0 ]; then
    echo "错误：执行下载器失败！"
    exit 4
fi

echo "所有操作完成！"
exit 0