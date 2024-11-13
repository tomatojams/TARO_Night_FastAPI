# pug 렌더링
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from pypugjs.ext.jinja import PyPugJSExtension
from fastapi.staticfiles import StaticFiles


# Jinja2Templates로 설정
template_env = Environment(
    loader=FileSystemLoader("views"),  # 템플릿 디렉토리 설정
    extensions=[PyPugJSExtension],  # PyPugJS 확장자 추가
)

templates = Jinja2Templates(directory="views")
templates.env = template_env  # PyPugJS를 지원하는 Jinja2 환경으로 설정


def get_template():
    return templates


def mount_static_files(app):
    app.mount("/static", StaticFiles(directory="views/static"), name="static")
    app.mount("/js", StaticFiles(directory="views/js"), name="js")
