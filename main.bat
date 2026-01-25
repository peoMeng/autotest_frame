@echo Create virtual environment and sync dependencies
call uv_env.bat

@echo Receive all command-line arguments passed from run.py
python run_task.py %*
