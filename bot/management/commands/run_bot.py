# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
# import requests
# from django.core.management.base import BaseCommand
# from shop.models import Product  # Импорт модели продукта
# from asgiref.sync import sync_to_async  # Импорт для работы с sync_to_async
#
#
# API_URL = "http://127.0.0.1:8000/api/v1/"
# TOKEN = "8103377214:AAGWiMGzSo2FAY64h6T_zGMnohFAX72wbZ0"
#
# STEP_CATEGORY = "STEP_CATEGORY"
# STEP_SUBCATEGORY = "STEP_SUBCATEGORY"
# STEP_FILTERS = "STEP_FILTERS"
# STEP_SHOW_PRODUCTS = "STEP_SHOW_PRODUCTS"
#
# user_data = {}
#
#
# # Функция для получения ключей спецификаций
# async def get_spec_keys():
#     all_products = await sync_to_async(list)(Product.objects.all())  # Асинхронно получаем все продукты
#     spec_keys = set()
#     for product in all_products:
#         spec_keys.update(product.specifications.keys())  # Собираем все ключи спецификаций
#     return list(spec_keys)
#
# # Команда старт с кнопкой Начать для первого запуска
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_data.clear()  # Сброс состояния фильтров
#     keyboard = [[InlineKeyboardButton("Начать", callback_data="start")]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text(
#         "Добро пожаловать! Нажмите 'Начать', чтобы выбрать категорию или установить фильтры.",
#         reply_markup=reply_markup
#     )
#
# # Функция сброса фильтров с отдельной кнопкой
# async def reset_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_data.clear()  # Очистка состояния
#     keyboard = [[InlineKeyboardButton("Начать заново", callback_data="start")]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.callback_query.message.reply_text(
#         "Фильтры сброшены. Нажмите 'Начать заново', чтобы начать поиск.",
#         reply_markup=reply_markup
#     )
#
# # Запрашиваем категории у API и отправляем их пользователю
# async def send_categories(update: Update):
#     response = requests.get(API_URL + 'category/')
#     categories = response.json().get('objects', [])
#     keyboard = [[InlineKeyboardButton(cat['name'], callback_data=f"{STEP_SUBCATEGORY}_{cat['id']}")] for cat in categories]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.callback_query.message.reply_text("Выберите категорию:", reply_markup=reply_markup)
#
# # Обработчик подкатегорий
# async def send_subcategories(update: Update, context: ContextTypes.DEFAULT_TYPE, category_id):
#     response = requests.get(f"{API_URL}category/{category_id}/")
#     subcategories = response.json().get('subcategories', [])
#     keyboard = [[InlineKeyboardButton(subcat['name'], callback_data=f"{STEP_FILTERS}_{subcat['id']}")] for subcat in subcategories]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.callback_query.message.reply_text("Выберите подкатегорию:", reply_markup=reply_markup)
#
# # Обработчик фильтров с кнопками для «Пропустить» и «Готово»
# async def set_filters(update: Update, context: ContextTypes.DEFAULT_TYPE, subcategory_id):
#     user_data['subcategory_id'] = subcategory_id
#     keyboard = [[InlineKeyboardButton("Пропустить", callback_data="SKIP")]]
#     await update.callback_query.message.reply_text("Введите минимальную цену или нажмите 'Пропустить'.", reply_markup=InlineKeyboardMarkup(keyboard))
#     user_data['step'] = 'set_min_price'
#
# # Показываем доступные ключи спецификаций
# async def show_spec_keys(update: Update):
#     spec_keys = await get_spec_keys()  # Асинхронно получаем ключи спецификаций
#     keyboard = [[InlineKeyboardButton(key, callback_data=f"spec_{key}")] for key in spec_keys]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#
#     # Используем callback_query.message для отправки сообщения
#     if update.message:
#         await update.message.reply_text("Выберите спецификацию для фильтрации:", reply_markup=reply_markup)
#     elif update.callback_query:
#         await update.callback_query.message.reply_text("Выберите спецификацию для фильтрации:", reply_markup=reply_markup)
#
#
# # Обработка сообщений с кнопками «Пропустить» и «Готово»
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_text = update.message.text
#
#     if user_data.get('step') == 'set_min_price':
#         if user_text.isdigit():
#             user_data['price_min'] = int(user_text)
#         await update.message.reply_text("Введите максимальную цену или нажмите 'Пропустить'.", reply_markup=create_skip_done_keyboard())
#         user_data['step'] = 'set_max_price'
#
#     elif user_data.get('step') == 'set_max_price':
#         if user_text.isdigit():
#             user_data['price_max'] = int(user_text)
#         await update.message.reply_text("Введите бренд или нажмите 'Пропустить'.", reply_markup=create_skip_done_keyboard())
#         user_data['step'] = 'set_brand'
#
#     elif user_data.get('step') == 'set_brand':
#         if user_text.lower() != 'пропустить':
#             user_data['brand'] = user_text
#         await show_spec_keys(update)  # Переход к выбору спецификаций
#
#     elif user_data.get('step') == 'set_spec_value':
#         selected_key = user_data.get('selected_spec_key')
#         if selected_key:
#             user_data.setdefault('specifications', {})[f"spec_{selected_key}"] = user_text
#             await update.message.reply_text("Спецификация добавлена. Выберите следующую спецификацию или нажмите 'Готово'.", reply_markup=create_skip_done_keyboard())
#             await show_spec_keys(update)  # Показываем клавиатуру спецификаций снова
#         else:
#             await update.message.reply_text("Произошла ошибка, выберите спецификацию.")
#
# # Запрос и отображение продуктов
# async def send_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     subcategory_id = user_data['subcategory_id']
#     filters = {
#         "category": subcategory_id,
#         "price_min": user_data.get("price_min"),
#         "price_max": user_data.get("price_max"),
#         "brand": user_data.get("brand"),
#     }
#     filters.update(user_data.get("specifications", {}))
#
#     print(f"Запрос к API с URL: {API_URL + 'products/'} и параметрами: {filters}")
#
#     response = requests.get(API_URL + 'products/', params=filters)
#
#     if response.status_code != 200:
#         reply_text = "Произошла ошибка при получении продуктов. Пожалуйста, попробуйте снова."
#         await update.callback_query.message.reply_text(reply_text)
#         return
#
#     products = response.json().get('objects', [])
#     if products:
#         for product in products[:10]:  # Показываем первые 10 товаров
#             await update.callback_query.message.reply_text(f"{product['name']} — {product['price']} руб.")
#         await update.callback_query.message.reply_text("Отправьте 'Следующие 10', чтобы увидеть больше товаров.")
#         user_data['step'] = STEP_SHOW_PRODUCTS
#     else:
#         await update.callback_query.message.reply_text("Товары не найдены по заданным фильтрам.")
#
# # Обработчик кнопок
# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#
#     # Обработка нажатия на кнопку "Начать"
#     if query.data == "start":
#         await send_categories(update)
#         return
#
#     # Проверка на кнопки "Пропустить" и "Готово"
#     if query.data == "SKIP":
#         current_step = user_data.get('step')
#         if current_step == 'set_min_price':
#             user_data['price_min'] = None
#             await query.message.reply_text("Введите максимальную цену или нажмите 'Пропустить'.", reply_markup=create_skip_done_keyboard())
#             user_data['step'] = 'set_max_price'
#         elif current_step == 'set_max_price':
#             user_data['price_max'] = None
#             await query.message.reply_text("Введите бренд или нажмите 'Пропустить'.", reply_markup=create_skip_done_keyboard())
#             user_data['step'] = 'set_brand'
#         elif current_step == 'set_brand':
#             user_data['brand'] = None
#             await show_spec_keys(update)  # Переход к выбору спецификаций
#         return
#
#     if query.data == "DONE":
#         await send_products(update, context)
#         return
#
#     # Обработка выбора спецификаций
#     if query.data.startswith("spec_"):
#         selected_key = query.data.split("spec_")[1]
#         user_data['selected_spec_key'] = selected_key
#         await query.message.reply_text(f"Введите значение для спецификации '{selected_key}':")
#         user_data['step'] = 'set_spec_value'
#         return
#
#     # Обработка шагов по категориям и подкатегориям
#     *step_parts, entity_id = query.data.split("_")
#     step = "_".join(step_parts)
#
#     if step == "STEP_SUBCATEGORY":
#         await send_subcategories(update, context, entity_id)
#     elif step == "STEP_FILTERS":
#         await set_filters(update, context, entity_id)
#     else:
#         await query.message.reply_text("Произошла ошибка: неизвестный шаг.")
#
# # Клавиатура с кнопками «Пропустить», «Готово», «Сбросить»
# def create_skip_done_keyboard():
#     return InlineKeyboardMarkup([
#         [InlineKeyboardButton("Пропустить", callback_data="SKIP")],
#         [InlineKeyboardButton("Готово", callback_data="DONE")],
#         [InlineKeyboardButton("Сбросить", callback_data="reset")]
#     ])
#
# # Основная функция запуска бота
# def main():
#     application = Application.builder().token(TOKEN).build()
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CallbackQueryHandler(button_handler))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#
#     print("Бот успешно запущен и ожидает запросов...")
#     application.run_polling()
#
# class Command(BaseCommand):
#     help = 'Запускает Telegram-бота'
#
#     def handle(self, *args, **kwargs):
#         self.stdout.write(self.style.SUCCESS("Запуск бота..."))
#         main()
#
#
#
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import requests
from django.core.management.base import BaseCommand
from shop.models import Product  # Импорт модели продукта
from asgiref.sync import sync_to_async  # Импорт для работы с sync_to_async


