@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

REM ========================================================
REM 自动更新仓库并运行下载器脚本
REM 修复中文乱码版本
REM ========================================================

set REPO_URL=https://github.com/ddz16/TSFpaper
set TARGET_DIR=src
set DOWNLOADER=downloader.py

echo.
echo [INFO] 开始执行脚本...
echo.

REM 检查目标目录是否存在
if exist "%TARGET_DIR%" (
    echo [INFO] 目标目录 %TARGET_DIR% 已存在，尝试更新...
    cd "%TARGET_DIR%"
    
    REM 尝试拉取更新
    git pull
    if !errorlevel! neq 0 (
        echo [WARN] 拉取更新失败，尝试清理后重试...
        git reset --hard HEAD
        git clean -fd
        git pull
        if !errorlevel! neq 0 (
            echo [ERROR] 无法拉取更新！
            exit /b 2
        )
    )
    cd ..
    echo [INFO] 仓库更新成功！
) else (
    echo [INFO] 目标目录 %TARGET_DIR% 不存在，开始克隆仓库...
    git clone "%REPO_URL%" "%TARGET_DIR%"
    if !errorlevel! neq 0 (
        echo [ERROR] 克隆仓库失败！
        exit /b 1
    )
    echo [INFO] 仓库克隆成功！
)

REM 检查下载器脚本是否存在
if not exist "%DOWNLOADER%" (
    echo [ERROR] 当前目录中未找到 %DOWNLOADER% 文件！
    exit /b 3
)

REM 执行Python下载器
echo [INFO] 开始执行下载器...
python "%DOWNLOADER%"
if !errorlevel! neq 0 (
    echo [ERROR] 执行下载器失败！
    exit /b 4
)

echo.
echo [INFO] 所有操作完成！
pause
exit /b 0