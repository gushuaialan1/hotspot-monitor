import logging
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def send_report(html_path: str, recipient: Optional[str] = None) -> None:
    path = Path(html_path)
    if not path.exists():
        logger.error("Report file not found: %s", html_path)
        return

    logger.info("Sending report: %s", html_path)
    try:
        result = subprocess.run(
            ["send_message", "--file", str(path), "--type", "html"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            logger.error("send_message failed: %s", result.stderr)
        else:
            logger.info("send_message succeeded: %s", result.stdout)
    except FileNotFoundError:
        logger.warning("send_message command not found, skipping delivery")
