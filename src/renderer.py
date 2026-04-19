from datetime import datetime
from pathlib import Path
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader

from src.config import Config
from src.models import SelectedItem


def render_report(selected: List[SelectedItem], config: Config, template_dir: str = "templates") -> str:
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report.html")

    grouped: Dict[str, List[SelectedItem]] = {
        "history": [],
        "emotion": [],
        "wisdom": [],
    }
    for item in selected:
        if item.account_type in grouped:
            grouped[item.account_type].append(item)

    accounts = config.accounts
    today = datetime.now().strftime("%Y-%m-%d")

    return template.render(
        date=today,
        accounts=accounts,
        grouped=grouped,
    )


def save_report(html: str, output_path: str) -> None:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
