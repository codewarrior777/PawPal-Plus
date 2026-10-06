"""Streamlit UI for PawPal+ — the smart pet care management system."""

from datetime import date

import streamlit as st

from pawpal_system import (
    Owner,
    Pet,
    Scheduler,
    Task,
    load_owner_from_json,
    save_owner_to_json,
)


def _get_or_create_owner() -> Owner:
    """
    Return the current Owner from session state.

    If none exists yet, attempt to load one from data.json.
    If data.json is missing, return an empty Owner with a placeholder name
    so the onboarding UI can prompt for the real name.
    """
    if "owner" not in st.session_state:
        st.session_state.owner = load_owner_from_json("data.json")
    return st.session_state.owner


def _is_onboarded(owner: Owner) -> bool:
    """Return True if the owner has completed onboarding (name is set)."""
    return bool(owner.name and owner.name.strip() and owner.name != "New User")


def main() -> None:
    st.set_page_config(page_title="PawPal+", page_icon="🐾")

    owner = _get_or_create_owner()

    # ------------------------------------------------------------------
    # First-run onboarding: ask for the owner's name
    # ------------------------------------------------------------------
    if not _is_onboarded(owner):
        st.title("🐾 Welcome to PawPal+")
        st.caption("Smart Pet Care Management System")
        st.write("Let's get you set up. What should we call you?")

        with st.form("onboarding_form"):
            name = st.text_input("Your name", placeholder="e.g. Gustavo")
            submitted = st.form_submit_button("Start using PawPal+ 🐾")

            if submitted:
                if name.strip():
                    st.session_state.owner.name = name.strip()
                    # NOTE: Do NOT auto-save here. That would overwrite any
                    # existing data.json. The user must click "Save to JSON"
                    # manually after adding their data.
                    st.rerun()
                else:
                    st.error("Please enter your name.")

        st.stop()  # Don't render the rest until the name is set

    # ------------------------------------------------------------------
    # Main app (owner is onboarded)
    # ------------------------------------------------------------------
    scheduler: Scheduler = st.session_state.get("scheduler") or Scheduler()
    st.session_state.scheduler = scheduler

    st.title(f"🐾 PawPal+ — Welcome, {owner.name}!")
    st.caption("Smart Pet Care Management System")

    # ------------------------------------------------------------------
    # Sidebar — Owner + Edit name + Reset + Persistence + Dashboard
    # ------------------------------------------------------------------
    st.sidebar.header(f"👤 {owner.name}")

    with st.sidebar.expander("✏️ Edit name"):
        new_name = st.text_input("New name", value=owner.name, key="edit_name_input")
        if st.button("Save name"):
            if new_name.strip():
                owner.name = new_name.strip()
                save_owner_to_json(owner, "data.json")
                st.success(f"Name changed to {owner.name}")
                st.rerun()

    if st.sidebar.button("🔄 Reset System"):
        st.session_state.owner = Owner(name="New User")
        st.rerun()

    # ---- JSON Persistence ----
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Persistence")

    if st.sidebar.button("💾 Save to JSON"):
        save_owner_to_json(owner, "data.json")
        st.sidebar.success("Data saved to data.json")

    if st.sidebar.button("📂 Load from JSON"):
        st.session_state.owner = load_owner_from_json("data.json")
        st.sidebar.success("Data loaded from data.json")
        st.rerun()

    # ---- Dashboard stats ----
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Dashboard")

    all_tasks_for_stats = owner.get_all_tasks()
    if all_tasks_for_stats:
        priority_counts = {"high": 0, "medium": 0, "low": 0}
        for t in all_tasks_for_stats:
            priority_counts[t.priority] += 1

        st.sidebar.metric("Total Tasks", len(all_tasks_for_stats))

        st.sidebar.write("**Tasks by Priority**")
        st.sidebar.bar_chart(
            {
                "Priority": list(priority_counts.keys()),
                "Count": list(priority_counts.values()),
            },
            x="Priority",
            y="Count",
        )

        st.sidebar.write("**Tasks per Pet**")
        pet_task_counts = {p.name: len(p.tasks) for p in owner.pets}
        st.sidebar.bar_chart(
            {
                "Pet": list(pet_task_counts.keys()),
                "Tasks": list(pet_task_counts.values()),
            },
            x="Pet",
            y="Tasks",
        )
    else:
        st.sidebar.info("Add tasks to see stats.")

    # ---- Registered pets ----
    st.sidebar.markdown("---")
    st.sidebar.subheader("Registered Pets")
    if owner.pets:
        for p in owner.pets:
            st.sidebar.write(f"• **{p.name}** ({p.species}, {p.age} yrs)")
    else:
        st.sidebar.info("No pets registered yet.")

    # ------------------------------------------------------------------
    # Main UI Tabs
    # ------------------------------------------------------------------
    tab_pet, tab_task, tab_schedule = st.tabs(
        ["🐶 Add Pet", "📝 Add Task", "📅 Today's Schedule"]
    )

    # ------------------------------------------------------------------
    # TAB 1: Add Pet
    # ------------------------------------------------------------------
    with tab_pet:
        st.subheader("Add a New Pet")
        with st.form("add_pet_form", clear_on_submit=True):
            pet_name = st.text_input("Pet Name")
            species = st.selectbox(
                "Species", ["Dog", "Cat", "Bird", "Fish", "Reptile", "Other"]
            )
            age = st.number_input("Age", min_value=0, max_value=30, value=1)
            submitted_pet = st.form_submit_button("Add Pet")

            if submitted_pet:
                if pet_name.strip():
                    new_pet = Pet(name=pet_name.strip(), species=species, age=int(age))
                    owner.add_pet(new_pet)
                    st.success(f"Added **{new_pet.name}** to your pets!")
                    st.rerun()
                else:
                    st.error("Please enter a valid pet name.")

        st.markdown("---")
        st.subheader("Current Pets")
        if owner.pets:
            for pet in owner.pets:
                st.write(
                    f"🐾 **{pet.name}** — {pet.species}, {pet.age} years old "
                    f"({len(pet.tasks)} tasks)"
                )
        else:
            st.info("No pets added yet. Use the form above to add your first pet!")

    # ------------------------------------------------------------------
    # TAB 2: Add Task
    # ------------------------------------------------------------------
    with tab_task:
        st.subheader("Add a Task for a Pet")
        if not owner.pets:
            st.warning("Please add at least one pet before creating tasks.")
        else:
            pet_names = [pet.name for pet in owner.pets]
            selected_pet_name = st.selectbox("Select Pet", pet_names)

            with st.form("add_task_form", clear_on_submit=True):
                description = st.text_input("Task Description")
                task_time = st.time_input("Task Time")
                frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
                priority = st.selectbox("Priority", ["high", "medium", "low"], index=1)
                submitted_task = st.form_submit_button("Add Task")

                if submitted_task:
                    if description.strip():
                        formatted_time = task_time.strftime("%H:%M")
                        new_task = Task(
                            description=description.strip(),
                            time=formatted_time,
                            due_date=date.today(),
                            frequency=frequency,
                            priority=priority,
                        )

                        target_pet = next(
                            (p for p in owner.pets if p.name == selected_pet_name),
                            None,
                        )
                        if target_pet:
                            target_pet.add_task(new_task)
                            st.success(
                                f"Task **'{new_task.description}'** added for "
                                f"**{target_pet.name}** at {new_task.time} "
                                f"({new_task.priority} priority)!"
                            )
                            st.rerun()
                    else:
                        st.error("Please enter a task description.")

    # ------------------------------------------------------------------
    # TAB 3: Today's Schedule
    # ------------------------------------------------------------------
    with tab_schedule:
        st.subheader("Today's Care Schedule")
        all_tasks = owner.get_all_tasks()

        if not all_tasks:
            st.info("No tasks scheduled for today!")
        else:
            incomplete_tasks = scheduler.filter_by_completion(
                all_tasks, completed=False
            )
            completed_tasks = scheduler.filter_by_completion(all_tasks, completed=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Tasks", len(all_tasks))
            col2.metric("Incomplete", len(incomplete_tasks))
            col3.metric("Completed", len(completed_tasks))

            st.markdown("---")

            conflicts = scheduler.detect_conflicts(all_tasks)
            if conflicts:
                st.warning("⚠️ **Schedule Conflicts Detected!**")
                for t1, t2 in conflicts:
                    st.write(
                        f"• Collision at **{t1.time}**: "
                        f"*'{t1.description}'* and *'{t2.description}'*"
                    )
                st.markdown("---")

            overlaps = scheduler.detect_overlaps(all_tasks)
            if overlaps:
                st.warning("⚠️ **30-Minute Window Overlaps Detected!**")
                for t1, t2 in overlaps:
                    st.write(
                        f"• Overlap between **{t1.time}** "
                        f"(*{t1.description}*) and **{t2.time}** "
                        f"(*{t2.description}*)"
                    )
                st.markdown("---")

            st.subheader("📋 Scheduled Tasks")
            sorted_tasks = scheduler.sort_by_time(all_tasks)

            for i, task in enumerate(sorted_tasks):
                pet_owner = next(
                    (p.name for p in owner.pets if task in p.tasks),
                    "Unknown",
                )

                cols = st.columns([1, 3, 2, 2, 2])
                cols[0].write(f"**{task.time}**")
                cols[1].write(f"{task.description} (*{pet_owner}*)")
                cols[2].write(f"Priority: `{task.priority}`")
                cols[3].write(f"Freq: `{task.frequency}`")

                if task.completed:
                    cols[4].success("✅ Done")
                else:
                    if cols[4].button(
                        "Mark Done", key=f"complete_{i}_{task.description}"
                    ):
                        task.mark_complete()
                        st.rerun()


if __name__ == "__main__":
    main()
