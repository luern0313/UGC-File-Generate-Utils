# 镜头生成工具 (Camera Generation Tools)

这是一个用于生成和验证游戏镜头配置的工具集，支持从原始GIA文件提取镜头数据，生成各种镜头变体，并验证生成结果的正确性。

## 功能概述

1. **镜头数据提取**：从原始GIA文件中提取镜头配置数据
2. **镜头模板管理**：管理不同类型的镜头模板
3. **镜头变体生成**：生成各种参数的镜头变体
4. **镜头验证**：验证生成的镜头参数是否符合设定的目标
5. **GIA文件解析**：解析和比较生成的GIA文件

## 依赖项

- Python 3.8+
- grpcio-tools (用于编译proto文件)
- protobuf (用于序列化和反序列化数据)

## 安装依赖

```bash
pip install -r requirements.txt
```

## 文件结构

```
generate_camera/
├── output/                  # 生成的文件输出目录
├── compare_binary_files.py  # 比较二进制文件的工具
├── generate_camera.py       # 生成镜头模板的主脚本
├── generate_camera_variations.py  # 生成各种镜头变体的脚本
├── test_camera_generation.py  # 测试镜头生成脚本
└── verify_camera_parameters.py  # 验证镜头参数是否符合设定的目标
```

## 主要文件说明

### 1. generate_camera.py

从原始GIA文件中提取镜头数据，并生成新的镜头模板GIA文件。

**功能**：
- 读取并解析原始GIA文件
- 提取结构化的镜头数据
- 将解析的数据赋值给对应的镜头模板
- 生成新的镜头模板GIA文件

**使用**：
```bash
python generate_camera.py
```

### 2. generate_camera_variations.py

生成各种参数的镜头变体，包括水平角、俯仰角、视距和视野变化。

**功能**：
- 生成水平角限制范围变化的镜头（-180°到180°）
- 生成俯仰角限制范围变化的镜头（-89°到89°）
- 生成视距限制范围变化的镜头（1到30，步长0.1）
- 生成视野变化的镜头（30°到60°）

**使用**：
```bash
python generate_camera_variations.py
```

### 3. verify_camera_parameters.py

验证生成的镜头参数是否符合设定的目标。

**功能**：
- 解析生成的GIA文件
- 验证水平角镜头参数
- 验证俯仰角镜头参数
- 验证视距镜头参数
- 验证视野镜头参数

**使用**：
```bash
python verify_camera_parameters.py
```

### 4. test_camera_generation.py

测试镜头生成脚本，对比原始和新生成的GIA文件的raw解析差异。

**功能**：
- 解析原始GIA文件
- 解析生成的GIA文件
- 对比两个文件的raw解析结果
- 输出差异详情

**使用**：
```bash
python test_camera_generation.py
```

### 8. compare_binary_files.py

比较两个二进制文件的差异。

**功能**：
- 逐字节比较两个二进制文件
- 输出差异位置和内容

**使用**：
```bash
python compare_binary_files.py <file1> <file2>
```

## 使用示例

### 生成镜头模板

```bash
python generate_camera.py
```

### 生成镜头变体

```bash
python generate_camera_variations.py
```

### 验证镜头参数

```bash
python verify_camera_parameters.py
```

### 测试镜头生成

```bash
python test_camera_generation.py
```

## 输出文件

生成的文件将保存在`output`目录中：

- `camera_templates.gia` - 生成的镜头模板文件
- `camera_variations.gia` - 生成的镜头变体文件
- `camera_variations.gia.decoded.txt` - 镜头变体文件的解析结果
- `original_raw.txt` - 原始文件的raw解析结果
- `generated_raw.txt` - 生成文件的raw解析结果

## 编译Proto文件

如果需要重新编译proto文件，可以使用以下命令：

```bash
python compile_camera_proto.py
```

## 项目结构

```
├── assembler/               # 资源组装器
├── config/                  # 配置文件
├── generate_camera/         # 镜头生成工具（当前目录）
├── model/                   # 数据模型
├── parser/                  # 文件解析器
├── proto/                   # Proto定义文件
└── proto_gen/               # 编译后的Proto文件
```

## 开发说明

1. **镜头模板**：所有镜头模板定义在`model/camera_model.py`中
2. **Proto定义**：镜头数据的Proto定义在`proto/camera.proto`中
3. **资源组装**：镜头资源的组装逻辑在`assembler/camera_assembler.py`中
4. **文件解析**：GIA文件的解析逻辑在`parser/parser_with_raw_data.py`和`parser/parser_with_proto.py`中
