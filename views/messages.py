from jinja2 import Environment, FileSystemLoader, select_autoescape
from views.custom_filters import escape
import random

# Подключаем шаблоны
env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
env.filters["escape"] = escape

# Список эмоджи для кнопки
CONFIRM_EMOJIS = ["✅", "👍", "🟢", "🎯", "💚", "🟩"]

def render_new_member_joined_message(new_member: dict):
    """
    Формирует текст приветственного сообщения с рандомным эмоджи
    """
    confirm_emoji = random.choice(CONFIRM_EMOJIS)
    params = {
        "new_member": new_member,
        "confirm_emoji": confirm_emoji
    }
    tpl = env.get_template("new_member_joined_message.j2")
    text = tpl.render(params)
    return text, confirm_emoji
