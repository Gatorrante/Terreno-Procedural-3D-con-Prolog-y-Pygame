[![English](https://img.shields.io/badge/lang-English-blue)](#english) [![Español](https://img.shields.io/badge/lang-Español-red)](#español)
--------------------------------------------------------------------------------------------------------------------------------------------
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0.1-green)](https://www.pygame.org/)
[![Prolog](https://img.shields.io/badge/Prolog-SWI--Prolog-orange)](https://www.swi-prolog.org/)

# English

## Procedural 3D Terrain with Prolog and Pygame

This project generates a 3D terrain procedurally using Perlin noise and rules defined in Prolog. The terrain is rendered in real-time using Pygame. The height and color of the terrain are determined by queries to Prolog, allowing for dynamic and varied landscape generation.

![Terrain Demo](terrain_demo.gif)

### Technologies Used
- Python 3.8+
- Pygame 2.0.1
- SWI-Prolog
- PySWIP
- Noise

### How to Run
1. Install the required dependencies:
    ```sh
    pip install pygame pyswip noise
    ```
2. Ensure you have SWI-Prolog installed and accessible from your PATH. You can download it from [SWI-Prolog](https://www.swi-prolog.org/Download.html).
3. Run the `terreno.py` script:
    ```sh
    python terreno.py
    ```

### Project Structure

### Description
- **generador.pl**: Prolog rules for determining terrain height and color.
- **terreno.py**: Main Python script that generates and renders the terrain.
- **README.md**: Project documentation.
- **terrain_demo.gif**: Animated demonstration of the terrain generation.

---

# Español

## Terreno Procedural 3D con Prolog y Pygame

Este proyecto genera un terreno 3D de manera procedural utilizando ruido Perlin y reglas definidas en Prolog. El terreno se renderiza en tiempo real utilizando Pygame. La altura y el color del terreno se determinan mediante consultas a Prolog, lo que permite una generación dinámica y variada del paisaje.

![Demostración del Terreno](terrain_demo.gif)

### Tecnologías Utilizadas
- Python 3.8+
- Pygame 2.0.1
- SWI-Prolog
- PySWIP
- Noise

### Cómo Ejecutar
1. Instalar las dependencias requeridas:
    ```sh
    pip install pygame pyswip noise
    ```
2. Asegúrate de tener SWI-Prolog instalado y accesible desde tu PATH. Puedes descargarlo desde [SWI-Prolog](https://www.swi-prolog.org/Download.html).
3. Ejecuta el script `terreno.py`:
    ```sh
    python terreno.py
    ```

### Descripción
- **generador.pl**: Reglas de Prolog para determinar la altura y el color del terreno.
- **terreno.py**: Script principal de Python que genera y renderiza el terreno.
- **README.md**: Documentación del proyecto.
- **terrain_demo.gif**: Demostración animada de la generación del terreno.
