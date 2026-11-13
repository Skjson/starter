"""HTTP и JSON раздела отчётов."""

from flask import request
from . import bp, service


@bp.get("/api/reports")
def get_items():
    kind = request.args.get("kind", "groups")
    return {"kind": kind, "items": service.get_report(kind)}
