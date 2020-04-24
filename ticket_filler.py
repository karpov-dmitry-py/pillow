# -*- coding: utf-8 -*-

# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png

# Написать консольный скрипт c помощью встроенного python-модуля agrparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.

#  для запуска из командной строки можно применить такой вызов - см ниже.:
#  python ticket.py "Карпов Дмитрий" 'SVO' 'BKK' '2021-01-31' --save_result_path='images'

from PIL import Image, ImageDraw, ImageFont, ImageColor
import os.path
import argparse

class TicketFiller():

    def __init__(self, fio, departure, destination, travel_date, save_result_path = None,  template_path = None, font_path = None):
        self.fio = fio
        self.departure = departure
        self.destination = destination
        self.travel_date = travel_date
        self.template_path = template_path if template_path else os.path.normpath(os.path.join('images', 'ticket_template.png'))
        self.font_path = font_path if font_path else os.path.normpath(os.path.join('fonts', 'ofont.ru_Arial Cyr.ttf'))
        self.save_result_path = os.path.normpath(save_result_path.replace("'", "")) if \
            save_result_path else os.path.dirname(__file__)

    def prepare_text(self, text):
        return text.replace("'", "").upper()

    def go(self):

        try:
            template = Image.open(self.template_path)
        except BaseException as exc:
            print(f'Ошибка открытия шаблона билета. Тип ошибки: {exc.__class__.__name__}, описание ошибки: {exc.args}')
            return

        try:
            font = ImageFont.truetype(self.font_path, 14)
        except BaseException as exc:
            print(f'Ошибка открытия шрифта. Тип ошибки: {exc.__class__.__name__}, описание ошибки: {exc.args}')
            return

        tool = ImageDraw.Draw(template)
        color = ImageColor.colormap['black']

        width, height       = template.size
        top_hor             = int(width * .067)
        top_vert            = int(height * .31)
        blocks_hor_gap      = 241
        blocks_vert_gap     = 69

        data_coords = {}
        data_coords[self.prepare_text(self.fio)]            = (top_hor, top_vert)
        data_coords[self.prepare_text(self.departure)]      = (top_hor, top_vert + blocks_vert_gap)
        data_coords[self.prepare_text(self.destination)]    = (top_hor, top_vert + blocks_vert_gap * 2)
        data_coords[self.prepare_text(self.travel_date)]    = (top_hor + blocks_hor_gap, top_vert + blocks_vert_gap * 2)

        for content, coords in data_coords.items():
            tool.text(coords, content, color, font)

        file, extension = os.path.splitext(self.template_path)

        result_file_name = f'processed_ticket{extension}'
        result_full_path = os.path.normpath(os.path.join(self.save_result_path, result_file_name)) \
            if self.save_result_path else result_file_name

        try:
            template.save(result_full_path)
        except BaseException as exc:
            print(f'Ошибка сохранения обработанного билета: {exc.args}')
            return

        print(f'Заполнение билета выполнено! Результат сохранен в путь: {result_full_path}')

def main():

    parser = argparse.ArgumentParser(description='Данные для заполнения билета')
    parser.add_argument('fio', type=str, help='ФИО пассажира')
    parser.add_argument('departure', type=str, help='Место вылета')
    parser.add_argument('destination', type=str, help='Место прилета')
    parser.add_argument('travel_date', type=str, help='Дата вылета')
    parser.add_argument('--save_result_path', type=str, help='Каталог сохранения заполненного билета')
    args = parser.parse_args()

    filler = TicketFiller(args.fio, args.departure, args.destination, args.travel_date,
                          args.save_result_path if args.save_result_path else None
    )
    filler.go()

if __name__ == '__main__':
    main()