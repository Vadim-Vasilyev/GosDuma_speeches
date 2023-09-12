import pandas as pd
import re

df_location = "/speeches.csv" #your dataframe location
save_to = "/speeches_clear.csv"

df = pd.read_csv(df_location, index_col=0)

def clear(speech):
    result = re.sub(r"^.{0,40} по карточке [^.]{0,40}\.", "", speech)
    result = re.sub(r"\n.{0,40} по карточке [^.]{0,40}\.", "", result)
    result = re.sub(r"[А-ЯЁ]{1}.{0,40} по карточке [А-Яа-яЁё\s]{0,40}\.", "", result)
    result = re.sub(r"По карточке[^.]{0,30}[А-Я]{1}[^.]{0,30}[А-Я]{1}[^.]{0,30}\.", "", result)
    result = re.sub(r"по карточке[^.]{0,30}[А-Я]{1}[^.]{0,30}[А-Я]{1}[^.]{0,30}\.", "", result)
    result = re.sub(r"Gо карточке\s[А-ЯЁ]{1}[^.]{0,30}[А-Я]{1}[^.]{0,30}\.", "", result)
    result = re.sub(r"по карточке\s[А-ЯЁ]{1}[^.]{0,30}[А-Я]{1}[^.]{0,30}\.", "", result)
    result = re.sub(r"По карточке[^.]{0,30}[А-Я]{1}[^.]{0,30}[А-Я]{1}[^.]{0,30}[А-Я]{1}", "", result)
    result = re.sub(r"по карточке[^.]{0,30}[А-Я]{1}[^.]{0,30}[А-Я]{1}[^.]{0,30}[А-Я]{1}", "", result)
    result = re.sub(r"По карточке [А-ЯЁ]{1}[а-яё]{0,20}\.", "", result)
    result = re.sub(r"по карточке [А-ЯЁ]{1}[а-яё]{0,20}\.", "", result)

    result = re.sub(r"[А-ЯЁё]+\s{0,1}[А-ЯЁё]\.\s{0,1}[А-ЯЁё]\.\,[^\.]+\.", "", result)
    result = re.sub(r"[А-ЯЁё]+\s{0,1}[А-ЯЁё]\.\s{0,1}[А-ЯЁё]\.", "", result)

    result = re.sub(r"\([^0-9\)]*(из зала|в зале|Аплодисменты|аплодисменты)+[^0-9\)]*\)", "", result)
    result = re.sub(r"\([^0-9\)]*(шум|смех|выкрики|оживление|Шум|Смех|Выкрики|Оживление)+[^0-9\)]*\)", "", result)
    result = re.sub(r"\([^0-9\)]*(Микрофон|микрофон|отключен|отчключён|выключен)+[^0-9\)]*\)", "", result)
    result = re.sub(r"Председательствует[А-Яа-яЁё\s]+\s[А-ЯЁё]\.[А-ЯЁё]\.[А-Яа-яЁё]+", "", result)

    result = re.sub(r"РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ.{0,300}Результат\:.{0,30}\.", "", result)
    result = re.sub(r"РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ.{0,300}Результат\:.{0,30}\n", "", result)
    result = re.sub(r"РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ.{0,300}Результат\:.{0,50}\.", "", result)
    result = re.sub(r"РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ.{0,300}Результат\:.{0,50}\n", "", result)
    result = re.sub(r"РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ.{0,300}Решение\:.{0,30}\.", "", result)
    result = re.sub(r"РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ.{0,300}Решение\:.{0,30}\n", "", result)
    result = re.sub(r"РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ.{0,300}Решение\:.{0,50}\.", "", result)
    result = re.sub(r"РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ.{0,300}Решение\:.{0,50}\n", "", result)
    result = re.sub(r"РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ.{0,200}чел\.", "", result)

    result = re.sub(r"Уважаем.{0,50}\!\s", "", result)
    result = re.sub(r"Уважаем.{0,30}(ич|вна),\s", "", result)
    result = re.sub(r"[А-ЯЁ]{1}[а-яё]{0,20}\s[А-ЯЁ]{1}[а-яё]{0,30}ич,\s", "", result)
    result = re.sub(r"[А-ЯЁ]{1}[а-яё]{0,20}\s[А-ЯЁ]{1}[а-яё]{0,30}ич\.\s", "", result)
    result = re.sub(r"[А-ЯЁ]{1}[а-яё]{0,20}\s[А-ЯЁ]{1}[а-яё]{0,30}вна,\s", "", result)
    result = re.sub(r"[А-ЯЁ]{1}[а-яё]{0,20}\s[А-ЯЁ]{1}[а-яё]{0,30}вна\.\s", "", result)
    result = re.sub(r"Уважаем[а-яё]{0,30}\s[А-Яа-яЁё]{0,50},\s", "", result)
    result = re.sub(r"\sуважаем[а-яё]{0,3}\,\s", "", result)

    result = re.sub(r"Спасибо.", "", result)

    result = re.sub(r"  ", " ", result)
    result = re.sub(r" \.", ".", result)
    result = re.sub(r" \,", ",", result)
    return result.strip()

clear_column = [clear(s) for s in df['text']]
df.insert(5, "clear", clear_column)

df.to_csv(save_to)