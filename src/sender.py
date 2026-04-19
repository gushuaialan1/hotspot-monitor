import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def send_report(html_path: str, recipient: Optional[str] = None) -> None:
    path = Path(html_path)
    if not path.exists():
        logger.error("Report file not found: %s", html_path)
        return

    logger.info("Report generated at: %s", html_path)

    # Try to use Hermes send_message if running inside Hermes environment
    try:
        from hermes_tools import send_message as hermes_send

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        target = recipient or "weixin"
        hermes_send(message=content, target=target)
        logger.info("Report sent to %s via Hermes", target)
    except ImportError:
        logger.info(
            "hermes_tools not available (normal outside Hermes). "
            "Report saved to %s for manual delivery.",
            html_path,
        )
    except Exception as e:
        logger.error("Failed to send report: %s", e)
