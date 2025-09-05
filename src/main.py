import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import datetime
import calendar # Importar el módulo calendar directamente
from agenda.calendar import Calendar
from agenda.tasks import Task
from agenda.sections import Section

class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # --- Configuración de Estilos ---
        self.setup_styles()

        self.set_app_icon()

        self.title("Agenda App")
        self.iconbitmap(default="") # Evitar error si no se encuentra el icono
        self.centrar_ventana(650, 550) # Tamaño de ventana más compacto
        self.resizable(False, False) # Hacer la ventana no redimensionable
        self.configure(bg=self.BG_COLOR) # Color de fondo de la ventana principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1) # Permite que el frame del calendario (fila 1) se expanda

        hoy = datetime.date.today()
        self.current_year = hoy.year
        self.current_month_num = hoy.month
        self.calendar = Calendar(self.current_year, self.current_month_num)

        self.predefined_sections = ["Gimnasio", "Escuela", "Trabajo", "Personal", "Hogar"]

        self.data_file = "tasks.txt" # Archivo para guardar los datos
        self.load_tasks() # Cargar tareas al iniciar

        self.create_widgets()

        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Guardar al cerrar

    def ask_string_non_resizable(self, title, prompt, parent):
        """
        Creates a simple dialog to ask for a string, but makes the window non-resizable.
        Returns the entered string, or None if the user cancels.
        """
        # The app instance is needed to access the color theme (self.BG_COLOR, etc.)
        app_instance = self

        class CustomDialog(simpledialog.Dialog):
            def body(self, master):
                # Apply the theme from the main app window to the dialog
                self.configure(bg=app_instance.BG_COLOR)
                master.configure(bg=app_instance.BG_COLOR)

                self.resizable(False, False)  # Make the dialog non-resizable

                # Internal widgets will pick up the global ttk style
                ttk.Label(master, text=prompt, justify=tk.LEFT, style='Dialog.TLabel').pack(padx=10, pady=(10, 5))
                self.entry = ttk.Entry(master, width=50, style='Dialog.TEntry')
                self.entry.pack(padx=10, pady=(0, 10), fill=tk.X, expand=True)
                
                return self.entry  # Set initial focus

            def buttonbox(self):
                # Override to use styled ttk.Buttons
                box = ttk.Frame(self)

                w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
                w.pack(side=tk.LEFT, padx=5, pady=5)
                w = ttk.Button(box, text="Cancelar", width=10, command=self.cancel)
                w.pack(side=tk.LEFT, padx=5, pady=5)

                self.bind("<Return>", self.ok)
                self.bind("<Escape>", self.cancel)

                box.pack()

            def apply(self):
                self.result = self.entry.get()

        # The 'parent' argument determines which window the dialog appears on top of.
        # The 'app_instance' provides the styling information.
        dialog = CustomDialog(parent, title=title)
        return dialog.result

    def ask_choice_non_resizable(self, title, prompt, parent):
        """
        Creates a dialog to choose from a list of options or enter a new one.
        """
        app_instance = self

        class CustomChoiceDialog(simpledialog.Dialog):
            def body(self, master):
                self.configure(bg=app_instance.BG_COLOR)
                master.configure(bg=app_instance.BG_COLOR)
                self.resizable(False, False)
                ttk.Label(master, text=prompt, justify=tk.LEFT, style='Dialog.TLabel').pack(padx=10, pady=(10, 5))

                self.choice_var = tk.StringVar(self)
                self.other_entry_var = tk.StringVar(self)

                radio_frame = ttk.Frame(master)
                radio_frame.pack(padx=15, pady=5, fill='x', expand=True)

                for section in app_instance.predefined_sections:
                    rb = ttk.Radiobutton(radio_frame, text=section, variable=self.choice_var, value=section, command=self.toggle_other_entry, style='Dialog.TRadiobutton')
                    rb.pack(anchor='w')
                
                other_frame = ttk.Frame(radio_frame)
                other_frame.pack(anchor='w', fill='x', expand=True, pady=(5,0))
                
                self.other_radio = ttk.Radiobutton(other_frame, text="Otro:", variable=self.choice_var, value="OTHER", command=self.toggle_other_entry, style='Dialog.TRadiobutton')
                self.other_radio.pack(side='left')

                self.other_entry = ttk.Entry(other_frame, textvariable=self.other_entry_var, width=40, style='Dialog.TEntry')
                self.other_entry.pack(side='left', fill='x', expand=True, padx=5)

                self.choice_var.set(app_instance.predefined_sections[0])
                self.toggle_other_entry()
                return self.other_entry

            def toggle_other_entry(self):
                if self.choice_var.get() == "OTHER":
                    self.other_entry.config(state='normal')
                    self.other_entry.focus_set()
                else:
                    self.other_entry.config(state='disabled')

            def buttonbox(self):
                box = ttk.Frame(self)
                w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
                w.pack(side=tk.LEFT, padx=5, pady=5)
                w = ttk.Button(box, text="Cancelar", width=10, command=self.cancel)
                w.pack(side=tk.LEFT, padx=5, pady=5)
                self.bind("<Return>", self.ok)
                self.bind("<Escape>", self.cancel)
                box.pack()

            def apply(self):
                if self.choice_var.get() == "OTHER":
                    self.result = self.other_entry_var.get().strip()
                else:
                    self.result = self.choice_var.get()

        dialog = CustomChoiceDialog(parent, title=title)
        return dialog.result

    def set_app_icon(self):
        """Establece el icono de la aplicación si el archivo existe."""
        # Se recomienda un archivo .ico para Windows
        icon_path = "assets/icon.ico" 
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except tk.TclError:
                print(f"Advertencia: No se pudo cargar el icono desde: {icon_path}")

    def setup_styles(self):
        """Define la paleta de colores y los estilos para la aplicación."""
        # --- Paleta de Colores (Tema Oscuro Moderno) ---
        self.BG_COLOR = "#2E2E2E"
        self.FG_COLOR = "#EAEAEA"
        self.FRAME_COLOR = "#3A3A3A"
        self.BUTTON_COLOR = "#7A5CC0" # Morado principal
        self.BUTTON_HOVER_COLOR = "#9378D5" # Morado más claro para el hover
        self.BUTTON_TEXT_COLOR = "#FFFFFF"
        self.DANGER_COLOR = "#E53935"
        self.DANGER_HOVER_COLOR = "#F44336"
        self.ENTRY_BG = "#424242"
        self.HEADER_COLOR = self.BUTTON_COLOR

        # --- Configuración de Estilos TTK ---
        style = ttk.Style(self)
        style.theme_use('clam') # 'clam' es un tema muy personalizable

        # Estilos generales
        style.configure('.', background=self.BG_COLOR, foreground=self.FG_COLOR, font=('Arial', 10))
        style.configure('TFrame', background=self.BG_COLOR)
        style.configure('TLabel', background=self.BG_COLOR, foreground=self.FG_COLOR)
        style.configure('TButton', background=self.BUTTON_COLOR, foreground=self.BUTTON_TEXT_COLOR, borderwidth=0, focusthickness=0, padding=5)
        style.map('TButton', background=[('active', self.BUTTON_HOVER_COLOR)])

        # Estilo para botones de peligro (Eliminar)
        style.configure('Danger.TButton', background=self.DANGER_COLOR, foreground=self.BUTTON_TEXT_COLOR)
        style.map('Danger.TButton', background=[('active', self.DANGER_HOVER_COLOR)])

        # Estilo para días del calendario con tareas
        # Se añade 'background=self.BG_COLOR' para que no herede el fondo morado de TButton,
        # lo que causaba que el texto (también morado) fuera invisible.
        style.configure('HasTasks.TButton', font=('Arial', 10, 'bold'), background=self.BUTTON_COLOR)
        # Se mantiene el texto morado para el estado normal y se define un color de fondo para el hover
        # que sea consistente con otros elementos de la UI.
        style.map('HasTasks.TButton', foreground=[('!active', self.FG_COLOR)],
                                    background=[('active', self.BUTTON_HOVER_COLOR)]) # Fondo gris claro al pasar el mouse

        # Estilo para el día actual
        style.configure('Today.TButton', bordercolor=self.BUTTON_COLOR, borderwidth=2)
        style.map('Today.TButton', bordercolor=[('active', self.BUTTON_HOVER_COLOR)])

        # Estilos para widgets de entrada
        style.configure('TEntry', font=('Arial', 12), fieldbackground=self.ENTRY_BG, foreground=self.FG_COLOR, borderwidth=1, insertcolor=self.FG_COLOR)
        style.configure('TMenubutton', background=self.BUTTON_COLOR, foreground=self.BUTTON_TEXT_COLOR, borderwidth=0, arrowcolor=self.FG_COLOR)
        style.map('TMenubutton', background=[('active', self.BUTTON_HOVER_COLOR)])

        # Estilo para Checkbuttons
        style.configure('TCheckbutton',
                        background=self.BG_COLOR,
                        foreground=self.FG_COLOR,
                        padding=5)
        
        style.map('TCheckbutton',
                  background=[('active', self.FRAME_COLOR)], # Color de fondo al pasar el mouse
                  indicatorcolor=[('selected', self.BUTTON_COLOR)]) # Color del indicador (check) al seleccionar

        # Estilo para Radiobuttons
        style.configure('TRadiobutton',
                        background=self.BG_COLOR,
                        foreground=self.FG_COLOR,
                        padding=5)
        
        style.map('TRadiobutton',
                  background=[('active', self.FRAME_COLOR)], # Color de fondo al pasar el mouse
                  indicatorcolor=[('selected', self.BUTTON_COLOR)]) # Color del indicador al seleccionar

        # Estilos para widgets de diálogo (letras más grandes)
        dialog_font = ('Arial', 14, "normal") # Fuente grande para el texto del diálogo y la entrada
        dialog_option_font = ('Arial', 12) # Fuente un poco más pequeña para las opciones
        style.configure('Dialog.TLabel', font=dialog_font, background=self.BG_COLOR)
        style.configure('Dialog.TEntry', font=dialog_font, fieldbackground=self.ENTRY_BG, foreground=self.FG_COLOR, borderwidth=1, insertcolor=self.FG_COLOR)
        style.configure('Dialog.TRadiobutton', font=dialog_option_font, background=self.BG_COLOR, foreground=self.FG_COLOR, padding=5)
        style.map('Dialog.TRadiobutton',
                  background=[('active', self.FRAME_COLOR)],
                  indicatorcolor=[('selected', self.BUTTON_COLOR)])

    def centrar_ventana(self, ancho, alto):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def create_widgets(self):
        # Frame superior para selección de mes y año
        month_year_frame = ttk.Frame(self, padding="10")
        month_year_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        month_year_frame.columnconfigure(1, weight=1) # Columna del menú de mes
        month_year_frame.columnconfigure(3, weight=1) # Columna del campo de año

        # Etiqueta y Dropdown para los meses
        ttk.Label(month_year_frame, text="Mes:").grid(row=0, column=0, padx=5, sticky="w")
        self.month_names = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.selected_month = tk.StringVar(self)
        self.selected_month.set(self.month_names[self.current_month_num - 1]) # Mes inicial (current_month_num es 1-12)
        month_menu = ttk.OptionMenu(month_year_frame, self.selected_month, self.selected_month.get(), *self.month_names, command=self.update_calendar_display)
        month_menu.grid(row=0, column=1, padx=5, sticky="ew")

        # Etiqueta y Campo para el año
        ttk.Label(month_year_frame, text="Año:").grid(row=0, column=2, padx=5, sticky="w")
        self.year_entry = ttk.Entry(month_year_frame, width=6) # Ajustar ancho
        self.year_entry.insert(0, str(self.current_year))
        self.year_entry.grid(row=0, column=3, padx=5, sticky="ew")
        self.year_entry.bind("<Return>", self.update_calendar_display_from_entry) # Actualiza al presionar Enter

        # Frame para el calendario (se expandirá con la ventana)
        self.cal_frame = ttk.Frame(self, padding="10", relief="groove", borderwidth=2)
        self.cal_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        # Configurar las columnas para que se expandan dentro del cal_frame
        for i in range(7):
            self.cal_frame.columnconfigure(i, weight=1)

        self.display_calendar()

        # Frame para botones de acción (añadir tarea, ver tareas, salir)
        action_btns_frame = ttk.Frame(self, padding="10")
        action_btns_frame.grid(row=2, column=0, pady=10, sticky="ew")
        action_btns_frame.columnconfigure(0, weight=1)
        action_btns_frame.columnconfigure(1, weight=1)
        action_btns_frame.columnconfigure(2, weight=1)

        ttk.Button(action_btns_frame, text="Ver tareas", command=self.ver_tareas).grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(action_btns_frame, text="Salir", command=self.destroy).grid(row=0, column=2, padx=5, sticky="ew")

    def display_calendar(self):
        # Limpiar el contenido actual del calendario
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        # Mostrar los días de la semana
        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        for i, dia in enumerate(dias):
            lbl = ttk.Label(self.cal_frame, text=dia, anchor="center", font=("Arial", 10, "bold"), foreground=self.HEADER_COLOR)
            lbl.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")

        # Obtener la matriz de días del mes
        # monthcalendar devuelve una lista de listas, donde cada sublista es una semana.
        # 0 representa un día fuera del mes.
        today = datetime.date.today() # Obtener la fecha actual una vez
        matriz = calendar.monthcalendar(self.calendar.year, self.calendar.month_num)
        
        for r, semana in enumerate(matriz):
            for c, dia in enumerate(semana):
                if dia == 0:
                    # Días fuera del mes, se muestran como etiquetas vacías o deshabilitadas
                    lbl = ttk.Label(self.cal_frame, text="", width=4) # Usar Label para días vacíos
                    lbl.grid(row=r+1, column=c, padx=2, pady=2, sticky="nsew")
                else:
                    # Determinar el estilo del botón
                    is_today = (self.calendar.year == today.year and
                                self.calendar.month_num == today.month and
                                dia == today.day)
                    
                    date_str = f"{self.calendar.year}-{self.calendar.month_num:02d}-{dia:02d}"
                    has_tasks = self.calendar.get_tasks(date_str)

                    button_style = 'TButton' # Estilo por defecto
                    if is_today:
                        button_style = 'Today.TButton'
                    elif has_tasks:
                        button_style = 'HasTasks.TButton'

                    btn = ttk.Button(
                        self.cal_frame,
                        text=str(dia),
                        style=button_style,
                        command=lambda d=dia: self.agregar_tarea_dia(d)
                    )
                    btn.grid(row=r+1, column=c, padx=2, pady=2, sticky="nsew")
                
                # Configurar la fila para que se expanda también
                self.cal_frame.rowconfigure(r+1, weight=1)

    def update_calendar_display_from_entry(self, event=None):
        try:
            new_year = int(self.year_entry.get())
            if not (1900 <= new_year <= 2100): # Rango de años razonable
                raise ValueError("Año fuera de rango.")
            self.current_year = new_year
            self.update_calendar_display()
        except ValueError:
            messagebox.showerror("Error de Año", "Año inválido. Por favor, ingrese un número entre 1900 y 2100.")

    def update_calendar_display(self, *args): # *args para ignorar el argumento del OptionMenu
        selected_month_name = self.selected_month.get()
        # Encontrar el índice del mes seleccionado (1-12)
        try:
            new_month_num = self.month_names.index(selected_month_name) + 1
        except ValueError:
            messagebox.showerror("Error de Mes", "Mes inválido seleccionado.")
            return

        # Actualizar el objeto Calendar con el nuevo año y mes
        self.calendar = Calendar(self.current_year, new_month_num)
        self.display_calendar()

    def agregar_tarea_dia(self, dia):
        # 1. Format the date for displaying to the user as DD-MM-YYYY
        # current_month_num is already the month number (1-12)
        # dia is the day number
        # current_year is the year
        
        try:
            # Create a datetime.date object to easily format
            date_obj = datetime.date(self.current_year, self.calendar.month_num, dia)
            display_date_str = date_obj.strftime("%d-%m-%Y")
        except ValueError:
            # This should ideally not happen if the calendar buttons are valid days,
            # but it's a fallback for invalid date combinations (e.g., Feb 30th).
            display_date_str = f"{dia:02d}-{self.calendar.month_num:02d}-{self.current_year}"

        # 2. The date passed to the calendar's add_task method should be YYYY-MM-DD
        # because the add_task method in calendar.py converts to and stores this format internally.
        # Passing YYYY-MM-DD directly avoids any ambiguity or potential parsing issues in calendar.py.
        storage_date_str = f"{self.current_year}-{self.calendar.month_num:02d}-{dia:02d}"
        
        # 3. Prompt the user for task details, displaying the date in DD-MM-YYYY format
        title = self.ask_string_non_resizable("Título", f"Ingrese el título de la tarea para el {display_date_str}:", parent=self)
        if title is None:
            return # User cancelled

        description = self.ask_string_non_resizable("Descripción", "Ingrese la descripción de la tarea:", parent=self)
        if description is None:
            return # User cancelled

        section_name = self.ask_choice_non_resizable("Sección", "Elija o ingrese una sección:", parent=self)
        if section_name is None:
            return # User cancelled
        
        if not section_name.strip():
            section_name = "General" # Default value if empty

        # 4. Create Task and Section objects
        section = Section(section_name)
        task = Task(title, description, section)
        
        # 5. Add the task to the calendar using the internal YYYY-MM-DD format
        self.calendar.add_task(storage_date_str, task)
        
        # 6. Show success message to the user, again using the DD-MM-YYYY display format
        messagebox.showinfo("Éxito", f"Tarea '{title}' agregada para el {display_date_str}.")
        self.save_tasks() # Guardar después de agregar una tarea

    def ver_tareas(self):
        # Si no hay tareas en el diccionario, muestra un mensaje y termina.
        if not self.calendar.tasks:
            messagebox.showinfo("Sin tareas", "No hay tareas registradas.")
            return

        # 1. Crear la ventana Toplevel
        top = tk.Toplevel(self)
        top.title("Historial de Tareas")
        top.configure(bg=self.BG_COLOR)
        self.centrar_ventana_toplevel(top, 500, 450) # Centrar la ventana
        top.resizable(False, False)
        top.transient(self) # Mantener la ventana por encima de la principal
        top.grab_set()      # Hacer la ventana modal (bloquea la interacción con la principal)

        # 2. Crear un Frame con Scrollbar para la lista de tareas
        container = ttk.Frame(top)
        container.pack(fill="both", expand=True, padx=10, pady=5)

        canvas = tk.Canvas(container, bg=self.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # 3. Poblar el frame con Checkbuttons interactivos
        self.task_vars = [] # Guardar referencia a las variables de Tkinter

        sorted_dates = sorted(self.calendar.tasks.keys())
        for fecha_str_internal in sorted_dates: # fecha_str_internal es YYYY-MM-DD
            tasks = self.calendar.tasks[fecha_str_internal]
            try:
                display_date = datetime.datetime.strptime(fecha_str_internal, "%Y-%m-%d").strftime("%d-%m-%Y")
            except ValueError:
                display_date = fecha_str_internal
            
            # Encabezado de fecha
            header = ttk.Label(scrollable_frame, text=f"--- Tareas para el {display_date} ---", font=("Arial", 12, "bold"), foreground=self.HEADER_COLOR)
            header.pack(anchor="w", pady=(10, 5), padx=10)

            for task in tasks:
                # Crear un frame para cada fila de tarea (checkbox + botón de eliminar)
                task_row_frame = ttk.Frame(scrollable_frame)
                task_row_frame.pack(fill='x', expand=True, padx=10)

                # Variable de control para el Checkbutton
                var = tk.BooleanVar(value=task.completed)
                self.task_vars.append(var) # Guardar referencia

                # Crear el Checkbutton
                check_button = ttk.Checkbutton(
                    task_row_frame,
                    text=f"{task.title} ({task.section.name})",
                    variable=var,
                    command=lambda t=task, v=var: self.toggle_task_completion(t, v)
                )
                check_button.pack(side=tk.LEFT, anchor="w", pady=2)

                # Crear un frame para los botones de acción de la tarea
                action_frame = ttk.Frame(task_row_frame)
                action_frame.pack(side=tk.RIGHT, padx=(0, 5))

                # Botón para editar la tarea
                edit_button = ttk.Button(
                    action_frame,
                    text="Editar",
                    command=lambda f=fecha_str_internal, t=task, top_win=top: self.editar_tarea(f, t, top_win)
                )
                edit_button.pack(side=tk.LEFT, padx=(0, 5))

                # Crear el botón para eliminar la tarea
                delete_button = ttk.Button(
                    action_frame,
                    text="Eliminar",
                    style='Danger.TButton', # Aplicar el estilo de peligro
                    command=lambda f=fecha_str_internal, t=task, top_win=top: self.eliminar_tarea(f, t, top_win),
                )
                delete_button.pack(side=tk.RIGHT, padx=(0, 5))

        # 4. Añadir un botón para cerrar la ventana
        ttk.Button(top, text="Cerrar", command=top.destroy).pack(pady=10)

    def toggle_task_completion(self, task: Task, var: tk.BooleanVar):
        """Actualiza el estado de completado de la tarea basado en el checkbox."""
        task.set_completed(var.get())
        self.save_tasks() # Guardar después de cambiar el estado de una tarea

    def editar_tarea(self, fecha_str, task_to_edit, toplevel_window):
        """Permite editar el título y la descripción de una tarea existente."""
        
        # Pedir nuevo título
        new_title = self.ask_string_non_resizable("Editar Título", f"Nuevo título para '{task_to_edit.title}':", parent=toplevel_window)
        if new_title is None: # El usuario canceló
            return

        # Pedir nueva descripción
        new_description = self.ask_string_non_resizable("Editar Descripción", f"Nueva descripción:", parent=toplevel_window)
        if new_description is None: # El usuario canceló
            return

        # Pedir nueva sección
        new_section_name = self.ask_choice_non_resizable("Editar Sección", "Elija o ingrese la nueva sección:", parent=toplevel_window)
        if new_section_name is None: # El usuario canceló
            return

        # Actualizar el objeto de la tarea en memoria
        if new_title.strip(): # Solo actualizar si no está vacío
            task_to_edit.title = new_title
        
        task_to_edit.description = new_description # La descripción puede estar vacía

        if new_section_name.strip():
            task_to_edit.section = Section(new_section_name)

        # Guardar los cambios y refrescar la vista
        self.save_tasks()
        
        # Refrescar la ventana de tareas para mostrar los cambios
        toplevel_window.destroy()
        self.ver_tareas()
        messagebox.showinfo("Éxito", "Tarea actualizada correctamente.", parent=self)

    def eliminar_tarea(self, fecha_str, task_to_delete, toplevel_window):
        """Elimina una tarea específica, pide confirmación y actualiza la vista."""
        
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar la tarea '{task_to_delete.title}'?",
            parent=toplevel_window # Asegura que el diálogo aparezca sobre la ventana de tareas
        )

        if not confirm:
            return

        # Eliminar la tarea del modelo de datos
        if fecha_str in self.calendar.tasks:
            tasks_on_date = self.calendar.tasks[fecha_str]
            if task_to_delete in tasks_on_date:
                tasks_on_date.remove(task_to_delete)
            
            # Si no quedan más tareas para esa fecha, eliminar la entrada completa
            if not tasks_on_date:
                del self.calendar.tasks[fecha_str]

        self.save_tasks()
        toplevel_window.destroy()
        self.ver_tareas()

    def save_tasks(self):
        """Guarda todas las tareas en el archivo de texto plano."""
        lines_to_save = []
        for date_str, tasks_list in self.calendar.tasks.items():
            for task in tasks_list:
                # Reemplazar el separador en los datos para evitar conflictos
                title = task.title.replace('|', '{{PIPE}}')
                description = task.description.replace('|', '{{PIPE}}')
                section_name = task.section.name.replace('|', '{{PIPE}}')
                
                # Crear la línea con el formato: FECHA|TITULO|DESCRIPCION|SECCION|COMPLETADO
                line = f"{date_str}|{title}|{description}|{section_name}|{task.completed}"
                lines_to_save.append(line)
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines_to_save))
        except IOError as e:
            messagebox.showerror("Error de guardado", f"No se pudieron guardar las tareas: {e}")

    def load_tasks(self):
        """Carga las tareas desde el archivo de texto plano al iniciar la aplicación."""
        if not os.path.exists(self.data_file):
            return # No hay archivo para cargar, empezar de cero
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Limpiar el diccionario de tareas actual antes de cargar
            self.calendar.tasks = {}

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                parts = line.split('|', 4)
                if len(parts) != 5:
                    continue # Ignorar líneas mal formadas

                date_str, title, description, section_name, completed_str = parts

                # Restaurar el separador si fue reemplazado
                title = title.replace('{{PIPE}}', '|')
                description = description.replace('{{PIPE}}', '|')
                section_name = section_name.replace('{{PIPE}}', '|')

                # Recrear los objetos y añadirlos al calendario
                section = Section(section_name)
                task = Task(title=title, description=description, section=section)
                task.set_completed(completed_str == 'True') # Convertir string a booleano
                self.calendar.add_task(date_str, task)
        except IOError as e:
            messagebox.showerror("Error de carga", f"No se pudieron cargar las tareas: {e}")

    def on_closing(self):
        """Maneja el evento de cierre de la ventana."""
        self.save_tasks()
        self.destroy()

    def centrar_ventana_toplevel(self, toplevel_window, ancho, alto):
        toplevel_window.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (ancho // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (alto // 2)
        toplevel_window.geometry(f"{ancho}x{alto}+{x}+{y}")

if __name__ == "__main__":
    app = AgendaApp()
    app.mainloop()