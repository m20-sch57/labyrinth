# декоратор для класса описывающего уникальный предмет
def unique(key):
    """
    key - ключ, который будет установлен
          этому уникальному объекту.
    """
    def unique_decorator(cls):
        old_function = cls.set_settings

        def set_settings(self, *args, **kwargs):
            """
            Новая функция дополнительно будет устанавливать
            указанный уникальный ключ.
            """
            self.labyrinth.set_unique(self, key)
            return old_function(self, *args, **kwargs)
        # изменяем функцию в классе.
        cls.set_settings = set_settings
        cls.add_meta('unique_object')
        return cls
    return unique_decorator
