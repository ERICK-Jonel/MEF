

# Proyecto MEF (Máquinas de Estados Finitos)

Este proyecto es una herramienta modular para definir, ejecutar y visualizar máquinas de estados finitos. Está dirigido a desarrolladores con conocimientos intermedios en Python y en teoría de autómatas, especialmente pensado para programadores de la Universidad UCLA. Aunque se encuentra en fase de desarrollo, el sistema es completamente funcional.

## Objetivos

- **Definir y ejecutar máquinas de estados:** Permite modelar estados y transiciones de forma flexible.
- **Visualización e integración:** Incorpora módulos para la generación de diagramas y una interfaz gráfica básica.
- **Enfoque modular:** Facilita la extensión y experimentación mediante una clara separación de responsabilidades.

## Estructura del Proyecto

La distribución de archivos es la siguiente:

```
config.py  
env/  
fsm_diagram/  
fsm_diagram.png  
fsm_gui.py  
fsm_logic.py  
main.py  
"MEF if.py"  
__pycache__/  
requirements.txt  
scr/
```

> **Nota:** La carpeta `scr` contiene algunas imágenes y fragmentos de código no esenciales para la funcionalidad principal.

## Cómo Usar el Proyecto

### 1. Descargar o Clonar el Repositorio (Windows)

Tienes dos opciones para obtener el proyecto:

- **Descargar ZIP:**  
  Accede al [repositorio en GitHub](https://github.com/ERICK-Jonel/MEF) y descarga el archivo ZIP del proyecto.

- **Clonar el repositorio:**  
  Abre la terminal en Windows y ejecuta el siguiente comando:
  ```bash
  git clone https://github.com/ERICK-Jonel/MEF.git
  ```

### 2. Activar el Entorno Virtual

El proyecto incluye un entorno virtual dentro de la carpeta `env`. Actívalo con:
```bash
env\Scripts\activate
```

### 3. Instalar las Dependencias

Con el entorno virtual activado, instala las dependencias necesarias ejecutando:
```bash
pip install -r requirements.txt
```

### 4. Instalar Graphviz

Para generar los diagramas, es obligatorio contar con [Graphviz](https://graphviz.org). Asegúrate de instalarlo y de agregarlo al PATH de tu sistema Windows.  
*Consulta la documentación oficial de Graphviz para más detalles sobre la instalación.*

### 5. Cargar y Ejecutar una Máquina

La sintaxis básica para cargar una máquina de estados está definida en los módulos del proyecto. En líneas generales, deberás:

1. Configurar la máquina ajustando la definición de estados y transiciones en el archivo correspondiente (por ejemplo, en `fsm_logic.py` o mediante archivos de configuración).
2. Ejecutar el programa principal con:
   ```bash
   python main.py
   ```
   
Consulta los comentarios y ejemplos incluidos en el código para conocer la sintaxis exacta utilizada al definir estados y transiciones.

## Notas Adicionales

- **Público objetivo:** Desarrolladores de la Universidad UCLA con conocimientos en Python y teoría de autómatas.
- **Fase de desarrollo:** Aunque el proyecto está en desarrollo, ya es completamente funcional. Se planean futuras mejoras en la documentación y nuevas funcionalidades.
- Las contribuciones son bienvenidas a través de _pull requests_ o la apertura de _issues_ en el repositorio GitHub.

---
