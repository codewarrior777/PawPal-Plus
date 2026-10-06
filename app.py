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


def main() -> None:
    st.set_page_config(page_title="PawPal+", page_icon="🐾")
    st.title("🐾 PawPal+")

    # Initialize Owner and Scheduler in session state
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(name="Alex")

    if "scheduler" not in st.session_state:
        st.session_state.scheduler = Scheduler()

    owner: Owner = st.session_state.owner
    scheduler: Scheduler = st.session_state.scheduler

    # ------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------
    st.sidebar.header(f"👤 Owner: {owner.name}")

    if st.sidebar.button("🔄 Reset System"):
        st.session_state.owner = Owner(name="Alex")
        st.rerun()

    # ---- Stretch Feature: JSON Persistence ----
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Persistence")

    if st.sidebar.button("💾 Save to JSON"):
        save_owner_to_json(st.session_state.owner, "data.json")
        st.sidebar.success("Data saved to data.json")

    if st.sidebar.button("📂 Load from JSON"):
        st.session_state.owner = load_owner_from_json("data.json")
        st.sidebar.success("Data loaded from data.json")
        st.rerun()

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
                submitted_task = st.form_submit_button("Add Task")

                if submitted_task:
                    if description.strip():
                        # Format time as "HH:MM"
                        formatted_time = task_time.strftime("%H:%M")
                        new_task = Task(
                            description=description.strip(),
                            time=formatted_time,
                            due_date=date.today(),
                            frequency=frequency,
                        )

                        # Find selected pet and add task
                        target_pet = next(
                            (p for p in owner.pets if p.name == selected_pet_name),
                            None,
                        )
                        if target_pet:
                            target_pet.add_task(new_task)
                            st.success(
                                f"Task **'{new_task.description}'** added for "
                                f"**{target_pet.name}** at {new_task.time}!"
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
            # Stats bar
            incomplete_tasks = scheduler.filter_by_completion(
                all_tasks, completed=False
            )
            completed_tasks = scheduler.filter_by_completion(all_tasks, completed=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Tasks", len(all_tasks))
            col2.metric("Incomplete Tasks", len(incomplete_tasks))
            col3.metric("Completed Tasks", len(completed_tasks))

            st.markdown("---")

            # Conflict Detection
            conflicts = scheduler.detect_conflicts(all_tasks)
            if conflicts:
                st.warning("⚠️ **Schedule Conflicts Detected!**")
                for t1, t2 in conflicts:
                    st.write(
                        f"• Collision at **{t1.time}**: "
                        f"*'{t1.description}'* and *'{t2.description}'*"
                    )
                st.markdown("---")

            # Sorted Tasks View
            st.subheader("📋 Scheduled Tasks")
            sorted_tasks = scheduler.sort_by_time(all_tasks)

            for i, task in enumerate(sorted_tasks):
                # Find which pet owns this task
                pet_owner = next(
                    (p.name for p in owner.pets if task in p.tasks), "Unknown"
                )

                cols = st.columns([1, 3, 2, 2])
                cols[0].write(f"**{task.time}**")
                cols[1].write(f"{task.description} (*{pet_owner}*)")
                cols[2].write(f"Frequency: `{task.frequency}`")

                # Mark complete toggle button
                if task.completed:
                    cols[3].success("✅ Done")
                else:
                    if cols[3].button(
                        "Mark Done", key=f"complete_{i}_{task.description}"
                    ):
                        task.mark_complete()
                        st.rerun()


if __name__ == "__main__":
    main()
