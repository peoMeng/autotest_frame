if exist ".venv\Scripts\activate.bat" (
    echo 虚拟环境已存在
    call ".venv\Scripts\activate.bat"
) else (
    echo 创建新的虚拟环境...
    python -m venv ".venv"
    call ".venv\Scripts\activate.bat"
    python -m pip install --upgrade pip
    pip install uv
    uv sync
)