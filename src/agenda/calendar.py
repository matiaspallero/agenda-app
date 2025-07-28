import calendar
import datetime

class Calendar:
    def __init__(self, year, month_num):  # Cambiado a month_num
        self.year = year
        self.month_num = month_num # Almacena el número del mes
        self.days = self.get_days_in_month()
        self.tasks = {}  # Diccionario para almacenar tareas por fecha

    def get_month_name(self):
        # Asegúrate de que month_num sea válido
        if 1 <= self.month_num <= 12:
            return calendar.month_name[self.month_num]
        return "Mes Desconocido"

    def get_days_in_month(self):
        return [day for day in range(1, calendar.monthrange(self.year, self.month_num)[1] + 1)]

    def display_calendar(self):
        cal = calendar.TextCalendar()
        return cal.formatmonth(self.year, self.month_num)

    def get_tasks_for_day(self, day):
        # Esta función puede ser útil si quieres obtener tareas para un día específico
        # directamente desde el objeto Calendar.
        # Por ahora, simplemente llama a get_tasks con el formato de fecha adecuado.
        date_str = f"{self.year}-{self.month_num:02d}-{day:02d}"
        return self.get_tasks(date_str)

    def add_task(self, date_str, task):
        """Añade una tarea a una fecha específica. Asume formato YYYY-MM-DD."""
        if date_str not in self.tasks:
            self.tasks[date_str] = []
        self.tasks[date_str].append(task)

    def get_tasks(self, date_str):
        """Obtiene las tareas de una fecha específica. Asume formato YYYY-MM-DD."""
        return self.tasks.get(date_str, [])