#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试镜头生成脚本，对比原始和新生成的GIA文件的raw解析差异
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from helper.file_helper import FileHelper
from parser.parser_with_raw_data import decode_raw_protobuf


def main():
    """主函数"""
    print("=" * 70)
    print("镜头生成测试脚本")
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
    
    # 解析原始文件
    print("1. 解析原始文件 镜头.gia...")
    original_data, success = FileHelper.load(original_file)
    if not success:
        print(f"Error: 读取原始文件失败: {original_file}")
        return
    
    original_raw = decode_raw_protobuf(original_data)
    print(f"原始文件解析完成，长度: {len(original_raw)}")
    print()
    
    # 解析生成的文件
    print("2. 解析生成的文件 output/camera_templates.gia...")
    generated_data, success = FileHelper.load(generated_file)
    if not success: 
        print(f"Error: 读取生成的文件失败: {generated_file}")
        return
    
    generated_raw = decode_raw_protobuf(generated_data)
    print(f"生成的文件解析完成，长度: {len(generated_raw)}")
    print()
    
    # 保存解析结果到文件
    print("3. 保存解析结果到文件...")
    original_output = os.path.join(os.path.dirname(__file__), "output/original_raw.txt")
    generated_output = os.path.join(os.path.dirname(__file__), "output/generated_raw.txt")
    
    with open(original_output, "w", encoding="utf-8") as f:
        f.write(original_raw)
    print(f"原始文件解析结果已保存到: {original_output}")
    
    with open(generated_output, "w", encoding="utf-8") as f:
        f.write(generated_raw)
    print(f"生成的文件解析结果已保存到: {generated_output}")
    print()
    
    # 对比解析结果
    print("4. 对比解析结果...")
    if original_raw == generated_raw:
        print("✅ 解析结果完全一致！")
    else:
        print("❌ 解析结果不一致！")
        print()
        
        # 逐行对比
        original_lines = original_raw.split('\n')
        generated_lines = generated_raw.split('\n')
        
        max_lines = max(len(original_lines), len(generated_lines))
        
        print("差异详情:")
        print(f"{'行号':>4} | {'原始文件':<40} | {'生成的文件':<40}")
        print("-" * 90)
        
        for i in range(max_lines):
            original_line = original_lines[i] if i < len(original_lines) else ""
            generated_line = generated_lines[i] if i < len(generated_lines) else ""
            
            if original_line != generated_line:
                print(f"{i+1:>4} | {original_line:<40} | {generated_line:<40}")
        
        print()
        print("建议：根据差异修正代码，确保生成的文件与原始文件的protobuf结构完全一致")
    
    print()
    print("=" * 70)
    print("测试完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()
