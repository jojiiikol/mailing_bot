import __main__
from aiogram import Router, types, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import InputFile, FSInputFile, InputMediaPhoto

from keyboards.user_kb import *

user_router = Router()


@user_router.message(Command("start"))
async def start(message: types.Message):
    await __main__.db.insert_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"Привет, {message.from_user.username}, я бот, который будет ифнормировать тебя о фестивале молодежи!\n"
        f"Прошу подписаться тебя на канал https://t.me/djflkasdfhkjasldhfkjas. после того, как ты подпишешься, мы начнем работу!",
        reply_markup=get_check_subscription_kb().as_markup())


@user_router.message(Command("menu"))
async def menu_button(message: types.Message):
    user = await __main__.db.get_id_from_tg_id(tg_id=message.from_user.id)
    if user is None:
        await message.answer("К сожалению вы не подписаны, просим это сделать как можно быстрей!\nСделать это можно "
                             "с помощью команды /start")
    else:
        status = await __main__.bot.get_chat_member(chat_id=-1002092565895, user_id=message.from_user.id)
        if status.status in ['left', 'kicked']:
            await message.answer("К сожалению вы не подписаны на канал, просим это сделать как можно быстрей!")
        else:
            if not await __main__.db.check_subscription_status_user(tg_id=message.from_user.id):
                await message.answer(text="Подтвердите подписку", reply_markup=get_check_subscription_kb().as_markup())
            else:
                await message.answer(
                    text="Выберите необходимую опцию",
                    reply_markup=get_main_kb()
                )


@user_router.callback_query(F.data == 'check_subscription')
async def check_subscription(callback: types.CallbackQuery):
    await callback.answer()
    status = await __main__.bot.get_chat_member(chat_id=-1002092565895, user_id=callback.from_user.id)
    if status.status in ['left', 'kicked']:
        await callback.message.answer("К сожалению вы не подписаны, просим это сделать как можно быстрей!")
    else:
        await __main__.db.update_subscription_status_user(callback.from_user.id)
        await callback.message.answer(
            "Спасибо за подписку!")
        await callback.message.answer(
            text="Выберите необходимую опцию",
            reply_markup=get_main_kb()
        )
        await callback.message.delete()


