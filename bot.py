import asyncio
import logging
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    InlineKeyboardButton,
    FSInputFile
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Загружаем переменные окружения
load_dotenv()

# ======================================================
# НАСТРОЙКИ
# ======================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "8374022888:AAGoZoIoMYPkyAOJy4nYVUPWUUb32Xw5mMY")

FUNPAY_URL = "https://funpay.com/users/17089244/"
CHANNEL_URL = "https://t.me/gift_hub_crypto"
SUPPORT_URL = "https://t.me/muffinn_2"

# Локальная картинка
BANNER_PATH = "banner.jpg"

# ======================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ======================================================
# ПАКЕТЫ
# ======================================================

PACKAGES = {
    "p50":   ("50",   "157 ₽",   "45 ₴",    "1.82 €",  "0.25 TON"),
    "p100":  ("100",  "209 ₽",   "80 ₴",    "2.43 €",  "0.45 TON"),
    "p250":  ("250",  "522 ₽",   "175 ₴",   "6.06 €",  "1.0 TON"),
    "p500":  ("500",  "940 ₽",   "330 ₴",   "10.91 €", "1.9 TON"),
    "p1000": ("1000", "1775 ₽",  "620 ₴",   "20.62 €", "3.5 TON"),
    "p2500": ("2500", "3299 ₽",  "1450 ₴",  "31.9 €",  "8.2 TON"),
    "p5000": ("5000", "6299 ₽",  "2780 ₴",  "60.9 €",  "15.5 TON"),
}

# ======================================================
# КНОПКИ
# ======================================================

def kb_main():
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(
            text="⭐ Купить Stars",
            callback_data="buy"
        )
    )

    kb.row(
        InlineKeyboardButton(
            text="💰 Цены",
            callback_data="prices"
        ),

        InlineKeyboardButton(
            text="🌍 Оплата",
            callback_data="payment"
        )
    )

    kb.row(
        InlineKeyboardButton(
            text="❓ Как купить",
            callback_data="how"
        ),

        InlineKeyboardButton(
            text="⭐ Отзывы",
            callback_data="reviews"
        )
    )

    kb.row(
        InlineKeyboardButton(
            text="📢 Канал",
            url=CHANNEL_URL
        ),

        InlineKeyboardButton(
            text="🛠 Поддержка",
            url=SUPPORT_URL
        )
    )

    return kb.as_markup()


def kb_packages():
    kb = InlineKeyboardBuilder()

    for key, data in PACKAGES.items():
        amount = data[0]

        kb.row(
            InlineKeyboardButton(
                text=f"⭐ {amount} Stars",
                callback_data=key
            )
        )

    kb.row(
        InlineKeyboardButton(
            text="✏️ Свое количество",
            callback_data="custom"
        )
    )

    kb.row(
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="main"
        )
    )

    return kb.as_markup()


def kb_order():
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(
            text="🛒 Купить на FunPay",
            url=FUNPAY_URL
        )
    )

    kb.row(
        InlineKeyboardButton(
            text="💬 Написать продавцу",
            url=SUPPORT_URL
        )
    )

    kb.row(
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="buy"
        )
    )

    return kb.as_markup()


def kb_back():
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(
            text="◀️ Главное меню",
            callback_data="main"
        )
    )

    return kb.as_markup()

# ======================================================
# ТЕКСТЫ
# ======================================================

def txt_main(name):

    return (
        f"👋 <b>Добро пожаловать, {name}!</b>\n\n"

        "⭐ Продажа Telegram Stars\n"
        "⚡ Быстрая выдача\n"
        "🔒 Безопасная покупка\n\n"

        "━━━━━━━━━━━━━━━\n"
        "✅ Выдача 5–15 минут\n"
        "✅ Лучшие цены\n"
        "✅ Оплата ₽ ₴ € TON\n"
        "✅ Надежный продавец\n"
        "━━━━━━━━━━━━━━━\n\n"

        "💫 Выберите нужный раздел ниже"
    )


