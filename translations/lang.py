from pyi18n import PyI18n


class Lang:
    def __init__(self):
        i18n = PyI18n(("en", "es"), load_path="translations/")
        self.translate: callable = i18n.gettext

