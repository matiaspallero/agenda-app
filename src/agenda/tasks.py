class Task:
    def __init__(self, title, description, section):
        self.title = title
        self.description = description
        self.section = section
        self.completed = False

    def mark_completed(self):
        """Marca la tarea como completada. Para compatibilidad o casos simples."""
        self.completed = True

    def set_completed(self, status: bool):
        """Establece el estado de completado de la tarea."""
        self.completed = status

    def __str__(self):
        status = "✔️" if self.completed else "❌"
        return f"{self.title} - {self.description} [{self.section}] - {status}"