from django import template

register = template.Library()

@register.filter()
def censor(value):
    censor_list = [                          # писок запрещенных слов, корни слов
        'редис',
        'падл'
    ]
    try:
        if not isinstance(value, str):
            raise TypeError
        word_list = value.split()                # получаем список слов из входного потока
        for i in range(len(word_list)):          # цикл прохода по всем словам текста
            word_check = word_list[i]            # берем слово для проверки
            if not word_check[0].isalpha():      # проверка на отсутствие в слове букв с самого начала (черточки, и т.д.)
                continue                         # сразу пропускаем этот вариант
            if word_check[-1].isalpha():         # если конец слова - буква
                word_al = word_check             # буквенное слово = слову
                word_n_al = ''                   # небуквенная концовка - пустая
            else:                                     # если есть небуквенный символ(ы) в конце слова
                n_al = -2                             # позиция проверяемого на букву символа (-1 уже проверена)
                while True:                           # цикл поиска концевых небуквенных символов (точки, знаки и т.д.)
                    if word_check[n_al].isalpha():    # если встретилась буква
                        break                         # прерывание цикла
                    n_al -= 1                         # смещение влево не след позицию
                word_al = word_check[:(n_al + 1)]     # получаем буквенную часть слова (n_al надо уменьшить на 1,
                                                      #  т.к. n_al указывает на букву после прерывания цикла)
                word_n_al = word_check[(n_al + 1):]   # небуквенная часть слова
            for root_curse in censor_list:            # цикл проверки на наличие корня ругательного слова в
                                                      # буквенном слове
                if root_curse in word_al:             # если найден корень ругательного слова
                    word_al = word_al[0] + '*' * (len(word_al) - 1)  # подменяем в буквенном слове все символы,
                                                                     # кроме 1-го - на звездочки.
                    break                                            # прекращаем проверку, слово ругательное
            if word_al + word_n_al != word_check:           # если контрольное слово изменено
                word_list[i] = word_al + word_n_al          # заменяем на него слово в основном списке
    except (TypeError):
        return 'Invalid value for censor filter'

    return ' '.join(word_list)                    # возврат обновленной строки - словачерез пробел.









