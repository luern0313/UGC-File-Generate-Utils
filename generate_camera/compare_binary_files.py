#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比较两个二进制文件的差异
"""

import os
import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from helper.file_helper import FileHelper


def main():
    """主函数"""
    print("=" * 70)
    print("二进制文件比较工具")
    print("=" * 70)
    print()
    
    # 定义文件路径
    original_file = os.path.join(os.path.dirname(__file__), "镜头.gia")
    generated_file = os.path.join(os.path.dirname(__file__), "output/camera_templates.gia")
    
    # 检查文件是否存在
    if not os.path.exists(original_file):
        print(f"Error: 原始文件不存在: {original_file}")
        return
    
    if not os.path.exists(generated_file):
        print(f"Error: 生成的文件不存在: {generated_file}")
        return
    
    # 读取原始文件的protobuf数据
    print("1. 读取原始文件的protobuf数据...")
    original_proto_data = FileHelper.load(original_file)[0]
    print(f"原始文件protobuf数据长度: {len(original_proto_data)} 字节")
    print()
    
    # 读取生成的文件的protobuf数据
    print("2. 读取生成的文件的protobuf数据...")
    generated_proto_data = FileHelper.load(generated_file)[0]
    print(f"生成的文件protobuf数据长度: {len(generated_proto_data)} 字节")
    print()
    
    # 比较二进制数据
    print("3. 比较二进制数据...")
    if original_proto_data == generated_proto_data:
        print("✅ 二进制数据完全一致！")
    else:
        print("❌ 二进制数据不一致！")
        print()
        
        # 显示差异
        print("差异详情:")
        print(f"{'偏移量':>8} | {'原始文件':<10} | {'生成的文件':<10} | {'描述':<20}")
        print("-" * 60)
        
        min_len = min(len(original_proto_data), len(generated_proto_data))
        max_len = max(len(original_proto_data), len(generated_proto_data))
        
        for i in range(max_len):
            if i < min_len:
                original_byte = original_proto_data[i]
                generated_byte = generated_proto_data[i]
                if original_byte != generated_byte:
                    print(f"{i:>8} | {original_byte:02x}        | {generated_byte:02x}        | 字节不同")
            elif i < len(original_proto_data):
                print(f"{i:>8} | {original_proto_data[i]:02x}        | --         | 原始文件有额外字节")
            else:
                print(f"{i:>8} | --         | {generated_proto_data[i]:02x}        | 生成的文件有额外字节")
    
    print()
    print("=" * 70)
    print("比较完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()
