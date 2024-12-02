@echo off
chcp 65001 > nul
if %errorlevel% neq 0 (
    echo 更改代码页失败！
    pause
    exit /b 1
)

setlocal EnableDelayedExpansion
REM 清空 Python 相关环境变量
set "PATH=%PATH:Python;=%"
set "PATH=%PATH:Python\Scripts;=%"
set "PYTHONHOME="
set "PYTHONPATH="

set PYTHON_HOME=%~dp0env
set PATH=%PYTHON_HOME%;%PYTHON_HOME%\Scripts;%PATH%
set INCLUDE=%INCLUDE%;%PYTHON_PATH%\include
set "PIPENV_PYPI_MIRROR=https://mirrors.aliyun.com/pypi/simple"


echo 设置环境变量成功


echo 等待程序启动...



%PYTHON_HOME%\python.exe -m streamlit run app.py
pause
