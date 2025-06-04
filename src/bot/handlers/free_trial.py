from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Const, Format
from loguru import logger

from src.database import db
from src.database.models import TrialWorkout
from src.services.free_trial import FreeTrialService


class TrialWorkoutStates(StatesGroup):
    list_workouts = State()
    show_workout = State()


# Getters
async def get_workouts_data(dialog_manager: DialogManager, **kwargs):
    async with db.session() as session:
        service = FreeTrialService(session)
        workouts = await service.get_trial_workouts()
        return {
            "workouts": [
                (work.position,) for work in workouts
            ]
        }


async def get_workout_data(dialog_manager: DialogManager, **kwargs):
    selected_workout_id = dialog_manager.dialog_data.get("selected_workout_id")
    if not selected_workout_id:
        logger.error(
            f"Trial workout with {selected_workout_id=} not found. Data: "
            f"{dialog_manager.dialog_data}"
        )
        return {}

    async with db.session() as session:
        service = FreeTrialService(session)
        workout: TrialWorkout = await service.get_trial_workout_by_position(selected_workout_id)
        if workout:
            return {"workout_desc": workout.description}

    logger.error(
        f"Trial workout with {selected_workout_id=} not found. Data: {dialog_manager.dialog_data}"
    )
    return None


# Handlers
async def on_workout_selected(
    callback: CallbackQuery,
    widget: Select,
    dialog_manager: DialogManager,
    workout_id: str,
):
    dialog_manager.dialog_data["selected_workout_id"] = int(workout_id)
    await dialog_manager.switch_to(TrialWorkoutStates.show_workout)


async def back_to_workouts_list(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(TrialWorkoutStates.list_workouts)


# Windows
workout_list_window = Window(
    Const("Выбирай пробную тренирвку + ОБЩАЯ ИСТРУКЦИЯ ТУТ "),
    Select(
        Format("Тренировка №{item[0]}"),
        id="select_trial_workout",
        item_id_getter=lambda item: item[0],
        items="workouts",
        on_click=on_workout_selected,
    ),
    state=TrialWorkoutStates.list_workouts,
    getter=get_workouts_data,
)

chosen_workout_window = Window(
    Format("Тут начинается опиисание:\n\n{workout_desc}"),
    Button(Const("⬅️ Назад к списку"), id="back_to_workouts_list", on_click=back_to_workouts_list),
    state=TrialWorkoutStates.show_workout,
    getter=get_workout_data,
)

free_trial_dialog = Dialog(workout_list_window, chosen_workout_window)
free_trial_router = Router()


@free_trial_router.callback_query(F.data == "trial_week")
async def choose_trial_week(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(TrialWorkoutStates.list_workouts, mode=StartMode.RESET_STACK)
    await callback.answer()
