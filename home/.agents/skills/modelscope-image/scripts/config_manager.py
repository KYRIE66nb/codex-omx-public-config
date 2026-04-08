#!/usr/bin/env python3
"""
ModelScope Image API 配置管理器
管理 API Key 和默认模型配置
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


class ConfigManager:
    """管理 ModelScope Image 配置"""

    CONFIG_DIR = Path.home() / ".modelscope-image"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    DEFAULT_CONFIG = {
        "api_key": "",
        "base_url": "https://api-inference.modelscope.cn/",
        "default_model": "Tongyi-MAI/Z-Image-Turbo"
    }

    def __init__(self):
        """初始化配置管理器"""
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """确保配置目录存在"""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.CONFIG_FILE.exists():
            return self.DEFAULT_CONFIG.copy()

        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并默认配置，确保所有字段存在
                return {**self.DEFAULT_CONFIG, **config}
        except (json.JSONDecodeError, IOError) as e:
            print(f"警告：加载配置文件失败: {e}")
            return self.DEFAULT_CONFIG.copy()

    def save_config(self, config: Dict[str, Any]):
        """保存配置文件"""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise RuntimeError(f"保存配置文件失败: {e}")

    def get_api_key(self) -> Optional[str]:
        """获取 API Key"""
        config = self.load_config()
        api_key = config.get("api_key", "").strip()
        return api_key if api_key else None

    def set_api_key(self, api_key: str):
        """设置 API Key"""
        config = self.load_config()
        config["api_key"] = api_key.strip()
        self.save_config(config)

    def get_base_url(self) -> str:
        """获取 Base URL"""
        config = self.load_config()
        return config.get("base_url", self.DEFAULT_CONFIG["base_url"])

    def set_base_url(self, base_url: str):
        """设置 Base URL"""
        config = self.load_config()
        config["base_url"] = base_url.strip().rstrip('/')
        self.save_config(config)

    def get_default_model(self) -> str:
        """获取默认模型"""
        config = self.load_config()
        return config.get("default_model", self.DEFAULT_CONFIG["default_model"])

    def set_default_model(self, model: str):
        """设置默认模型"""
        config = self.load_config()
        config["default_model"] = model.strip()
        self.save_config(config)

    def is_configured(self) -> bool:
        """检查是否已配置 API Key"""
        api_key = self.get_api_key()
        return api_key is not None and len(api_key) > 0

    def reset(self):
        """重置配置为默认值"""
        self.save_config(self.DEFAULT_CONFIG.copy())


def main():
    """命令行工具"""
    import argparse

    parser = argparse.ArgumentParser(description="ModelScope Image 配置管理")
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # get 命令
    get_parser = subparsers.add_parser('get', help='获取配置')
    get_parser.add_argument('key', choices=['api_key', 'base_url', 'default_model', 'all'],
                           help='配置项')

    # set 命令
    set_parser = subparsers.add_parser('set', help='设置配置')
    set_parser.add_argument('key', choices=['api_key', 'base_url', 'default_model'],
                           help='配置项')
    set_parser.add_argument('value', help='配置值')

    # check 命令
    subparsers.add_parser('check', help='检查配置状态')

    # reset 命令
    subparsers.add_parser('reset', help='重置配置')

    args = parser.parse_args()
    manager = ConfigManager()

    if args.command == 'get':
        if args.key == 'all':
            config = manager.load_config()
            # 隐藏 API Key
            if config.get('api_key'):
                config['api_key'] = config['api_key'][:8] + '...'
            print(json.dumps(config, indent=2, ensure_ascii=False))
        elif args.key == 'api_key':
            api_key = manager.get_api_key()
            if api_key:
                print(api_key[:8] + '...')
            else:
                print("未配置")
        elif args.key == 'base_url':
            print(manager.get_base_url())
        elif args.key == 'default_model':
            print(manager.get_default_model())

    elif args.command == 'set':
        if args.key == 'api_key':
            manager.set_api_key(args.value)
            print("API Key 已设置")
        elif args.key == 'base_url':
            manager.set_base_url(args.value)
            print(f"Base URL 已设置为: {args.value}")
        elif args.key == 'default_model':
            manager.set_default_model(args.value)
            print(f"默认模型已设置为: {args.value}")

    elif args.command == 'check':
        if manager.is_configured():
            print("[OK] 已配置 API Key")
            print(f"  Base URL: {manager.get_base_url()}")
            print(f"  默认模型: {manager.get_default_model()}")
        else:
            print("[X] 未配置 API Key")
            print("\n请访问以下链接获取 API Key：")
            print("https://modelscope.cn/my/myaccesstoken")

    elif args.command == 'reset':
        manager.reset()
        print("配置已重置")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
