chcp 65001
@echo off
cd /d "%~dp0"

where protoc >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到protoc命令，请检查是否已安装protobuf。
    pause
    exit /b 1
)

set /p "confirm=将清空"proto_gen/"目录，重新编译"proto/"下的protobuf文件并输出，是否继续？(y/N): "
if /i not "%confirm%"=="y" (
    echo 取消执行
    pause
    exit /b 1
)

del /q proto_gen\*

echo 正在重新编译protobuf文件...

protoc --python_out=proto_gen/ --proto_path=proto/ --pyi_out=proto_gen/ proto/entity.proto
protoc --python_out=proto_gen/ --proto_path=proto/ --pyi_out=proto_gen/ proto/asset.proto
protoc --python_out=proto_gen/ --proto_path=proto/ --pyi_out=proto_gen/ proto/gia.proto

echo Done!
pause