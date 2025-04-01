"""
File: measures.py
Description: 资源文件的绝对路径，兼容打包后的环境
Author: Misaka-xxw
Created: 2025-04-01
"""
import os
import sys


def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容打包后的环境"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    print(resource_path("config.json"))
    print(resource_path(os.path.join("fonts", "font1.otf")))
