from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler


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

    print("==================================================")
    print(f"🐾 WELCOME TO PAWPAL+ DEMO | Owner: {owner.name} 🐾")
    print("==================================================\n")

    # Gather all tasks across pets
    all_tasks = owner.get_all_tasks()

    # --- Feature 1: Sorted Schedule ---
    print("📅 TODAY'S SCHEDULE (Sorted by Time)")
    print("--------------------------------------------------")
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    for task in sorted_tasks:
        status = "✅ Done" if task.completed else "⏳ Pending"
        print(f"  • [{task.time}] {task.description:<20} ({status})")
    print()

    # --- Feature 2: Incomplete Tasks ---
    print("⏳ INCOMPLETE TASKS")
    print("--------------------------------------------------")
    incomplete = scheduler.filter_by_completion(all_tasks, completed=False)
    for task in incomplete:
        print(f"  • [{task.time}] {task.description}")
    print()

    # --- Feature 3: Schedule Conflicts ---
    print("⚠️ CONFLICTS DETECTED")
    print("--------------------------------------------------")
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        for t1, t2 in conflicts:
            print(f"  🚨 Time Collision at {t1.time}:")
            print(f"     - {t1.description}")
            print(f"     - {t2.description}")
    else:
        print("  No schedule conflicts detected!")
    print()

    # --- Feature 4: Filter Tasks by Pet Name ---
    print("🐶 COOPER'S TASKS")
    print("--------------------------------------------------")
    coopers_tasks = scheduler.filter_by_pet_name(owner, "Cooper")
    for task in coopers_tasks:
        status = "✅" if task.completed else "❌"
        print(f"  • {status} [{task.time}] {task.description}")
    print()

    # --- Feature 5: Demo Recurring Task Handler ---
    print("🔄 RECURRING TASK GENERATION")
    print("--------------------------------------------------")
    next_walk = scheduler.handle_recurring(task1)
    if next_walk:
        print(f"  Original: {task1.description} on {task1.due_date}")
        print(f"  Next Due: {next_walk.description} on {next_walk.due_date}")
    print("\n==================================================")


if __name__ == "__main__":
    main()