#!/usr/bin/env python3
"""
ModelScope Image 图片生成器
基于魔搭平台异步 API 生成图片
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from PIL import Image
from io import BytesIO

# 导入配置管理器
try:
    from config_manager import ConfigManager
except ImportError:
    # 如果直接运行，尝试从当前目录导入
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from config_manager import ConfigManager


# 支持的宽高比预设
ASPECT_RATIOS = [
    "2.35:1", "21:9", "2:1", "16:9", "3:2", "4:3", "5:4",
    "1:1", "4:5", "3:4", "2:3", "9:16"
]

# 支持的模型
MODELS = {
    "z-image": "Tongyi-MAI/Z-Image-Turbo",
    "qwen-image": "Qwen/Qwen-Image-2512"
}


def parse_aspect_ratio(ratio_str: str) -> Tuple[float, float]:
    """
    解析宽高比字符串

    Args:
        ratio_str: 宽高比字符串，如 "16:9" 或 "2.35:1"

    Returns:
        (width_ratio, height_ratio) 元组
    """
    try:
        parts = ratio_str.split(':')
        if len(parts) != 2:
            raise ValueError(f"无效的宽高比格式: {ratio_str}")

        width = float(parts[0])
        height = float(parts[1])

        if width <= 0 or height <= 0:
            raise ValueError(f"宽高比必须大于 0: {ratio_str}")

        return width, height
    except (ValueError, IndexError) as e:
        raise ValueError(f"无法解析宽高比 '{ratio_str}': {e}")


def calculate_size(aspect_ratio: str, long_edge: int = 2048) -> Tuple[int, int]:
    """
    根据宽高比和长边计算实际像素尺寸

    Args:
        aspect_ratio: 宽高比字符串，如 "16:9"
        long_edge: 长边像素值，默认 2048

    Returns:
        (width, height) 像素尺寸
    """
    # 限制长边范围
    if long_edge < 64:
        long_edge = 64
    elif long_edge > 2048:
        long_edge = 2048

    ratio_w, ratio_h = parse_aspect_ratio(aspect_ratio)

    if ratio_w >= ratio_h:
        # 横向或正方形：宽度是长边
        width = long_edge
        height = round(long_edge * (ratio_h / ratio_w))
    else:
        # 竖向：高度是长边
        height = long_edge
        width = round(long_edge * (ratio_w / ratio_h))

    # 确保尺寸在有效范围内
    width = max(64, min(2048, width))
    height = max(64, min(2048, height))

    return width, height


def generate_image(
    prompt: str,
    model: Optional[str] = None,
    aspect_ratio: str = "1:1",
    long_edge: int = 2048,
    output_path: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: int = 300,
    polling_interval: int = 5,
    loras: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    生成图片

    Args:
        prompt: 提示词
        model: 模型 ID（如果为 None，使用配置的默认模型）
        aspect_ratio: 宽高比
        long_edge: 长边像素值
        output_path: 输出文件路径
        api_key: API Key（如果为 None，从配置读取）
        base_url: Base URL（如果为 None，从配置读取）
        timeout: 超时秒数
        polling_interval: 轮询间隔秒数
        loras: LoRA 配置

    Returns:
        包含任务信息的字典
    """
    # 加载配置
    config_manager = ConfigManager()

    if not api_key:
        api_key = config_manager.get_api_key()
        if not api_key:
            raise RuntimeError(
                "未配置 API Key！\n"
                "请访问 https://modelscope.cn/my/myaccesstoken 获取 API Key，\n"
                "然后运行: python config_manager.py set api_key YOUR_API_KEY"
            )

    if not base_url:
        base_url = config_manager.get_base_url()

    if not model:
        model = config_manager.get_default_model()

    # 移除末尾斜杠
    base_url = base_url.rstrip('/')

    # 计算尺寸
    width, height = calculate_size(aspect_ratio, long_edge)
    size_str = f"{width}x{height}"

    print(f"[PROMPT] 提示词: {prompt}")
    print(f"[MODEL] 模型: {model}")
    print(f"[RATIO] 宽高比: {aspect_ratio}")
    print(f"[SIZE] 尺寸: {size_str}")

    # 构建请求体
    request_body = {
        "model": model,
        "prompt": prompt,
        "size": size_str
    }

    # 添加 LoRA 配置
    if loras:
        request_body["loras"] = loras

    # 构建请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-ModelScope-Async-Mode": "true"
    }

    # 步骤 1：提交任务
    print("\n[SUBMIT] 提交任务...")
    try:
        response = requests.post(
            f"{base_url}/v1/images/generations",
            headers=headers,
            data=json.dumps(request_body, ensure_ascii=False).encode('utf-8'),
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        task_id = result.get("task_id")

        if not task_id:
            raise RuntimeError(f"API 未返回 task_id: {result}")

        print(f"[OK] 任务已提交，ID: {task_id}")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"提交任务失败: {e}")

    # 步骤 2：轮询任务状态
    print(f"\n[WAIT] 等待生成完成（超时: {timeout}秒，轮询间隔: {polling_interval}秒）...")

    start_time = time.time()
    task_headers = {
        "Authorization": f"Bearer {api_key}",
        "X-ModelScope-Task-Type": "image_generation"
    }

    while True:
        elapsed = time.time() - start_time

        if elapsed > timeout:
            raise TimeoutError(f"任务超时（{timeout}秒）")

        time.sleep(polling_interval)

        try:
            status_response = requests.get(
                f"{base_url}/v1/tasks/{task_id}",
                headers=task_headers,
                timeout=30
            )
            status_response.raise_for_status()
            status_data = status_response.json()

            task_status = status_data.get("task_status")

            if task_status == "SUCCEED":
                print(f"[OK] 生成完成！耗时: {elapsed:.1f}秒")
                output_images = status_data.get("output_images", [])

                if not output_images:
                    raise RuntimeError("API 未返回输出图片")

                image_url = output_images[0]

                # 步骤 3：下载图片
                print(f"\n[DOWNLOAD] 下载图片...")
                image_response = requests.get(image_url, timeout=60)
                image_response.raise_for_status()

                image = Image.open(BytesIO(image_response.content))

                # 保存图片
                if output_path:
                    output_file = Path(output_path)
                else:
                    output_file = Path(f"modelscope_{task_id}.png")

                # 确保输出目录存在
                output_file.parent.mkdir(parents=True, exist_ok=True)

                image.save(output_file)
                print(f"[OK] 图片已保存: {output_file.absolute()}")

                return {
                    "task_id": task_id,
                    "status": "success",
                    "image_url": image_url,
                    "output_path": str(output_file.absolute()),
                    "size": size_str,
                    "model": model,
                    "elapsed_time": elapsed
                }

            elif task_status == "FAILED":
                error_msg = status_data.get("error") or status_data.get("message") or "未知错误"
                raise RuntimeError(f"图片生成失败: {error_msg}")

            elif task_status in ["PENDING", "RUNNING"]:
                print(f"  状态: {task_status}，已等待 {elapsed:.1f}秒...")

            else:
                print(f"  未知状态: {task_status}")

        except requests.exceptions.RequestException as e:
            print(f"  轮询出错: {e}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="ModelScope Image 图片生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 生成 16:9 横向图片
  python image_generator.py "一只金色的猫" --aspect-ratio "16:9"

  # 生成 9:16 竖向图片，指定输出路径
  python image_generator.py "赛博朋克城市夜景" --aspect-ratio "9:16" --output cat.png

  # 使用特定模型和长边
  python image_generator.py "山水画" --model qwen-image --long-edge 1024

  # 指定 API Key（覆盖配置文件）
  python image_generator.py "风景" --api-key YOUR_API_KEY
"""
    )

    parser.add_argument('prompt', help='图片描述提示词')
    parser.add_argument('--model', '-m',
                       choices=list(MODELS.keys()) + list(MODELS.values()),
                       help='模型（z-image 或 qwen-image，默认使用配置的模型）')
    parser.add_argument('--aspect-ratio', '-a', default='1:1',
                       help=f'宽高比（默认 1:1），支持: {", ".join(ASPECT_RATIOS[:5])}...')
    parser.add_argument('--long-edge', '-l', type=int, default=2048,
                       help='长边像素值（64-2048，默认 2048）')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--api-key', help='API Key（覆盖配置文件）')
    parser.add_argument('--base-url', help='Base URL（覆盖配置文件）')
    parser.add_argument('--timeout', '-t', type=int, default=300,
                       help='超时秒数（默认 300）')
    parser.add_argument('--polling-interval', '-p', type=int, default=5,
                       help='轮询间隔秒数（默认 5）')

    args = parser.parse_args()

    # 处理模型参数
    model = args.model
    if model and model in MODELS:
        model = MODELS[model]

    try:
        result = generate_image(
            prompt=args.prompt,
            model=model,
            aspect_ratio=args.aspect_ratio,
            long_edge=args.long_edge,
            output_path=args.output,
            api_key=args.api_key,
            base_url=args.base_url,
            timeout=args.timeout,
            polling_interval=args.polling_interval
        )

        print("\n" + "="*50)
        print("[OK] 成功！")
        print("="*50)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
