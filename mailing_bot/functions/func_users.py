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
        f"Привет 🙌🏻\nЯ буду твоим проводником по Недели Молодежи и фестивалю День Молодежи на Ягоме! Но для начала "
        f"подпишись на наш канал Молодежный центр ✔️\nПосле подписки мы начнём экскурсию по предстоящим мероприятиям 🚀"
        f"\nhttps://t.me/molodnv",
        reply_markup=get_check_subscription_kb().as_markup())


@user_router.message(Command("menu"))
async def menu_button(message: types.Message):
    user = await __main__.db.get_id_from_tg_id(tg_id=message.from_user.id)
    if user is None:
        await message.answer("К сожалению вы не подписаны, просим это сделать как можно быстрей!\nСделать это можно "
                             "с помощью команды /start")
    else:
        status = await __main__.bot.get_chat_member(chat_id=-1001858677023, user_id=message.from_user.id)
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
    status = await __main__.bot.get_chat_member(chat_id=-1001858677023, user_id=callback.from_user.id)
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
        photo="AgACAgIAAxkBAAM9ZnU3AUlNI1uZc93LJFlqKemdrg4AApbZMRtR8KhLdcOKxa0jYIcBAAMCAAN5AAM1BA",
        caption="Отметьте День молодежи в уникальном лесном комплексе Ягом!\n\nЭто место, где можно не только интересно "
                "провести время, но и насладиться красотой нетронутой природы.\n\nЯгом - это настоящий оазис в близи "
                "города, где вы сможете:\n\n🌳 Прогуляться по живописным экологическим тропам и полюбоваться вековыми "
                "деревьями\n🐦 Понаблюдать за птицами, белками  и другими обитателями леса в их естественной среде\n🧘 "
                "Отдохнуть от городской суеты и зарядиться энергией природы\n\nА еще в программе события:\n💫 Звездные "
                "блогеры\n🎨 Творческие, экологические мастер-классы и полезные лекции\n🎤 Выступления амбассадоров "
                "арт-резиденции «Ядро»\n🏃 Спортивные игры и состязания на свежем воздухе\n🍽 Дегустация сибирской "
                "кухни\n\nПриглашаем тебя молодежь и всю твою семью провести незабываемый день в уникальном лесном "
                "комплексе Ягом!\nВход свободный.",
        reply_markup=get_back_button()
    )

@user_router.callback_query(F.data == 'draw')
async def about_festival(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIBA2Z1ZXwizmhqcBkUvG0U_jXedAFuAALE2jEbUfCoSwpMSP3ygDdFAQADAgADeQADNQQ",
        caption="29 июня на главной сцене «Ягома» будет проходить розыгрыш подарков среди присутствующих, "
             "не пропусти!\n\nГлавный приз – годовой запас пиццы от «До-До» и год интернета от «Метросети»\n\nА так же "
             "подарочные сертификаты от наших партнеров:\n\n1.Салон красоты «IDOL FACE»\n2.Салон красоты «Milana "
             "beauty»\n3.Студия красоты «LUXURY STUDIO»\n4.Шоурум «Аутфит»\n5.Dо4а\n6.Сибур\n7.Барбершоп «YUSUF»\n8.СК "
             "«STORM»\n9.Картинг «Югра Дрифт»\n10.Салон красоты «Хорошая девочка»\n11.Photolab "
             "фотостудия\n12.Боулинг-ресторан «Brooklyn Bowl»\n13.Центр проката КвадроМания Нижневартовск\n"
             "14.«Yumey Wear»",
        reply_markup=get_back_button()
    )


@user_router.callback_query(F.data == 'logistic')
async def logistic(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAM_ZnU3JZfmdcxrTR2UKnr79iAR-CUAApfZMRtR8KhLgPXsCd9sVV0BAAMCAAN5AAM1BA",
        caption="Лесной комплекс ЯГОМ расположен в районе Нижневартовского ГПЗ, на расстоянии 10 километров от "
                "памятника покорителям «Самотлора» и граничит с поймой реки Мысовая Мега. ЯГОМ внесен во многие "
                "навигаторы. До него легко добраться и найти.\n\nБолее подробная информация далее по ссылке\n\n"
                "https://vk.com/@-161303519-kak-do-nas-dobratsya",
        reply_markup=get_back_button()
    )


