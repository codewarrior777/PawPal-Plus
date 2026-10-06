from datetime import date
import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


@pytest.fixture
def today():
    return date.today()


def test_mark_complete_changes_status(today):
    task = Task("Morning Walk", "08:00", today)
    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_add_task_increases_count(today):
    pet = Pet("Cooper", "Dog", 4)
    assert len(pet.get_tasks()) == 0

    task = Task("Morning Walk", "08:00", today)
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1


def test_get_incomplete_tasks_filters_correctly(today):
    pet = Pet("Cooper", "Dog", 4)
    task1 = Task("Morning Walk", "08:00", today)
    task2 = Task("Evening Walk", "18:00", today)

    pet.add_task(task1)
    pet.add_task(task2)

    task1.mark_complete()

    incomplete = pet.get_incomplete_tasks()
    assert len(incomplete) == 1
    assert incomplete[0] == task2


def test_owner_get_all_tasks_combines_pets(today):
    owner = Owner("Alex")
    cooper = Pet("Cooper", "Dog", 4)
    prince = Pet("Prince", "Cat", 2)

    task1 = Task("Walk Cooper", "08:00", today)
    task2 = Task("Feed Prince", "08:30", today)

    cooper.add_task(task1)
    prince.add_task(task2)

    owner.add_pet(cooper)
    owner.add_pet(prince)

    all_tasks = owner.get_all_tasks()
    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks


def test_scheduler_sort_by_time(today):
    scheduler = Scheduler()
    task1 = Task("Evening Feed", "18:00", today)
    task2 = Task("Morning Walk", "07:00", today)
    task3 = Task("Lunch Snack", "12:00", today)

    tasks = [task1, task2, task3]
    sorted_tasks = scheduler.sort_by_time(tasks)

    assert sorted_tasks == [task2, task3, task1]


def test_scheduler_detect_conflicts(today):
    scheduler = Scheduler()
    task1 = Task("Walk Cooper", "08:00", today)
    task2 = Task("Feed Prince", "08:00", today)
    task3 = Task("Vet Visit", "14:00", today)

    tasks = [task1, task2, task3]
    conflicts = scheduler.detect_conflicts(tasks)

    assert len(conflicts) == 1
    assert conflicts[0] == (task1, task2)