import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_tasks(self):
        """Save tasks to JSON file."""
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, title, priority='medium', due_date=None):
        """Add a new task."""
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'priority': priority,
            'due_date': due_date,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Task added: '{title}'")

    def view_tasks(self, show_completed=False):
        """Display all tasks."""
        if not self.tasks:
            print("No tasks found.")
            return

        # Filter tasks
        active_tasks = [t for t in self.tasks if not t['completed']]
        completed_tasks = [t for t in self.tasks if t['completed']]

        if active_tasks:
            print("\n📋 ACTIVE TASKS")
            print("-" * 60)
            for task in active_tasks:
                self.display_task(task)

        if show_completed and completed_tasks:
            print("\n✅ COMPLETED TASKS")
            print("-" * 60)
            for task in completed_tasks:
                self.display_task(task)

    def display_task(self, task):
        """Display a single task."""
        status = "○" if not task['completed'] else "●"
        priority_emoji = {"low": "🔵", "medium": "🟡", "high": "🔴"}
        emoji = priority_emoji.get(task['priority'], "🔵")
        
        print(f"{status} [{task['id']}] {emoji} {task['title']}")
        if task['due_date']:
            print(f"    Due: {task['due_date']}")

    def complete_task(self, task_id):
        """Mark a task as completed."""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                print(f"✓ Task '{task['title']}' marked as completed!")
                return
        print(f"Task {task_id} not found.")

    def delete_task(self, task_id):
        """Delete a task."""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                title = task['title']
                self.tasks.pop(i)
                self.save_tasks()
                print(f"✗ Task '{title}' deleted.")
                return
        print(f"Task {task_id} not found.")

    def update_task(self, task_id, title=None, priority=None, due_date=None):
        """Update a task."""
        for task in self.tasks:
            if task['id'] == task_id:
                if title:
                    task['title'] = title
                if priority:
                    task['priority'] = priority
                if due_date:
                    task['due_date'] = due_date
                self.save_tasks()
                print(f"✓ Task {task_id} updated!")
                return
        print(f"Task {task_id} not found.")

    def get_stats(self):
        """Get task statistics."""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t['completed']])
        active = total - completed
        
        print("\n📊 STATISTICS")
        print(f"Total tasks: {total}")
        print(f"Active: {active}")
        print(f"Completed: {completed}")
        if total > 0:
            print(f"Progress: {(completed/total)*100:.1f}%")


def main():
    """Main application loop."""
    app = TodoApp()
    
    print("=" * 60)
    print("       📝 WELCOME TO YOUR TO-DO LIST APP")
    print("=" * 60)
    
    commands = {
        '1': ('Add task', 'add'),
        '2': ('View tasks', 'view'),
        '3': ('Complete task', 'complete'),
        '4': ('Delete task', 'delete'),
        '5': ('Update task', 'update'),
        '6': ('Statistics', 'stats'),
        '7': ('Exit', 'exit')
    }
    
    while True:
        print("\n" + "-" * 60)
        print("MENU:")
        for key, (description, _) in commands.items():
            print(f"  {key}. {description}")
        print("-" * 60)
        
        choice = input("Select option (1-7): ").strip()
        
        if choice == '1':
            title = input("Enter task title: ").strip()
            if not title:
                print("Task title cannot be empty.")
                continue
            priority = input("Priority (low/medium/high) [medium]: ").strip() or 'medium'
            due_date = input("Due date (YYYY-MM-DD) [optional]: ").strip() or None
            app.add_task(title, priority, due_date)
        
        elif choice == '2':
            show_completed = input("Show completed tasks? (y/n) [n]: ").strip().lower() == 'y'
            app.view_tasks(show_completed)
        
        elif choice == '3':
            app.view_tasks()
            try:
                task_id = int(input("Enter task ID to complete: ").strip())
                app.complete_task(task_id)
            except ValueError:
                print("Invalid task ID.")
        
        elif choice == '4':
            app.view_tasks()
            try:
                task_id = int(input("Enter task ID to delete: ").strip())
                app.delete_task(task_id)
            except ValueError:
                print("Invalid task ID.")
        
        elif choice == '5':
            app.view_tasks()
            try:
                task_id = int(input("Enter task ID to update: ").strip())
                title = input("New title [leave empty to skip]: ").strip() or None
                priority = input("New priority (low/medium/high) [leave empty to skip]: ").strip() or None
                due_date = input("New due date (YYYY-MM-DD) [leave empty to skip]: ").strip() or None
                app.update_task(task_id, title, priority, due_date)
            except ValueError:
                print("Invalid task ID.")
        
        elif choice == '6':
            app.get_stats()
        
        elif choice == '7':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