@user_router.callback_query(F.data == 'navigation')
async def navigation(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAILvGZzMrpuK5-JmKrjQK7S1F4c0xahAAK03zEbUD2YS2RDWHDZrnIcAQADAgADeQADNQQ",
        caption="Текст про карту",
        reply_markup=get_back_button()
    )


@user_router.callback_query(F.data == 'contact')
async def logistic(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIBAWZ1ZNxYh_WvbpLayubxZMa-n1KmAALC2jEbUfCoSwAB1Mk03E84WwEAAwIAA3kAAzUE",
        caption="Контакты: https://vk.com/molodnv",
        reply_markup=get_back_button()
    )


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
        photo="AgACAgIAAxkBAAIPVWZ1M_t-MVfxXaDyqe2boh7dpMKOAAJT2jEbZsOoS_XCeQogtAABGgEAAwIAA3kAAzUE"
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
            photo="AgACAgIAAxkBAAIPR2Z1MuSbgkk4IihIGRvQ4HzY3inNAAJA2jEbZsOoS76jl6Natsp5AQADAgADeQADNQQ",
            caption="В понедельник ждёт насыщенный день! С утра — зарядка и баскетбол для бодрости тела и духа. А "
                    "вечером погружение в мир искусства.",
            reply_markup=get_back_from_event_button()
        )
    if data == "25":
        await callback.message.answer_photo(
            caption="Вторник, 25 июня - день насыщенных мероприятий для всех!\n\nВеселые командные игры для всей семьи, "
                    "лаборатория настольных игр с опытными ведущими, «Мафия» для любителей интриг и молодежный "
                    "кинопоказ в арт-резиденции «Ядро».\n\nИ, конечно же,  выставка креативного туризма об уникальных "
                    "возможностях путешествий по Югре!\n\nПриходите, будет интересно!\n\n\n"
                    "На игру 'Мафия' вы сможете зарегистрироваться под постом* в группе:\nhttps://vk.com/siberianmafiaclub\n*пост с регистрацией выходит за сутки до мероприятия",
            photo="AgACAgIAAxkBAAIPSWZ1MxN_bn9nEmmaUAZDIf9HsmrJAAJB2jEbZsOoSyJgbYjSY8WoAQADAgADeQADNQQ",
            reply_markup=get_back_from_event_button()
        )
    if data == "26":
        await callback.message.answer_photo(
            photo="AgACAgIAAxkBAAIPS2Z1M0Ldh1bxxSogyLQ8FYNUK-5rAAJC2jEbZsOoSy8UER1vndYsAQADAgADeQADNQQ",
            caption="Сегодня начни день с игр на открытом воздухе, а после окунись в атмосферу творчества и свободны.",
            reply_markup=get_back_from_event_button()
        )
    if data == "27":
        await callback.message.answer_photo(
            photo="AgACAgIAAxkBAAIPTWZ1M2XuJApJAdmqF1f2eVpSfoGIAAJG2jEbZsOoS2dLlhvivIa8AQADAgADeQADNQQ",
            caption="Четверг это маленькая пятница\n\nПоэтому нужно повеселиться на фитджитал танцах, занять ум "
                    "шахматами и узнать кто же все таки «Мафия»\n\nОбратите внимание, что на мероприятия необходима регистрация!\n\n"
                    "Турнир по шахматам и фиджитал танцы:\nhttps://forms.gle/imypwf7hsmJ9Q6iv9\n\n"
                    "Посещение компьютерного клуба 'Cheek point':\nhttps://forms.gle/N8PetohDBntZQvrP6\n\n"
                    "На игру 'Мафия' вы сможете зарегистрироваться под постом* в группе:\nhttps://vk.com/siberianmafiaclub\n*пост с регистрацией выходит за сутки до мероприятия",
            reply_markup=get_back_from_event_button()
        )
    if data == "28":
        await callback.message.answer_photo(
            photo="AgACAgIAAxkBAAIPT2Z1M5njwSkecfY7CEAWZJbYHcIFAAJI2jEbZsOoS5Bv-Z1bTBTrAQADAgADeQADNQQ",
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
