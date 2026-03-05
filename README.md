<div align="center">

# Tetris

**Un clásico reimaginado en Python**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.0-00B140?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org/)
[![Status](https://img.shields.io/badge/Estado-Completado-success?style=for-the-badge)]()
[![Materia](https://img.shields.io/badge/Materia-Objetos%20%26%20Abstracción-purple?style=for-the-badge)]()

</div>

---

## 📖 Sobre el Proyecto

**Tetris** es un juego de bloques desarrollado como **módulo** del proyecto **Arcade Machine**, en el marco de la materia **Taller de Objetos y Abstracción de Datos.**

El juego recrea la experiencia clásica del Tetris con soporte para múltiples rulesets, sistema de records, controles configurables y una arquitectura orientada a objetos construida desde cero en Python con Pygame.

> *"Siete piezas. Infinitas posibilidades."*

---

## 🎮 Características

- 🧩 **Múltiples Rulesets** — Modos de juego con distintas reglas de gravedad, bloqueo y mecánicas
- 🏆 **Sistema de Records** — Tabla de puntajes por ruleset con persistencia en base de datos local
- ⚙️ **Controles Configurables** — Editor de keybinds con soporte para múltiples teclas por acción
- 🎵 **Gestión de Audio** — Música, efectos de sonido y control de volumen integrado
- 👻 **Ghost Piece** — Visualización de dónde caerá la pieza activa
- 🔄 **Hold** — Guarda una pieza para usarla después *(disponible según ruleset)*
- ✨ **T-Spin Detection** — Detección de maniobras especiales con puntaje adicional
- 📊 **HUD en tiempo real** — Score, nivel y líneas actualizados frame a frame

---

## 🕹️ Cómo Jugar

| Acción | Tecla por defecto |
|--------|-------------------|
| Mover izquierda / derecha | `← →` |
| Bajar (soft drop) | `↓` |
| Caída instantánea (hard drop) | `Espacio` |
| Rotar derecha / izquierda | `X` / `Z` |
| Hold | `C` |
| Pausa | `P` |

> Los controles son completamente reasignables desde el menú de **Opciones → Controles**.

---

## 🚀 Instalación

### Requisitos

- **Python 3.11** o superior — [Descargar aquí](https://www.python.org/downloads/)
- **Pygame 2.6.0** o superior
- **pip actualizado:**
  ```bash
  python -m pip install --upgrade pip
  ```

---

### Paso 1: Instalar el SDK de Arcade Machine

Este juego forma parte del ecosistema **Arcade Machine** y requiere su SDK como dependencia base.

#### Opción A — Desde PyPI *(recomendado)*
```bash
pip install arcade-machine-sdk
```

> ⚠️ En algunos sistemas puede ser necesario usar `python -m pip install arcade-machine-sdk`.

#### Opción B — Desde GitHub *(versión de desarrollo)*
```bash
pip install git+https://github.com/Neritoou/arcade-machine-sdk.git
```

#### Verificar instalación del SDK
```bash
python -c "from arcade_machine_sdk import GameBase; print('SDK instalado correctamente')"
```

Si ves el mensaje de confirmación, ¡el SDK está listo!

#### Actualizar el SDK

Desde PyPI:
```bash
pip install --upgrade arcade-machine-sdk
```

Desde GitHub:
```bash
pip install --upgrade --force-reinstall git+https://github.com/Neritoou/arcade-machine-sdk.git@main
```

---

### Paso 2: Clonar el repositorio del juego

```bash
git clone https://github.com/Neritoou/tetris.git
cd tetris
```

### Paso 3: Instalar dependencias del juego

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar

```bash
python main.py
```

---

# 👥 Equipo de Desarrollo


- Agostinho Dos Santos

- Odett Sayegh

---

## 🙏 Créditos

### 🎨 Assets
- **Andrea Zabala** — Contribución en los assets visuales del juego

---

## 📚 Contexto Académico

Este proyecto fue desarrollado como módulo evaluativo de la materia **Taller de Objetos y Abstracción de Datos**, aplicando conceptos de:

- Programación Orientada a Objetos (POO)
- Abstracción, encapsulamiento, herencia y polimorfismo
- Patrones de diseño: State Machine, Strategy, Facade, Factory
- Arquitectura modular y separación de responsabilidades
- Gestión de recursos, audio y entrada del usuario

---
</div>