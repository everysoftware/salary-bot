from aiogram import Router, types
from aiogram.filters import CommandStart

from src.db import aggregate_payments
from src.schemes import SRequest

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Hello! I'm a salary bot!")


@router.message()
async def process(message: types.Message):
    try:
        request = SRequest.model_validate_json(message.text)

        await message.answer(aggregate_payments(request).model_dump_json())
    except ValueError:
        await message.answer("Invalid request")
