from pathlib import Path
import os
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader
import json
import re
import requests


def render_html(
    template_name: str,
    data: Dict[str, Any],
    output_path: str,
    template_dir: str = "templates",
) -> str:

    # ایجاد پوشه خروجی در صورت نیاز
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # تنظیم محیط Jinja2
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

    # بارگذاری قالب
    template = env.get_template(template_name)

    # رندر کردن قالب با داده‌ها
    html_content = template.render(**data)

    # ذخیره فایل HTML
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return True

    except OSError:
        return False


def save_json(json_path, adr_folder):
    Path(json_path).parent.mkdir(parents=True, exist_ok=True)

    data = {"download_path": str(adr_folder)}

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_path(json_path):
    with open(json_path, "r") as file:
        data = json.load(file)
        return data


def set_address(json_path):
    data = Path(load_path(json_path)["download_path"])
    pop_path = data / "pop"
    rap_path = data / "rap"
    remix_path = data / "remix"
    other_path = data / "other"
    report_path = data / "report"
    try:
        for path in [pop_path, rap_path, remix_path, other_path, report_path]:
            path.mkdir(parents=True, exist_ok=True)
        return {
            "pop_path": pop_path,
            "rap_path": rap_path,
            "remix_path": remix_path,
            "other_path": other_path,
            "report_path": report_path,
        }
    except OSError:
        return False


def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)
    filename = filename.strip().rstrip(".")

    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }

    if filename.upper() in reserved_names:
        filename = f"_{filename}"

    return filename or "unknown"