TXT_PRICES = (
    "💰 <b>АКТУАЛЬНЫЕ ЦЕНЫ</b>\n\n"

    "⭐ 50 Stars — 157 ₽\n"
    "⭐ 100 Stars — 209 ₽\n"
    "⭐ 250 Stars — 522 ₽\n"
    "⭐ 500 Stars — 940 ₽\n"
    "⭐ 1000 Stars — 1775 ₽\n"
    "⭐ 2500 Stars — 3299 ₽\n"
    "⭐ 5000 Stars — 6299 ₽\n\n"

    "━━━━━━━━━━━━━━━\n"
    "💎 Доступна оплата:\n"
    "₽ / ₴ / € / TON / USDT"
)


TXT_PAYMENT = (
    "🌍 <b>СПОСОБЫ ОПЛАТЫ</b>\n\n"

    "🇺🇦 <b>Гривны (₴)</b>\n"
    "• PrivatBank\n"
    "• Monobank\n\n"

    "🇷🇺 <b>Рубли (₽)</b>\n"
    "• FunPay\n"
    "• Банковские карты РФ\n\n"

    "💶 <b>Евро (€)</b>\n"
    "• Оплата через FunPay\n\n"

    "💎 <b>TON / USDT</b>\n"
    "• TON Wallet\n"
    "• CryptoBot\n"
    "• Любой криптокошелек\n\n"

    "━━━━━━━━━━━━━━━\n"
    "⚡ Stars приходят\n"
    "в течение 5–15 минут"
)


TXT_HOW = (
    "❓ <b>КАК КУПИТЬ STARS?</b>\n\n"

    "1️⃣ Выберите пакет\n"
    "2️⃣ Нажмите купить\n"
    "3️⃣ Оплатите заказ\n"
    "4️⃣ Отправьте @username\n"
    "5️⃣ Получите Stars ⭐\n\n"

    "⏱ Среднее время выдачи:\n"
    "<b>5–15 минут</b>"
)


TXT_REVIEWS = (
    "⭐ <b>ОТЗЫВЫ ПОКУПАТЕЛЕЙ</b>\n\n"

    "⭐⭐⭐⭐⭐\n"
    "«Пришло за 5 минут»\n\n"

    "⭐⭐⭐⭐⭐\n"
    "«Лучшие цены, беру постоянно»\n\n"

    "⭐⭐⭐⭐⭐\n"
    "«Оплатил TON — выдали моментально»"
)


TXT_CUSTOM = (
    "✏️ <b>СВОЕ КОЛИЧЕСТВО</b>\n\n"

    "Нужен индивидуальный заказ?\n\n"

    "📩 Напишите продавцу:\n"
    "@muffinn_2\n\n"

    "💎 Оптовые цены доступны"
)

# ======================================================
# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ
# ======================================================

