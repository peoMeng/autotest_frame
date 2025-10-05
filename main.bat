@REM 创建虚拟环境同步依赖并激活
call uv_env.bat

@REM 接收run.py传递的所有命令行参数
python run_task.py %*