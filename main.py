"""CLI demo for PawPal+ showing sorting, filtering, conflicts, and recurrence.

Uses the `tabulate` library for structured ASCII tables.
"""

from datetime import date

from tabulate import tabulate

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    # Initialize Scheduler
    scheduler = Scheduler()

    # 1. Create Owner
    owner = Owner(name="Alex")

    # 2. Create Pets
    cooper = Pet(name="Cooper", species="Dog", age=4)
    prince = Pet(name="Prince", species="Cat", age=2)

    # 3. Add Pets to Owner
    owner.add_pet(cooper)
    owner.add_pet(prince)

    # 4. Create Tasks
    today = date.today()

    task1 = Task(
        description="Morning walk",
        time="07:00",
        due_date=today,
        frequency="daily",
    )
    task2 = Task(
        description="Feed breakfast",
        time="08:00",
        due_date=today,
        frequency="daily",
    )
    task3 = Task(
        description="Playtime",
        time="08:00",
        due_date=today,
        frequency="daily",
    )
    task4 = Task(
        description="Vet appointment",
        time="14:00",
        due_date=today,
        frequency="once",
    )

    # Mark one task complete to test completion filtering
    task1.mark_complete()

    # 5. Add Tasks to Pets
    cooper.add_task(task1)
    prince.add_task(task2)
    cooper.add_task(task3)
    cooper.add_task(task4)

    print("=" * 60)
    print(f"🐾 WELCOME TO PAWPAL+ DEMO | Owner: {owner.name} 🐾")
    print("=" * 60)

    # Gather all tasks across pets
    all_tasks = owner.get_all_tasks()

    # Helper: map each task to its pet's name
    def pet_for(task: Task) -> str:
        for pet in owner.pets:
            if task in pet.tasks:
                return pet.name
        return "Unknown"

    # ------------------------------------------------------------------
    # Feature 1: Sorted Schedule (tabulate table)
    # ------------------------------------------------------------------
    print("\n📅 TODAY'S SCHEDULE (Sorted by Time)\n")
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    schedule_rows = [
        [
            t.time,
            t.description,
            pet_for(t),
            t.frequency,
            "✅ Done" if t.completed else "⏳ Pending",
        ]
        for t in sorted_tasks
    ]
    print(
        tabulate(
            schedule_rows,
            headers=["Time", "Task", "Pet", "Frequency", "Status"],
            tablefmt="fancy_grid",
        )
    )

    # ------------------------------------------------------------------
    # Feature 2: Incomplete Tasks
    # ------------------------------------------------------------------
    print("\n⏳ INCOMPLETE TASKS\n")
    incomplete = scheduler.filter_by_completion(all_tasks, completed=False)
    incomplete_rows = [
        [t.time, t.description, pet_for(t)] for t in incomplete
    ]
    print(
        tabulate(
            incomplete_rows,
            headers=["Time", "Task", "Pet"],
            tablefmt="fancy_grid",
        )
    )

    # ------------------------------------------------------------------
    # Feature 3: Schedule Conflicts
    # ------------------------------------------------------------------
    print("\n⚠️  CONFLICTS DETECTED\n")
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        conflict_rows = [
            [t1.time, t1.description, pet_for(t1), t2.description, pet_for(t2)]
            for t1, t2 in conflicts
        ]
        print(
            tabulate(
                conflict_rows,
                headers=["Time", "Task A", "Pet A", "Task B", "Pet B"],
                tablefmt="fancy_grid",
            )
        )
    else:
        print("  ✅ No schedule conflicts detected!")

    # ------------------------------------------------------------------
    # Feature 4: Filter Tasks by Pet Name
    # ------------------------------------------------------------------
    print("\n🐶 COOPER'S TASKS\n")
    coopers_tasks = scheduler.filter_by_pet_name(owner, "Cooper")
    cooper_rows = [
        [t.time, t.description, "✅" if t.completed else "❌"]
        for t in coopers_tasks
    ]
    print(
        tabulate(
            cooper_rows,
            headers=["Time", "Task", "Done?"],
            tablefmt="fancy_grid",
        )
    )

    # ------------------------------------------------------------------
    # Feature 5: Demo Recurring Task Handler
    # ------------------------------------------------------------------
    print("\n🔄 RECURRING TASK GENERATION\n")
    next_walk = scheduler.handle_recurring(task1)
    if next_walk:
        recurring_rows = [
            ["Original", task1.description, str(task1.due_date)],
            ["Next Due", next_walk.description, str(next_walk.due_date)],
        ]
        print(
            tabulate(
                recurring_rows,
                headers=["", "Task", "Due Date"],
                tablefmt="fancy_grid",
            )
        )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()