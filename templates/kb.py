from aiogram.utils.keyboard import InlineKeyboardBuilder


def keyboard(data: list, adj=None):
        kb = InlineKeyboardBuilder()
        for b in data:
            if isinstance(b[1], dict):
                kb.button(text=b[0], **b[1])
            else:
                kb.button(text=b[0], callback_data=b[1])
        if adj is None:
            adj = [1 for i in range(len(data))]
        kb.adjust(*adj)
        return kb.as_markup()


start = keyboard([
     #["Рефералка", "repheral"],
     #["Ввести промокод", "promo"]
])

choose_type = keyboard([
     ["Загрузить видео (.mp4)", "download_video"],
     ["Загрузить аудио (.mp3)", "download_audio"]
     #["Назад", "start"]
])