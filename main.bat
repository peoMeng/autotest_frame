@echo --创建虚拟环境同步依赖--
call uv_env.bat

@echo --接收run.py传递的所有命令行参数--
python run_task.py %*