"""Функциональные разделы учебного журнала."""


def positive_id(value, label):
    """Проверяет целый положительный идентификатор в диапазоне SQLite."""
    if type(value) is not int or not 1 <= value <= 2**63 - 1:
        raise ValueError(f"{label}: укажите положительный целый ID.")
    return value
