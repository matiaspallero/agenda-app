# Agenda App

Este proyecto es una aplicación de agenda que permite a los usuarios gestionar sus tareas diarias organizadas por secciones como gimnasio, escuela, iglesia, entre otros. La aplicación muestra todos los días del mes y permite marcar las tareas como completadas.

## Estructura del Proyecto

```
agenda-app
├── src
│   ├── main.py               # Punto de entrada de la aplicación
│   ├── agenda
│   │   ├── __init__.py       # Inicializa el paquete de agenda
│   │   ├── calendar.py        # Maneja la visualización del calendario
│   │   ├── tasks.py          # Define la clase Task para las tareas diarias
│   │   └── sections.py       # Define la clase Section para las secciones de tareas
│   └── utils
│       └── helpers.py        # Funciones auxiliares para la aplicación
├── requirements.txt          # Dependencias necesarias para el proyecto
└── README.md                 # Documentación del proyecto
```

## Instalación

1. Clona el repositorio en tu máquina local.
2. Navega al directorio del proyecto.
3. Instala las dependencias necesarias ejecutando:

```
pip install -r requirements.txt
```

## Uso

Para iniciar la aplicación, ejecuta el siguiente comando:

```
python src/main.py
```

## Funcionalidades

- Visualización de todos los días del mes.
- Agregar tareas diarias organizadas por secciones.
- Marcar tareas como completadas.
- Gestión de diferentes secciones de tareas.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.