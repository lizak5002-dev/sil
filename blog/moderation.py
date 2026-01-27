class ModerationBlog():
    def __init__(self):
        self.stop_words = [
            'спам', 'реклама', 'купить', 'продать', 'дешево',
            'скидка', 'акция', 'распродажа', 'заработок',
            'обман', 'мошенник', 'взлом', 'пароль', 'халява',
            'казино', 'ставки', 'кредит', 'ипотека', 'займ',
        ]
    
    def check_text(self, text):
        if not text:
            return True, []
    
        text_lower = text.lower()
        found_words = []

        for word in self.stop_words:
            if word in text_lower:
                found_words.append(word)

        return len(found_words) == 0, found_words
    
    def check_post(self, title, content):
        full_text = f"{title} {content}"
        return self.check_text(full_text)