if exist ".venv\Scripts\activate.bat" (
    echo Virtual environment already exists
    call ".venv\Scripts\activate.bat"
) else (
    echo Creating a new virtual environment
    python -m pip install --upgrade pip
    pip install uv
    uv venv .venv
    call ".venv\Scripts\activate.bat"
    uv sync
)