API_URL = "http://127.0.0.1:8000/api/v1/"
TOKEN = "8103377214:AAGWiMGzSo2FAY64h6T_zGMnohFAX72wbZ0"

STEP_CATEGORY = "STEP_CATEGORY"
STEP_SUBCATEGORY = "STEP_SUBCATEGORY"
STEP_FILTERS = "STEP_FILTERS"
STEP_SHOW_PRODUCTS = "STEP_SHOW_PRODUCTS"

user_data = {}


# Функция для получения ключей спецификаций
async def get_spec_keys(subcategory_id):
    response = requests.get(f"{API_URL}specifications/{subcategory_id}/")
    spec_keys = response.json().get('spec_keys', [])
    return spec_keys


# Команда старт с кнопкой Начать для первого запуска
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data.clear()  # Сброс состояния фильтров
    keyboard = [[InlineKeyboardButton("Начать", callback_data="start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать! Нажмите 'Начать', чтобы выбрать категорию или установить фильтры.",
        reply_markup=reply_markup
    )

# Функция сброса фильтров с отдельной кнопкой
async def reset_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data.clear()  # Очистка состояния
    keyboard = [[InlineKeyboardButton("Начать заново", callback_data="start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        "Фильтры сброшены. Нажмите 'Начать заново', чтобы начать поиск.",
        reply_markup=reply_markup
    )

# Запрашиваем категории у API и отправляем их пользователю
async def send_categories(update: Update):
    response = requests.get(API_URL + 'category/')
    categories = response.json().get('objects', [])
    keyboard = [[InlineKeyboardButton(cat['name'], callback_data=f"{STEP_SUBCATEGORY}_{cat['id']}")] for cat in categories]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Выберите категорию:", reply_markup=reply_markup)

# Обработчик подкатегорий
async def send_subcategories(update: Update, context: ContextTypes.DEFAULT_TYPE, category_id):
    response = requests.get(f"{API_URL}category/{category_id}/")
    subcategories = response.json().get('subcategories', [])
    keyboard = [[InlineKeyboardButton(subcat['name'], callback_data=f"{STEP_FILTERS}_{subcat['id']}")] for subcat in subcategories]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Выберите подкатегорию:", reply_markup=reply_markup)

# Обработчик фильтров с кнопками для «Пропустить» и «Готово»
async def set_filters(update: Update, context: ContextTypes.DEFAULT_TYPE, subcategory_id):
    user_data['subcategory_id'] = subcategory_id
    keyboard = [[InlineKeyboardButton("Пропустить", callback_data="SKIP")]]
    await update.callback_query.message.reply_text("Введите минимальную цену или нажмите 'Пропустить'.", reply_markup=InlineKeyboardMarkup(keyboard))
    user_data['step'] = 'set_min_price'
    await show_spec_keys(update, subcategory_id=subcategory_id)



# Показываем доступные ключи спецификаций
async def show_spec_keys(update: Update, subcategory_id):
    try:
        spec_keys = await get_spec_keys(subcategory_id)
    except requests.exceptions.JSONDecodeError:
        await update.callback_query.message.reply_text("Ошибка загрузки спецификаций.")
        return

    keyboard = [[InlineKeyboardButton(key, callback_data=f"spec_{key}")] for key in spec_keys]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Используем callback_query.message для отправки сообщения
    if update.message:
        await update.message.reply_text("Выберите спецификацию для фильтрации:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text("Выберите спецификацию для фильтрации:", reply_markup=reply_markup)


# Обработка сообщений с кнопками «Пропустить» и «Готово»
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if user_data.get('step') == 'set_min_price':
        if user_text.isdigit():
            user_data['price_min'] = int(user_text)
        await update.message.reply_text("Введите максимальную цену или нажмите 'Пропустить'.", reply_markup=create_skip_done_keyboard())
        user_data['step'] = 'set_max_price'

    elif user_data.get('step') == 'set_max_price':
        if user_text.isdigit():
            user_data['price_max'] = int(user_text)
        await update.message.reply_text("Введите бренд или нажмите 'Пропустить'.", reply_markup=create_skip_done_keyboard())
        user_data['step'] = 'set_brand'

    elif user_data.get('step') == 'set_brand':
        if user_text.lower() != 'пропустить':
            user_data['brand'] = user_text
        await show_spec_keys(update)  # Переход к выбору спецификаций

    elif user_data.get('step') == 'set_spec_value':
        selected_key = user_data.get('selected_spec_key')
        if selected_key:
            user_data.setdefault('specifications', {})[f"spec_{selected_key}"] = user_text
            await update.message.reply_text("Спецификация добавлена. Выберите следующую спецификацию или нажмите 'Готово'.", reply_markup=create_skip_done_keyboard())
            await show_spec_keys(update)  # Показываем клавиатуру спецификаций снова
        else:
            await update.message.reply_text("Произошла ошибка, выберите спецификацию.")

# Запрос и отображение продуктов
async def send_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subcategory_id = user_data['subcategory_id']
    filters = {
        "category": subcategory_id,
        "price_min": user_data.get("price_min"),
        "price_max": user_data.get("price_max"),
        "brand": user_data.get("brand"),
    }
    filters.update(user_data.get("specifications", {}))

    print(f"Запрос к API с URL: {API_URL + 'products/'} и параметрами: {filters}")

    response = requests.get(API_URL + 'products/', params=filters)

    if response.status_code != 200:
        reply_text = "Произошла ошибка при получении продуктов. Пожалуйста, попробуйте снова."
        await update.callback_query.message.reply_text(reply_text)
        return

    products = response.json().get('objects', [])
    if products:
        for product in products[:10]:  # Показываем первые 10 товаров
            await update.callback_query.message.reply_text(f"{product['name']} — {product['price']} руб.")
        await update.callback_query.message.reply_text("Отправьте 'Следующие 10', чтобы увидеть больше товаров.")
        user_data['step'] = STEP_SHOW_PRODUCTS
    else:
        await update.callback_query.message.reply_text("Товары не найдены по заданным фильтрам.")

# Обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()


    # Обработка нажатия на кнопку "Начать"
    if query.data == "start":
        await send_categories(update)
        return

    # Проверка на кнопки "Пропустить" и "Готово"
    if query.data == "SKIP":
        current_step = user_data.get('step')
        if current_step == 'set_min_price':
            user_data['price_min'] = None
            await query.message.reply_text("Введите максимальную цену или нажмите 'Пропустить'.", reply_markup=create_skip_done_keyboard())
            user_data['step'] = 'set_max_price'
        elif current_step == 'set_max_price':
            user_data['price_max'] = None
            await query.message.reply_text("Введите бренд или нажмите 'Пропустить'.", reply_markup=create_skip_done_keyboard())
            user_data['step'] = 'set_brand'
        elif current_step == 'set_brand':
            user_data['brand'] = None
            await show_spec_keys(update)  # Переход к выбору спецификаций
        return

    if query.data == "DONE":
        await send_products(update, context)
        return

    # Обработка выбора спецификаций
    if query.data.startswith("spec_"):
        selected_key = query.data.split("spec_")[1]
        user_data['selected_spec_key'] = selected_key
        await query.message.reply_text(f"Введите значение для спецификации '{selected_key}':")
        user_data['step'] = 'set_spec_value'
        return

    # Обработка шагов по категориям и подкатегориям
    *step_parts, entity_id = query.data.split("_")
    step = "_".join(step_parts)

    if step == "STEP_SUBCATEGORY":
        await send_subcategories(update, context, entity_id)
    elif step == "STEP_FILTERS":
        await set_filters(update, context, entity_id)
    else:
        await query.message.reply_text("Произошла ошибка: неизвестный шаг.")

    await show_spec_keys(update, entity_id)



# Клавиатура с кнопками «Пропустить», «Готово», «Сбросить»
def create_skip_done_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Пропустить", callback_data="SKIP")],
        [InlineKeyboardButton("Готово", callback_data="DONE")],
        [InlineKeyboardButton("Сбросить", callback_data="reset")]
    ])

# Основная функция запуска бота
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот успешно запущен и ожидает запросов...")
    application.run_polling()

class Command(BaseCommand):
    help = 'Запускает Telegram-бота'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Запуск бота..."))
        main()



