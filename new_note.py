import json
from datetime import datetime

class Note:
    def __init__(self, note_id, title, body, timestamp):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.timestamp = timestamp

class NoteManager:
    def __init__(self, filename):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        try:
            with open(self.filename, 'r') as file:
                notes_data = json.load(file)
                notes = [Note(int(note['note_id']), note['title'], note['body'], self.parse_timestamp(note['timestamp']))
                         for note in notes_data if all(key in note for key in ['note_id', 'title', 'body', 'timestamp'])]
                return notes
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def parse_timestamp(self, timestamp_str):
        return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

    def save_notes(self):
        notes_data = [{"note_id": note.note_id, "title": note.title, "body": note.body, "timestamp": note.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
                      for note in self.notes]
        with open(self.filename, 'w') as file:
            json.dump(notes_data, file)

    def list_notes(self):
        if not self.notes:
            print("No notes available.")
            return

        print("{:<5} {:<30} {:<30} {:<25}".format("ID", "Title", "Last Modified", "Timestamp"))
        print("="*90)

        for note in self.notes:
            print("{:<5} {:<30} {:<30} {:<25}".format(note.note_id, note.title, note.timestamp.strftime("%Y-%m-%d %H:%M:%S"), note.timestamp))

   
    def view_note(self, note_id):
        try:
            note_id = int(note_id)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        note = next((note for note in self.notes if note.note_id == note_id), None)
        if note:
            print(f"ID: {note.note_id}\nTitle: {note.title}\nBody: {note.body}\nTimestamp: {note.timestamp}")
        else:
            print("Note not found.")   
   

    def edit_note(self, note_id, title, body):
        try:
            note_id = int(note_id)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        note = next((note for note in self.notes if note.note_id == note_id), None)
        if note:
            note.title = title
            note.body = body
            note.timestamp = datetime.now()
            self.save_notes()
            print("Note edited successfully.")
        else:
            print("Note not found.")

    def add_note(self, title, body):
        note_id = len(self.notes) + 1
        timestamp = datetime.now()
        new_note = Note(note_id, title, body, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print("Note added successfully.")

    def edit_note(self, note_id, title, body):
        note = next((note for note in self.notes if note.note_id == note_id), None)
        if note:
            note.title = title
            note.body = body
            note.timestamp = datetime.now()
            self.save_notes()
            print("Note edited successfully.")
        else:
            print("Note not found.")

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.note_id != note_id]
        self.save_notes()
        print("Note deleted successfully.")

    def filter_notes_by_date(self, start_date, end_date):
        filtered_notes = [note for note in self.notes if start_date <= note.timestamp <= end_date]
        return filtered_notes
    
    def delete_note(self, note_id):
        try:
            note_id = int(note_id)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        if any(note.note_id == note_id for note in self.notes):
            self.notes = [note for note in self.notes if note.note_id != note_id]
            self.save_notes()  # Сохраняем изменения в файл
            print("Note deleted successfully.")
        else:
            print("Note not found.")

if __name__ == "__main__":
    filename = "notes.json"
    manager = NoteManager(filename)
    while True:
        print("\nOptions:")
        print("1. List notes")
        print("2. View note")
        print("3. Add note")
        print("4. Edit note")
        print("5. Delete note")
        print("6. Filter notes by date")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            manager.list_notes()
        elif choice == "2":
            note_id = input("Enter note ID: ")
            manager.view_note(note_id)
        elif choice == "3":
            title = input("Enter note title: ")
            body = input("Enter note body: ")
            manager.add_note(title, body)
        elif choice == "4":
            note_id = input("Enter note ID to edit: ")
            title = input("Enter new title: ")
            body = input("Enter new body: ")
            manager.edit_note(note_id, title, body)
        elif choice == "5":
            note_id = input("Enter note ID to delete: ")
            manager.delete_note(note_id)
        elif choice == "6":
            start_date_str = input("Enter start date (YYYY-MM-DD HH:MM:SS): ")
            end_date_str = input("Enter end date (YYYY-MM-DD HH:MM:SS): ")

            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print("Invalid date format. Please use the format YYYY-MM-DD HH:MM:SS.")
                continue

            filtered_notes = manager.filter_notes_by_date(start_date, end_date)
            if filtered_notes:
                print("\nFiltered notes:")
                for note in filtered_notes:
                    print(f"{note.note_id}. {note.title} - {note.timestamp}")
            else:
                print("No notes found in the specified date range.")

        elif choice == "7":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
