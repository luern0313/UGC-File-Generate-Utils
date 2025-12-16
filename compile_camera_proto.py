#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译camera.proto文件的Python脚本
无需系统安装protoc编译器，使用Python的grpc_tools.protoc模块
"""

import os
import sys
from grpc_tools import protoc


def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置输出路径和proto包含路径
    output_dir = os.path.join(script_dir, 'proto_gen')
    proto_include = os.path.join(script_dir, '.venv', 'Lib', 'site-packages', 'grpc_tools', '_proto')
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 只获取camera和asset的proto文件
    proto_dir = os.path.join(script_dir, 'proto')
    # 只编译camera.proto和asset.proto文件
    proto_files = [
        os.path.join(proto_dir, 'camera.proto'),
        os.path.join(proto_dir, 'asset.proto')
    ]
    # 确保文件存在
    proto_files = [f for f in proto_files if os.path.exists(f)]
    
    # 构建protoc命令参数
    args = [
        'grpc_tools.protoc',
        f'--proto_path={proto_dir}',
        f'--python_out={output_dir}',
        f'--pyi_out={output_dir}',
        f'--proto_path={proto_include}',
    ]
    
    # 添加所有proto文件
    args.extend(proto_files)
    
    print(f"Compiling proto files: {', '.join([os.path.basename(f) for f in proto_files])}...")
    
    # 执行编译
    result = protoc.main(args)
    
    if result == 0:
        print("Compilation successful!")
        return 0
    else:
        print(f"Compilation failed with exit code {result}!")
        return result


if __name__ == "__main__":
    sys.exit(main())