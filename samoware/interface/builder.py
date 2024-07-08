from typing import Optional


class XIMSSBuilder:
    def __init__(self, root_tag):
        self._root_tag = root_tag
        self.ximss = f"<{root_tag}>"

    def add_element(self, tag: str, text: str, attributes: Optional[dict] = None) -> None:
        if attributes:
            attr_str = ' '.join([f'{key}="{value}"' for key, value in attributes.items()])
            self.ximss += f"<{tag} {attr_str}/>{text}"
        else:
            self.ximss += f"<{tag}/>{text}"

    def end_element(self, tag):
        self.ximss += f"</{tag}>"

    def __str__(self):
        return self.ximss + f"</{self._root_tag}>"

    def __repr__(self):
        return str(self)
