#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
存档文件写入/导出工具类
自动处理存档文件的header和footer
"""

import struct
from typing import Union


class FileHelper:
    """
    GIA文件写入器

    文件格式：
    [0-3]    uint32 (大端) - 文件长度-4
    [4-7]    固定值: 00 00 00 01
    [8-11]   固定值: 00 00 03 26
    [12-15]  固定值: 00 00 00 03
    [16-19]  uint32 (大端) - 文件长度-24
    [20-N]   Protobuf数据
    [N+1-N+4] 固定值: 00 00 06 79
    """

    HEADER_FIELD_1 = b'\x00\x00\x00\x01'
    HEADER_FIELD_2 = b'\x00\x00\x03\x26'
    HEADER_FIELD_3 = b'\x00\x00\x00\x03'

    FOOTER = b'\x00\x00\x06\x79'

    @staticmethod
    def save(proto_data: Union[bytes, bytearray], filename: str) -> bool:
        """
        保存protobuf数据为GIA文件

        Args:
            proto_data: protobuf编码后的字节数组
            filename: 保存的文件路径

        Returns:
            bool: 保存是否成功
        """
        try:
            # 确保proto_data是bytes类型
            if isinstance(proto_data, bytearray):
                proto_data = bytes(proto_data)
            elif not isinstance(proto_data, bytes):
                raise TypeError(f"Error: proto_data必须是bytes或bytearray类型，当前是 {type(proto_data)}")

            # 计算文件大小
            proto_size = len(proto_data)
            total_file_size = 20 + proto_size + 4

            # 计算header中的两个大小字段
            size_field_1 = total_file_size - 4
            size_field_2 = total_file_size - 24

            # 构建header
            header = (
                struct.pack('>I', size_field_1) +
                FileHelper.HEADER_FIELD_1 +
                FileHelper.HEADER_FIELD_2 +
                FileHelper.HEADER_FIELD_3 +
                struct.pack('>I', size_field_2)
            )

            file_data = header + proto_data + FileHelper.FOOTER

            with open(filename, 'wb') as f:
                f.write(file_data)

            # 打印信息
            print(f"文件已保存至 {filename}")
            print(f"文件大小: {total_file_size} 字节")
            print(f"Protobuf大小: {proto_size} 字节")

            return True

        except Exception as e:
            print(f"Error: 保存GIA文件失败 {e}")
            return False

    @staticmethod
    def load(filename: str) -> tuple[bytes | None, bool]:
        """
        读取GIA文件并提取protobuf数据

        Args:
            filename: GIA文件路径

        Returns:
            tuple: (proto_data, success)
                - proto_data: 提取的protobuf字节数据
                - success: 是否成功
        """
        try:
            # 读取文件
            with open(filename, 'rb') as f:
                file_data = f.read()

            file_size = len(file_data)

            # 验证文件大小
            if file_size < 24:
                print(f"Error: 文件 {file_size} 字节，至少需要24字节")
                return None, False

            header = file_data[:20]
            footer = file_data[-4:]
            proto_data = file_data[20:-4]

            size_field_1 = struct.unpack('>I', header[0:4])[0]
            size_field_2 = struct.unpack('>I', header[16:20])[0]

            print(f"文件大小: {file_size} 字节")
            print(f"Header[0-3]: {header[0:3].hex()} ({size_field_1}) 期望{file_size - 4}")
            print(f"Header[4-8]: {header[4:8].hex()}")
            print(f"Header[8-12]: {header[8:12].hex()}")
            print(f"Header[12-16]: {header[12:16].hex()}")
            print(f"Header[0-3]: {header[16:20].hex()} ({size_field_2}) 期望{file_size - 24}")
            print(f"Footer: {footer.hex()}")

            return proto_data, True

        except FileNotFoundError:
            print(f"Error: 文件不存在 {filename}")
            return None, False
        except Exception as e:
            print(f"Error: 读取文件失败 {e}")
            return None, False
