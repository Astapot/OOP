from vk_api.keyboard import VkKeyboard, VkKeyboardColor


start_keyboard = VkKeyboard(one_time=True)
start_keyboard.add_button('Найди людей', color=VkKeyboardColor.PRIMARY)
start_keyboard.add_line()
start_keyboard.add_button('Вывести список избранных', color=VkKeyboardColor.SECONDARY)
start_keyboard.add_line()
start_keyboard.add_button('Старт', color=VkKeyboardColor.NEGATIVE)

continue_keyboard = VkKeyboard(one_time=False)
continue_keyboard.add_button('Следующий', color=VkKeyboardColor.POSITIVE)
continue_keyboard.add_button('Добавить в избранное', color=VkKeyboardColor.PRIMARY)
continue_keyboard.add_line()
continue_keyboard.add_button('В начало', color=VkKeyboardColor.NEGATIVE)