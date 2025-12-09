#!/usr/bin/env bash

cd "$(dirname "$0")" || exit

if ! command -v protoc &> /dev/null; then
    echo "错误: 未找到protoc命令，请检查是否已安装protobuf。"
    exit 1
fi

read -p "将清空\"proto_gen/\"目录，重新编译\"proto/\"下的protobuf文件并输出，是否继续？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消执行"
    exit 1
fi

rm -rf proto_gen/*

echo "正在重新编译protobuf文件..."

protoc --python_out=proto_gen/ --proto_path=proto/ --pyi_out=proto_gen/ proto/entity.proto
protoc --python_out=proto_gen/ --proto_path=proto/ --pyi_out=proto_gen/ proto/asset.proto
protoc --python_out=proto_gen/ --proto_path=proto/ --pyi_out=proto_gen/ proto/gia.proto

echo "完成！"