async def edit_message(callback, text, keyboard):

    if callback.message.photo:

        await callback.message.edit_caption(
            caption=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    else:

        await callback.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

# ======================================================
# START
# ======================================================

@dp.message(CommandStart())
@dp.message(Command("menu"))
async def start(message: types.Message):

    photo = FSInputFile(BANNER_PATH)

    await message.answer_photo(
        photo=photo,
        caption=txt_main(message.from_user.first_name),
        parse_mode="HTML",
        reply_markup=kb_main()
    )

# ======================================================
# ГЛАВНОЕ МЕНЮ
# ======================================================

@dp.callback_query(F.data == "main")
async def main_menu(callback: types.CallbackQuery):

    await callback.message.delete()

    photo = FSInputFile(BANNER_PATH)

    await callback.message.answer_photo(
        photo=photo,
        caption=txt_main(callback.from_user.first_name),
        parse_mode="HTML",
        reply_markup=kb_main()
    )

    await callback.answer()

# ======================================================
# КУПИТЬ
# ======================================================

@dp.callback_query(F.data == "buy")
async def buy(callback: types.CallbackQuery):

    text = (
        "⭐ <b>ВЫБЕРИТЕ ПАКЕТ</b>\n\n"

        "Выберите нужное количество Stars 👇\n\n"

        "💡 Чем больше пакет — тем выгоднее"
    )

    await edit_message(
        callback,
        text,
        kb_packages()
    )

    await callback.answer()

# ======================================================
# ТЕКСТ ПАКЕТА
# ======================================================

def package_text(amount, rub, uah, eur, ton):

    return (
        f"⭐ <b>{amount} Telegram Stars</b>\n\n"

        f"🇷🇺 {rub}\n"
        f"🇺🇦 {uah}\n"
        f"💶 {eur}\n"
        f"💎 {ton}\n\n"

        "━━━━━━━━━━━━━━━\n"

        "⚡ Выдача 5–15 минут\n"
        "🔒 Безопасная покупка\n"
        "⭐ Гарантия получения\n\n"

        "📩 После оплаты отправьте\n"
        "свой Telegram username"
    )

# ======================================================
# ОБРАБОТКА ПАКЕТОВ
# ======================================================

@dp.callback_query(F.data.in_(PACKAGES.keys()))
async def package_handler(callback: types.CallbackQuery):

    amount, rub, uah, eur, ton = PACKAGES[callback.data]

    await edit_message(
        callback,
        package_text(amount, rub, uah, eur, ton),
        kb_order()
    )

    await callback.answer()

# ======================================================
# ЦЕНЫ
# ======================================================

@dp.callback_query(F.data == "prices")
async def prices(callback: types.CallbackQuery):

    await edit_message(
        callback,
        TXT_PRICES,
        kb_back()
    )

    await callback.answer()

# ======================================================
# ОПЛАТА
# ======================================================

@dp.callback_query(F.data == "payment")
async def payment(callback: types.CallbackQuery):

    await edit_message(
        callback,
        TXT_PAYMENT,
        kb_back()
    )

    await callback.answer()

# ======================================================
# КАК КУПИТЬ
# ======================================================

@dp.callback_query(F.data == "how")
async def how(callback: types.CallbackQuery):

    await edit_message(
        callback,
        TXT_HOW,
        kb_back()
    )

    await callback.answer()

# ======================================================
# ОТЗЫВЫ
# ======================================================

@dp.callback_query(F.data == "reviews")
async def reviews(callback: types.CallbackQuery):

    await edit_message(
        callback,
        TXT_REVIEWS,
        kb_back()
    )

    await callback.answer()

# ======================================================
# СВОЕ КОЛИЧЕСТВО
# ======================================================

@dp.callback_query(F.data == "custom")
async def custom(callback: types.CallbackQuery):

    await edit_message(
        callback,
        TXT_CUSTOM,
        kb_order()
    )

    await callback.answer()

# ======================================================
# ЗАПУСК БОТА
# ======================================================

# ======================================================
# ЗАПУСК БОТА
# ======================================================

async def main():
    """
    Основной цикл работы бота с автоматическим переподключением (24/7)
    """
    retry_count = 0
    max_retries = 5
    base_delay = 5  # секунд
    
    logger.info("=" * 50)
    logger.info("🚀 TELEGRAM BOT STARTED - 24/7 MODE")
    logger.info("=" * 50)
    
    while True:
        try:
            logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Подключение к Telegram...")
            retry_count = 0
            
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
            
        except KeyboardInterrupt:
            logger.info("✋ Bot остановлен пользователем")
            await bot.session.close()
            break
            
        except asyncio.CancelledError:
            logger.warning(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Polling отменен")
            await asyncio.sleep(5)
            continue
            
        except Exception as error:
            retry_count += 1
            delay = min(base_delay * (2 ** retry_count), 300)  # макс 5 минут
            
            logger.error(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Ошибка: {error}\n"
                f"Попытка переподключения {retry_count}/{max_retries}. "
                f"Ждем {delay} сек..."
            )
            
            if retry_count >= max_retries:
                logger.warning(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Достигнут лимит попыток. Сброс счетчика..."
                )
                retry_count = 0
            
            try:
                await bot.session.close()
            except:
                pass
            
            await asyncio.sleep(delay)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("❌ Программа завершена")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"💥 Критическая ошибка: {e}")
        sys.exit(1)