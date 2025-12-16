#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件Proto解析器
使用FileHelper读取文件，并用预编译的proto模块解析
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../proto_gen"))

import tkinter as tk
from tkinter import filedialog

from helper.file_helper import FileHelper
from proto_gen import gia_pb2


def select_file():
    """弹出文件选择对话框"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    file_path = filedialog.askopenfilename(
        title="选择要解析的文件",
        filetypes=[
            ("所有文件", "*.*")
        ]
    )

    return file_path


def parse_with_proto(proto_bytes: bytes) -> str:
    """
    使用编译后的proto类解析数据

    Args:
        proto_bytes: protobuf字节数据

    Returns:
        str: 解析结果文本
    """
    try:
        # 解析数据
        message = gia_pb2.GIACollection()
        message.ParseFromString(proto_bytes)

        # 转换为文本格式
        from google.protobuf import text_format
        result = text_format.MessageToString(message, as_utf8=True)

        return result

    except Exception as e:
        raise Exception(f"Error: 解析失败: {e}")


def main():
    print("=" * 70)
    print("Protobuf Decoder with .proto")
    print("=" * 70)
    print()

    # 检查命令行参数
    file_path = None
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"使用命令行参数指定的文件: {file_path}")
    else:
        # 选择文件
        file_path = select_file()

    if not file_path:
        print("未选择文件，程序退出。")
        return

    print()
    print(f"选择的文件: {file_path}")
    print(f"文件大小: {os.path.getsize(file_path)} 字节")

    data, success = FileHelper.load(file_path)

    # 解析数据
    print("解析Protobuf数据")
    print("=" * 70)

    parsed_text = parse_with_proto(data)

    # 显示结果
    print("解析结果")
    print("=" * 70)
    print(parsed_text)
    print("=" * 70)
    print()

    # 保存结果到文件
    save_option = input("是否保存解析结果到文件? (y/N): ").strip().lower()
    if save_option == 'y':
        output_file = file_path + ".decoded.txt"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"文件: {file_path}\n")
                f.write("=" * 70 + "\n\n")
                f.write(parsed_text)
            print(f"结果已保存到: {output_file}")
        except Exception as e:
            print(f"Error: 保存文件失败: {e}")


if __name__ == "__main__":
    main()
