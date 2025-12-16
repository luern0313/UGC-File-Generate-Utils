#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证生成的镜头参数是否符合设定的目标
"""

import sys
import os

# 添加项目根目录和proto_gen目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../proto_gen"))

from helper.file_helper import FileHelper
import gia_pb2

def parse_gia_file(file_path):
    """
    解析gia文件并返回解析结果
    
    Args:
        file_path: gia文件路径
        
    Returns:
        解析后的GIACollection对象
    """
    # 读取文件
    proto_bytes, success = FileHelper.load(file_path)
    if not success:
        raise Exception(f"读取文件失败: {file_path}")
    
    # 解析数据
    message = gia_pb2.GIACollection()
    message.ParseFromString(proto_bytes)
    
    return message

def verify_horizontal_angle_lens(camera_data, lens_num):
    """
    验证水平角镜头参数
    
    Args:
        camera_data: CameraData对象
        lens_num: 镜头名称对应的数字
        
    Returns:
        (是否通过, 错误信息)
    """
    # 计算期望的水平角值
    expected_angle = lens_num - 500
    
    # 验证水平角限制范围
    if camera_data.min_horizontal_angle != expected_angle:
        return False, f"水平角下限错误: 期望 {expected_angle}, 实际 {camera_data.min_horizontal_angle}"
    
    if camera_data.max_horizontal_angle != expected_angle:
        return False, f"水平角上限错误: 期望 {expected_angle}, 实际 {camera_data.max_horizontal_angle}"
    
    return True, ""

def verify_pitch_angle_lens(camera_data, lens_num):
    """
    验证俯仰角镜头参数
    
    Args:
        camera_data: CameraData对象
        lens_num: 镜头名称对应的数字
        
    Returns:
        (是否通过, 错误信息)
    """
    # 计算期望的俯仰角值
    expected_angle = lens_num - 1000
    
    # 验证俯仰角限制范围
    if camera_data.min_pitch_angle != expected_angle:
        return False, f"俯仰角下限错误: 期望 {expected_angle}, 实际 {camera_data.min_pitch_angle}"
    
    if camera_data.max_pitch_angle != expected_angle:
        return False, f"俯仰角上限错误: 期望 {expected_angle}, 实际 {camera_data.max_pitch_angle}"
    
    return True, ""

def verify_distance_lens(camera_data, lens_num):
    """
    验证视距镜头参数
    
    Args:
        camera_data: CameraData对象
        lens_num: 镜头名称对应的数字
        
    Returns:
        (是否通过, 错误信息)
    """
    # 计算期望的视距值
    expected_distance = (lens_num - 1500) / 10.0
    
    # 验证视距限制范围，允许一定的浮点数误差
    if abs(camera_data.min_distance - expected_distance) > 0.01:
        return False, f"视距下限错误: 期望 {expected_distance}, 实际 {camera_data.min_distance}"
    
    if abs(camera_data.max_distance - expected_distance) > 0.01:
        return False, f"视距上限错误: 期望 {expected_distance}, 实际 {camera_data.max_distance}"
    
    if abs(camera_data.default_distance - expected_distance) > 0.01:
        return False, f"默认视距错误: 期望 {expected_distance}, 实际 {camera_data.default_distance}"
    
    return True, ""

def verify_field_of_view_lens(camera_data, lens_num):
    """
    验证视野镜头参数
    
    Args:
        camera_data: CameraData对象
        lens_num: 镜头名称对应的数字
        
    Returns:
        (是否通过, 错误信息)
    """
    # 计算期望的视野值
    expected_fov = lens_num - 2000
    
    # 验证视野
    if camera_data.field_of_view != expected_fov:
        return False, f"视野错误: 期望 {expected_fov}, 实际 {camera_data.field_of_view}"
    
    return True, ""

def main():
    print("=" * 80)
    print("验证生成的镜头参数是否符合设定的目标")
    print("=" * 80)
    print()
    
    # 生成的gia文件路径
    file_path = "./output/camera_variations.gia"
    
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        print("请先运行generate_camera_variations.py生成文件")
        return
    
    print(f"文件路径: {file_path}")
    print(f"文件大小: {os.path.getsize(file_path)} 字节")
    print()
    
    try:
        # 解析文件
        collection = parse_gia_file(file_path)
        
        # 统计镜头数量
        total_lenses = len(collection.Assets)
        print(f"总镜头数量: {total_lenses}")
        print()
        
        # 验证结果统计
        verify_results = {
            "horizontal_angle": {"total": 0, "passed": 0, "failed": 0},  # 水平角镜头
            "pitch_angle": {"total": 0, "passed": 0, "failed": 0},  # 俯仰角镜头
            "distance": {"total": 0, "passed": 0, "failed": 0},  # 视距镜头
            "field_of_view": {"total": 0, "passed": 0, "failed": 0}  # 视野镜头
        }
        
        failed_lenses = []  # 保存验证失败的镜头
        
        # 遍历所有镜头
        for asset in collection.Assets:
            # 检查是否有camera_config
            if asset.HasField("camera_config"):
                camera_config = asset.camera_config
                
                # 遍历camera_details列表
                for camera_detail in camera_config.camera_details:
                    camera_data = camera_detail.camera_data
                    
                    # 根据镜头名称判断类型
                    lens_name = camera_data.name
                    
                    try:
                        lens_num = int(lens_name)
                        
                        # 判断镜头类型并验证
                        if 320 <= lens_num <= 680:  # 水平角镜头
                            verify_results["horizontal_angle"]["total"] += 1
                            passed, error_msg = verify_horizontal_angle_lens(camera_data, lens_num)
                            if passed:
                                verify_results["horizontal_angle"]["passed"] += 1
                            else:
                                verify_results["horizontal_angle"]["failed"] += 1
                                failed_lenses.append(("horizontal_angle", lens_name, error_msg))
                            
                        elif 911 <= lens_num <= 1089:  # 俯仰角镜头
                            verify_results["pitch_angle"]["total"] += 1
                            passed, error_msg = verify_pitch_angle_lens(camera_data, lens_num)
                            if passed:
                                verify_results["pitch_angle"]["passed"] += 1
                            else:
                                verify_results["pitch_angle"]["failed"] += 1
                                failed_lenses.append(("pitch_angle", lens_name, error_msg))
                            
                        elif 1510 <= lens_num <= 1800:  # 视距镜头
                            verify_results["distance"]["total"] += 1
                            passed, error_msg = verify_distance_lens(camera_data, lens_num)
                            if passed:
                                verify_results["distance"]["passed"] += 1
                            else:
                                verify_results["distance"]["failed"] += 1
                                failed_lenses.append(("distance", lens_name, error_msg))
                            
                        elif 2030 <= lens_num <= 2060:  # 视野镜头
                            verify_results["field_of_view"]["total"] += 1
                            passed, error_msg = verify_field_of_view_lens(camera_data, lens_num)
                            if passed:
                                verify_results["field_of_view"]["passed"] += 1
                            else:
                                verify_results["field_of_view"]["failed"] += 1
                                failed_lenses.append(("field_of_view", lens_name, error_msg))
                            
                    except ValueError:
                        # 如果名称不是数字，跳过
                        continue
        
        # 打印验证结果
        print("验证结果统计:")
        print("=" * 80)
        
        total_passed = 0
        total_failed = 0
        
        for lens_type, stats in verify_results.items():
            passed = stats["passed"]
            failed = stats["failed"]
            total = stats["total"]
            
            total_passed += passed
            total_failed += failed
            
            status = "✅" if failed == 0 else "❌"
            print(f"{status} {lens_type}: {passed}/{total} 通过")
            if failed > 0:
                print(f"    失败: {failed} 个")
        
        print()
        print(f"总验证结果: {total_passed}/{total_lenses} 通过")
        
        if total_failed == 0:
            print("✅ 所有镜头参数验证通过！")
        else:
            print(f"❌ 有 {total_failed} 个镜头参数验证失败")
        
        print("=" * 80)
        
        # 打印失败的镜头详细信息
        if failed_lenses:
            print()
            print("失败镜头详细信息:")
            print("-" * 80)
            
            for i, (lens_type, lens_name, error_msg) in enumerate(failed_lenses[:20]):  # 只显示前20个
                print(f"{i+1}. {lens_type} 镜头 {lens_name}: {error_msg}")
            
            if len(failed_lenses) > 20:
                print(f"... 还有 {len(failed_lenses) - 20} 个失败镜头未显示")
            
            print("-" * 80)
        
        # 打印样本镜头信息
        print()
        print("样本镜头参数:")
        print("-" * 80)
        
        sample_count = 0
        sample_types = set()
        
        for asset in collection.Assets:
            if asset.HasField("camera_config"):
                camera_config = asset.camera_config
                
                for camera_detail in camera_config.camera_details:
                    camera_data = camera_detail.camera_data
                    lens_name = camera_data.name
                    
                    try:
                        lens_num = int(lens_name)
                        
                        # 确定镜头类型
                        lens_type = ""
                        if 320 <= lens_num <= 680:  # 水平角镜头
                            lens_type = "horizontal_angle"
                        elif 911 <= lens_num <= 1089:  # 俯仰角镜头
                            lens_type = "pitch_angle"
                        elif 1510 <= lens_num <= 1800:  # 视距镜头
                            lens_type = "distance"
                        elif 2030 <= lens_num <= 2060:  # 视野镜头
                            lens_type = "field_of_view"
                        
                        # 如果该类型还没有样本，显示该镜头
                        if lens_type and lens_type not in sample_types:
                            sample_types.add(lens_type)
                            sample_count += 1
                            
                            print(f"{lens_type} 镜头 {lens_name}:")
                            print(f"    水平角范围: {camera_data.min_horizontal_angle}° 到 {camera_data.max_horizontal_angle}°")
                            print(f"    俯仰角范围: {camera_data.min_pitch_angle}° 到 {camera_data.max_pitch_angle}°")
                            print(f"    视距范围: {camera_data.min_distance} 到 {camera_data.max_distance}")
                            print(f"    默认视距: {camera_data.default_distance}")
                            print(f"    视野: {camera_data.field_of_view}°")
                            print()
                            
                            # 如果已经显示了所有类型的样本，停止
                            if sample_count >= 4:
                                break
                    except ValueError:
                        continue
                
                if sample_count >= 4:
                    break
        
        print("=" * 80)
        print("验证完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
