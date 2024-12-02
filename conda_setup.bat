@echo off
chcp 65001 > nul
if %errorlevel% neq 0 (
    echo 更改代码页失败！
    pause
    exit /b 1
)

setlocal EnableDelayedExpansion

set "ENV_NAME=env"  REM 设置你的环境名称
set "ENV_PATH=%cd%\%ENV_NAME%"

REM 检查环境是否存在
if exist "!ENV_PATH!" (
    echo 环境 "!ENV_NAME!" 已存在，正在激活...
) else (
    echo 环境 "!ENV_NAME!" 不存在，正在创建...
    conda create -p %ENV_NAME% python=3.13 -y
    if %errorlevel% neq 0 (
        echo 创建环境失败，退出脚本
        pause
        exit /b 1
    )
)


REM 激活环境
call conda activate %ENV_PATH%
if %errorlevel% neq 0 (
    echo 激活环境失败，退出脚本
    pause
    exit /b 1
)

set "PIPENV_PYPI_MIRROR=https://mirrors.aliyun.com/pypi/simple"
set "HF_ENDPOINT=https://hf-mirror.com"


echo 设置环境变量成功


echo 安装依赖
pip install -r requirements.txt
::conda deactivate


cmd \k
pause