@user_router.callback_query(F.data.contains('back_to_main'))
async def back_to_main(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    if callback.data.split("_")[3] != "0":
        await __main__.bot.delete_message(callback.message.chat.id, callback.data.split("_")[3])
    await callback.message.answer(
        text="Выберите необходимую опцию",
        reply_markup=get_main_kb()
    )


@user_router.callback_query(F.data == 'about_festival')
async def about_festival(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAINQ2Z0WstKqEzS-6eu2qGTn4hFGFDqAAIj4jEbUD2gS38SqeHsrNZAAQADAgADeQADNQQ",
        caption="МОЛОДЕЖЬ РЕШАЕТ, МОЛОДЕЖЬ ВЫБИРАЕТ!\n\nТЫ ГЛАВНЫЙ ГЕРОЙ СВОЕЙ ЖИЗНИ!\n\nНеделя молодежи - настоящий "
                "городской праздник со множеством активностей, в каждой из них тебя ждет своя увлекательная программа. "
                "Исследуй наполнение этих пространств, найди себя!\n\nНеделя молодежи объединит не только молодых людей, "
                "но и все поколения, станет по-настоящему семейным праздником.\n\nОбщую программу мероприятия ты найдешь в "
                "меню!",
        reply_markup=get_back_button()
    )

@user_router.callback_query(F.data == 'draw')
async def about_festival(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        text="29 июня на главной сцене «Ягома» будет проходить розыгрыш подарков среди присутствующих, "
             "не пропусти!\n\nГлавный приз – годовой запас пиццы от «До-До» и год интернета от «Метросети»\n\nА так же "
             "подарочные сертификаты от наших партнеров:\n\n1.Салон красоты «IDOL FACE»\n2.Салон красоты «Milana "
             "beauty»\n3.Студия красоты «LUXURY STUDIO»\n4.Шоурум «Аутфит»\n5.Dо4а\n6.Сибур\n7.Барбершоп «YUSUF»\n8.СК "
             "«STORM»\n9.Картинг «Югра Дрифт»\n10.Салон красоты «Хорошая девочка»\n11.Photolab "
             "фотостудия\n12.Боулинг-ресторан «Brooklyn Bowl»\n13.Центр проката КвадроМания Нижневартовск",
        reply_markup=get_back_button()
    )


@user_router.callback_query(F.data == 'logistic')
async def logistic(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAINSWZ0Wx1EqgRwR8i0qsr4aKcYLQb1AAIr4jEbUD2gS_7ssCrjX7GzAQADAgADeQADNQQ",
        caption="Лесной комплекс ЯГОМ расположен в районе Нижневартовского ГПЗ, на расстоянии 10 километров от "
                "памятника покорителям «Самотлора» и граничит с поймой реки Мысовая Мега. ЯГОМ внесен во многие "
                "навигаторы. До него легко добраться и найти.\n\nБолее подробная информация далее по ссылке\n\n"
                "https://vk.com/@-161303519-kak-do-nas-dobratsya",
        reply_markup=get_back_button()
    )


@user_router.callback_query(F.data == 'navigation')
async def logistic(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAILvGZzMrpuK5-JmKrjQK7S1F4c0xahAAK03zEbUD2YS2RDWHDZrnIcAQADAgADeQADNQQ",
        caption="Текст про карту",
        reply_markup=get_back_button()
    )


# @user_router.callback_query(F.data == 'contact')
# async def logistic(callback: types.CallbackQuery):
#     await callback.answer()
#     await callback.message.delete()
#     await callback.message.answer(
#         text="https://vk.com/molodnv",
#         reply_markup=get_back_button()
#     )


@user_router.callback_query(F.data == 'program')
async def program(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text="Выберите необходимую дату",
        reply_markup=get_program_kb()
    )


@user_router.callback_query(F.data == 'molod_day')
async def molod_day(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    photo_msg = await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAINh2Z0XzTxIi4UAuI6P2f_pJqCnHHZAAI94jEbUD2gS1PuSCcxid6EAQADAgADeQADNQQ"
    )
    await callback.message.answer(
        text="<b>Гастрономия</b>\n10:00-20:00 – Ресторан «Дана»\n11:00-20:00\n– Семейный ресторан «У Камелька»\n– Ресторан Изба "
             "New\n– Мороженное «Травушка Муравушка»\n\n"
             "<b>Ярмарка</b>\n12:00-18:00\n– Изделия из эпоксидной смолы "
             "«ArtStudioDeco»\n– Изделия макраме «Плети»\n– Украшения ручной работы «Wilvarinisil»\n12:00-19:00\n– Свечи "
             "ручной работы «Тепло в душЕ»\n– Аксессуары для волос, вязаные изделия «AnastasiyaCherneckaya»\n\n<b>Детская "
             "зона</b>\n12:00-14:00\n– Мастер-класс по приготовлению леденцов\n12:00-18:00\n- Мастер-класс «Гигантская "
             "раскраска»\n- Игровая программа с любимыми героями\n- Игровая зона\n– «Мыльные пузыри»\n- Площадка «Сладкая "
             "вата»\n- Игровая зона\n- «Деревянные игры»\n- Площадка «Аквагрим»\n14:00-16:00\n– Мастер-класс по созданию "
             "деревянного значка\n15:00-15:30\n– Научное шоу «Между нами химия»\n16:00-18:00\n– Мастер-класс по созданию "
             "браслета\n\n<b>Сцена</b>\n12:00-12:30\n– Официальное открытие «Дня молодежи»\n12:30-13:30\n– Звездные блоггеры с "
             "мастер-классом «Я-блогер»\n13:30-14:30\n– Награждение талантливой молодежи города\n14:30-15:00\n– "
             "Интерактивы, розыгрыши от партнеров\n15:00-17:00\n– Квартирник от амбассадоров арт-резиденции "
             "«Ядро»\n17:00-17:50\n– Концерт cover-band «Bourbon»\n17:50-18:00\n– Розыгрыш годового запаса пиццы от "
             "«До-До» и интернета от «Метросеть»\n18:00-19:00\n– Кавер-сет KIRILLDRUM & DJSHISHULION\n\n<b>Знание</b>\n12:30-13:20\n"
             "– Национальный туристический маршрут\n13:40-14:40\n- Промышленный туризм АО «СибурТюменьГаз»\n- "
             "Grill-Park «FINLAND»\n- Cosmos Smart Kogalym Hotel\n- Визит центр «Хуторок»\n- Открытый диалог\n14:50-15:00\n"
             "– Итоговая резолюция\n15:00-16:00\n– Открытая дискуссия молодежи с представителями бизнеса «Старт в "
             "бизнес»\n\n<b>Молодежь</b>\n12:30-15:00\n– Экологическая игра «Экотропа»\n12:30-16:00\n- Патриотическая площадка ("
             "Мастер-классы)\n- Чек-лист от психолога «Поверь в себя»\n- Достигай максимум!\n- «Молодежь на стиле»\n- "
             "Профориентационная площадка\n- Подкаст «Я по записи»\n15:00-16:00\n– Экологическая игра «Секреты "
             "переработки»\n\n<b>На встречу творчеству и креативу</b>\n14:30-15:00\n- Торжественное открытие "
             "арт-объекта\n15:00-16:00\n- «Акустический вайб». Музыкальный концерт в кругу друзей\n\n<b>Спорт</b>\n10:00-11:00\n– "
             "Кросс\n11:00-12:00\n– Семейный забег",
        reply_markup=get_back_button(photo_msg.message_id)
    )


@user_router.callback_query(F.data.contains("june_"))
async def date_program(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    data = callback.data.split("_")[1]
    if data == "24":
        await callback.message.answer_photo(
            photo="AgACAgIAAxkBAAINS2Z0W9n5aUqsUrnGWFXbKjLtxz31AAIv4jEbUD2gS7YU6pehRfvnAQADAgADeQADNQQ",
            caption="В понедельник ждёт насыщенный день! С утра — зарядка и баскетбол для бодрости тела и духа. А "
                    "вечером погружение в мир искусства.",
            reply_markup=get_back_from_event_button()
        )
    if data == "25":
        await callback.message.answer_photo(
            caption="Вторник, 25 июня - день насыщенных мероприятий для всех!\n\nВеселые командные игры для всей семьи, "
                    "лаборатория настольных игр с опытными ведущими, «Мафия» для любителей интриг и молодежный "
                    "кинопоказ в арт-резиденции «Ядро».\n\nИ, конечно же,  выставка креативного туризма об уникальных "
                    "возможностях путешествий по Югре!\n\nПриходите, будет интересно!",
            photo="AgACAgIAAxkBAAINTWZ0XEwm7QABytF-HUEjjbtPptsRhQACMuIxG1A9oEvqW6xxO9g9MAEAAwIAA3kAAzUE",
            reply_markup=get_back_from_event_button()
        )
    if data == "26":
        await callback.message.answer_photo(
            photo="AgACAgIAAxkBAAINT2Z0XJWQ6JrzyB7PM6brx8Cyb-t_AAI04jEbUD2gS8unBf4HqgafAQADAgADeQADNQQ",
            caption="Сегодня начни день с игр на открытом воздухе, а после окунись в атмосферу творчества и свободны.",
            reply_markup=get_back_from_event_button()
        )
    if data == "27":
        await callback.message.answer_photo(
            photo="AgACAgIAAxkBAAINUWZ0XNmyoKWxcPdEkPYRzQnFNvKtAAI14jEbUD2gSwYtiUg_2TbpAQADAgADeQADNQQ",
            caption="Четверг это маленькая пятница\n\nПоэтому нужно повеселиться на фитджитал танцах, занять ум "
                    "шахматами и узнать кто же все таки «Мафия»",
            reply_markup=get_back_from_event_button()
        )
    if data == "28":
        await callback.message.answer_photo(
            photo="AgACAgIAAxkBAAINU2Z0XTnPZr9fsaoaZoqnQzdZVl4uAAI44jEbUD2gS4ZSAygdrH2fAQADAgADeQADNQQ",
            caption="28 июня - праздник для всей семьи! Вас ждет насыщенный день с развлечениями для всех возрастов:\n\n"
                    "Семейные выходные с конкурсами и мастер-классами,\n\nВстреча любителей настольных игр с турнирами,\n\n"
                    "Зумба-вечеринка с зажигательными танцами,\n\nДень открытых дверей в скейт-парке с обучением, "
                    "мастер-классами и шоу от профессионалов.\n\nПриходите всей семьей и проведите незабываемый день!",
            reply_markup=get_back_from_event_button()
        )
    if data == "29":
        await callback.message.answer_photo(
            photo="AgACAgIAAxkBAAILvGZzMrpuK5-JmKrjQK7S1F4c0xahAAK03zEbUD2YS2RDWHDZrnIcAQADAgADeQADNQQ",
            caption="Текст про мероприятие на 29 число",
            reply_markup=get_back_from_event_button()
        )


@user_router.callback_query(F.data == "back_to_event")
async def back_to_event(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        text="Выберите необходимую дату",
        reply_markup=get_program_kb()
    )


# @user_router.message(F.content_type == ContentType.PHOTO)
# async def get__file_id(message: types.Message):
#     await __main__.bot.send_message(chat_id=513173580, text=message.photo[-1].file_id)
