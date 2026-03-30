#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protobuf Raw Decoder
使用protobuf decode_raw方式解析
"""

import tkinter as tk
from tkinter import filedialog
import os
import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from google.protobuf.internal import decoder, wire_format

from helper.file_helper import FileHelper


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


def decode_raw_protobuf_to_dict(data):
    """使用Python protobuf库解析原始protobuf数据为字典"""
    try:
        pos = 0

        def decode_field(data, pos):
            """递归解析protobuf字段"""
            fields = {}
            while pos < len(data):
                try:
                    # 解析tag (field_number << 3 | wire_type)
                    tag, new_pos = decoder._DecodeVarint(data, pos)
                    if new_pos == pos:
                        break

                    field_number = tag >> 3
                    wire_type = tag & 0x7
                    pos = new_pos

                    # 根据wire type解析值
                    if wire_type == wire_format.WIRETYPE_VARINT:
                        # Varint (int32, int64, uint32, uint64, bool, enum)
                        value, pos = decoder._DecodeVarint(data, pos)
                        fields[field_number] = value

                    elif wire_type == wire_format.WIRETYPE_FIXED64:
                        # Fixed64 (fixed64, sfixed64, double)
                        value = data[pos:pos + 8]
                        pos += 8
                        # 尝试解析为不同类型
                        import struct
                        int_val = struct.unpack('<Q', value)[0]
                        double_val = struct.unpack('<d', value)[0]
                        fields[field_number] = {'hex': value.hex(), 'fixed64': int_val, 'double': double_val}

                    elif wire_type == wire_format.WIRETYPE_LENGTH_DELIMITED:
                        # Length-delimited (string, bytes, embedded messages, packed repeated fields)
                        length, pos = decoder._DecodeVarint(data, pos)
                        value = data[pos:pos + length]
                        pos += length

                        # 尝试判断是否为嵌套消息
                        try:
                            # 尝试作为UTF-8字符串解析
                            str_value = value.decode('utf-8')
                            if str_value.isprintable() or all(c in '\n\r\t ' or c.isprintable() for c in str_value):
                                fields[field_number] = str_value
                            else:
                                raise UnicodeDecodeError('utf-8', b'', 0, 1, 'not printable')
                        except (UnicodeDecodeError, AttributeError):
                            # 可能是嵌套消息
                            try:
                                # 尝试作为嵌套消息解析
                                nested_fields, _ = decode_field(value, 0)
                                fields[field_number] = nested_fields
                            except:
                                # 显示为bytes
                                fields[field_number] = {'hex': value.hex(), 'bytes': value}

                    elif wire_type == wire_format.WIRETYPE_FIXED32:
                        # Fixed32 (fixed32, sfixed32, float)
                        value = data[pos:pos + 4]
                        pos += 4
                        import struct
                        int_val = struct.unpack('<I', value)[0]
                        float_val = struct.unpack('<f', value)[0]
                        fields[field_number] = {'hex': value.hex(), 'fixed32': int_val, 'float': float_val}

                    else:
                        fields[field_number] = {'unknown_wire_type': wire_type}
                        break

                except Exception as e:
                    fields['error'] = f"解析错误 at position {pos}: {e}"
                    break

            return fields, pos

        fields, _ = decode_field(data, 0)
        return fields

    except Exception as e:
        return {"error": f"解析错误: {str(e)}\n{type(e).__name__}"}


def decode_raw_protobuf(data):
    """使用Python protobuf库解析原始protobuf数据"""
    try:
        result = []
        pos = 0
        indent_level = 0

        def add_line(text, indent=0):
            result.append("  " * indent + text)

        def decode_field(data, pos, indent=0):
            """递归解析protobuf字段"""
            while pos < len(data):
                try:
                    # 解析tag (field_number << 3 | wire_type)
                    tag, new_pos = decoder._DecodeVarint(data, pos)
                    if new_pos == pos:
                        break

                    field_number = tag >> 3
                    wire_type = tag & 0x7
                    pos = new_pos

                    # 根据wire type解析值
                    if wire_type == wire_format.WIRETYPE_VARINT:
                        # Varint (int32, int64, uint32, uint64, bool, enum)
                        value, pos = decoder._DecodeVarint(data, pos)
                        add_line(f"{field_number}: {value}", indent)

                    elif wire_type == wire_format.WIRETYPE_FIXED64:
                        # Fixed64 (fixed64, sfixed64, double)
                        value = data[pos:pos + 8]
                        pos += 8
                        # 尝试解析为不同类型
                        import struct
                        int_val = struct.unpack('<Q', value)[0]
                        double_val = struct.unpack('<d', value)[0]
                        add_line(f"{field_number}: 0x{value.hex()} (fixed64: {int_val}, double: {double_val})", indent)

                    elif wire_type == wire_format.WIRETYPE_LENGTH_DELIMITED:
                        # Length-delimited (string, bytes, embedded messages, packed repeated fields)
                        length, pos = decoder._DecodeVarint(data, pos)
                        value = data[pos:pos + length]
                        pos += length

                        # 尝试判断是否为嵌套消息
                        try:
                            # 尝试作为UTF-8字符串解析
                            str_value = value.decode('utf-8')
                            if str_value.isprintable() or all(c in '\n\r\t ' or c.isprintable() for c in str_value):
                                add_line(f'{field_number}: "{str_value}"', indent)
                            else:
                                raise UnicodeDecodeError('utf-8', b'', 0, 1, 'not printable')
                        except (UnicodeDecodeError, AttributeError):
                            # 可能是嵌套消息或二进制数据
                            add_line(f"{field_number} {{", indent)
                            try:
                                decode_field(value, 0, indent + 1)
                                add_line("}", indent)
                            except:
                                # 如果不是有效的嵌套消息，显示为bytes
                                result.pop()  # 移除开括号
                                add_line(f"{field_number}: <{len(value)} bytes: 0x{value.hex()}>", indent)

                    elif wire_type == wire_format.WIRETYPE_FIXED32:
                        # Fixed32 (fixed32, sfixed32, float)
                        value = data[pos:pos + 4]
                        pos += 4
                        import struct
                        int_val = struct.unpack('<I', value)[0]
                        float_val = struct.unpack('<f', value)[0]
                        add_line(f"{field_number}: 0x{value.hex()} (fixed32: {int_val}, float: {float_val})", indent)

                    else:
                        add_line(f"{field_number}: <unknown wire type {wire_type}>", indent)
                        break

                except Exception as e:
                    add_line(f"# 解析错误 at position {pos}: {e}", indent)
                    break

            return pos

        decode_field(data, 0, 0)
        return "\n".join(result)

    except Exception as e:
        return f"解析错误: {str(e)}\n{type(e).__name__}"


def main():
    print("=" * 70)
    print("Protobuf Raw Decoder")
    print("=" * 70)

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
    print()
    print("=" * 70)
    print("Protobuf Decode Raw 结果:")
    print("=" * 70)

    result = decode_raw_protobuf(data)
    print(result)
    print()

    # 保存结果到文件
    save_option = input("是否保存解析结果到文件? (y/N): ")
    if save_option.lower() == 'y':
        output_file = file_path + ".decoded.txt"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"文件: {file_path}\n")
                f.write("=" * 70 + "\n\n")
                f.write(result)
            print(f"结果已保存到: {output_file}")
        except Exception as e:
            print(f"Error: 保存文件失败: {e}")


if __name__ == "__main__":
    main()
