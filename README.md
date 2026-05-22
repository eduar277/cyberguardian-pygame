# CyberGuardian: Amenaza Xenon

**CyberGuardian: Amenaza Xenon** es un videojuego 2D educativo desarrollado con **Python** y **Pygame**. El juego combina plataformas, enemigos, música, fondos con efecto parallax y retos interactivos de ciberseguridad.

El jugador controla a **Cyber**, un defensor digital que debe superar tres niveles, evitar drones enemigos e interactuar con terminales para resolver desafíos relacionados con seguridad informática.

---

## Descripción del juego

CyberGuardian se desarrolla en un entorno digital amenazado por **Xenon**, una entidad maliciosa que intenta comprometer la red central.

Cyber debe avanzar por distintos escenarios, superar plataformas, evitar enemigos y resolver retos de ciberseguridad para desbloquear puertas y completar la misión.

El juego incluye tres niveles:

- **Nivel 1:** reto de phishing.
- **Nivel 2:** reto de contraseñas seguras.
- **Nivel 3:** reto avanzado sobre autenticación en dos pasos.

---

## Características principales

- Juego 2D de plataformas.
- Personaje principal animado mediante sprites.
- Tres niveles jugables.
- Fondos con efecto parallax.
- Música diferente para el menú y cada nivel.
- Enemigos tipo drone con patrullaje.
- Terminales interactivos.
- Retos educativos de ciberseguridad.
- HUD con vidas representadas por corazones.
- Pantalla principal.
- Pantalla de controles.
- Pantalla de créditos.
- Pantallas de finalización por nivel.
- Generación de ejecutable para Windows con PyInstaller.

---

## Tecnologías utilizadas

- Python
- Pygame
- PyInstaller
- PyCharm / IntelliJ IDEA
- Sprites personalizados
- Imágenes generadas con IA
- Recursos de audio

---

## Estructura del proyecto

```text
pythonProject/
│
├── main_menu.py
├── nivel1.py
├── nivel2.py
├── nivel3.py
│
├── assets/
│   ├── Musica/
│   │   ├── Manu.mp3
│   │   ├── Nivel1.mp3
│   │   ├── Nivel2.mp3
│   │   └── Nivel3.mp3
│   │
│   └── sprites/
│       ├── Atlas/
│       ├── Cyber/
│       ├── Lana/
│       ├── Xenon/
│       └── Fondos/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Personajes

### Cyber

Cyber es el protagonista del juego. Es el personaje controlado por el jugador y debe infiltrarse en la red central para detener la propagación de Xenon.

### Lana

Lana actúa como aliada dentro de la narrativa del juego. Su presencia refuerza el acompañamiento del jugador durante la misión.

### Atlas

Atlas representa el soporte del equipo de defensa digital y aparece como parte de la historia del juego.

### Xenon

Xenon es el villano principal. Representa la amenaza digital que intenta comprometer el sistema.

---

## Controles

| Acción | Tecla |
|---|---|
| Mover a la izquierda | A / Flecha izquierda |
| Mover a la derecha | D / Flecha derecha |
| Saltar | W / Espacio / Flecha arriba |
| Interactuar con terminal | E |
| Responder retos | 1 / 2 / 3 |
| Volver / salir según pantalla | ESC |

---

## Niveles del juego

### Nivel 1: Phishing

El jugador debe avanzar por plataformas, evitar drones y resolver un reto relacionado con phishing.

Pregunta del reto:

```text
¿Cuál de estos correos es un intento de phishing?
```

El objetivo es identificar el correo sospechoso para desbloquear la puerta del nivel.

---

### Nivel 2: Contraseñas seguras

El segundo nivel presenta un reto sobre la creación de contraseñas seguras.

Pregunta del reto:

```text
¿Cuál de estas contraseñas es la más segura?
```

El jugador debe seleccionar la contraseña más robusta para continuar.

---

### Nivel 3: Seguridad avanzada

El último nivel presenta un reto relacionado con buenas prácticas de seguridad.

Pregunta del reto:

```text
¿Cuál de estas prácticas es más segura?
```

El objetivo es reconocer la importancia de la autenticación en dos pasos.

---

## Instalación

Primero, clona o descarga el proyecto.

Luego, instala las dependencias:

```bash
pip install -r requirements.txt
```

Si no tienes `requirements.txt`, puedes instalar Pygame manualmente:

```bash
pip install pygame
```

---

## Ejecución del juego

Desde la raíz del proyecto, ejecuta:

```bash
python main_menu.py
```

Esto abrirá la pantalla principal del juego.

---

## Generar ejecutable para Windows

Para generar el ejecutable, instala PyInstaller:

```bash
pip install pyinstaller
```

Luego ejecuta:

```bash
python -m PyInstaller --noconfirm --clean --windowed --name CyberGuardian --add-data "assets;assets" main_menu.py
```

El ejecutable se generará en:

```text
dist/CyberGuardian/CyberGuardian.exe
```

Para distribuir el juego, se recomienda comprimir la carpeta completa:

```text
dist/CyberGuardian/
```

No se debe entregar únicamente el archivo `.exe`, ya que la versión generada en modo carpeta necesita los archivos internos creados por PyInstaller.

---

## Archivos que no se deben subir al repositorio

El proyecto debe excluir archivos generados automáticamente o demasiado pesados, como:

```text
venv/
.venv/
build/
dist/
Installer/
__pycache__/
*.exe
*.spec
.idea/
```

Estos archivos deben estar registrados en `.gitignore`.

---

## Créditos

**Creador:**  
Eduar Ferney Rodríguez López

**Desarrollo:**  
Videojuego 2D desarrollado con Python y Pygame.

**Imágenes:**  
Imágenes generadas con IA - OpenAI.

**Efectos de sonido:**  
https://accounts.google.com/

**Uso:**  
Proyecto realizado con fines académicos y educativos.

---

## Estado del proyecto

El proyecto cuenta actualmente con:

- Menú principal funcional.
- Pantalla de controles.
- Pantalla de créditos.
- Tres niveles completos.
- Retos interactivos de ciberseguridad.
- Personaje animado.
- Enemigos tipo drone.
- Música por nivel.
- HUD mejorado.
- Pantallas finales.
- Generación de ejecutable para Windows.

---

## Autor

**Eduar Ferney Rodríguez López**

Proyecto académico desarrollado como videojuego educativo de ciberseguridad.
