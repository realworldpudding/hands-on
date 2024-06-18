from pathlib import Path

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fasthx import Jinja


def init_template(auto_reload: bool = True):
    base_dir = Path()
    paths = [
        base_dir / "pudding_todo" / "templates",
        base_dir / "pudding_todo" / "apps" / "account" / "templates",
        base_dir / "pudding_todo" / "apps" / "todo" / "templates",
    ]

    template_loader = FileSystemLoader(searchpath=paths)

    template_env = Environment(
        loader=template_loader,
        extensions=[
            "jinja2.ext.i18n",
            "jinja2.ext.loopcontrols",
            "jinja2.ext.do",
        ],
        autoescape=select_autoescape(["html", "xml"]),
        auto_reload=auto_reload,
    )
    templates = Jinja2Templates(env=template_env)
    return Jinja(templates)


tpl = init_template()
