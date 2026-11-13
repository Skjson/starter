"""Blueprint функционального раздела reports."""

from flask import Blueprint

bp = Blueprint(
    "reports", __name__, template_folder="templates",
    static_folder="static", static_url_path="/reports/static",
)

# Импорт после создания bp позволяет зарегистрировать декораторы.
from . import pages, api
