Se utilizó asistencia de inteligencia artificial (del tipo sugerencias de línea de código / Inline Suggestions), así como unas cuantos prompts (ambas herramientas de Copilot Chat en VSCode).

Los prompts se señalarán a continuación:

"En detalles.html, necesito que el botón Comprar (línea 58), dirija a comprar.html, cumpliendo la lógica que involucra views.py y urls.py para su inclusión."

r - Hecho: el botón Comprar en detalle.html ahora enlaza a la ruta nombrada catalogo:comprar. Añadí la vista que renderiza comprar.html en views.py y registré la ruta en urls.py.

Verificación: python manage.py test catalogo pasó correctamente.

Archivos que alteró: 
- test.py
- urls.py (catalogo)
- detalle.html
- views.py

---

"Al hacer click en comprar, me dirije a una página en blanco, no a "comprar.html""

r - La vista y la ruta ya servían comprar.html; la página aparecía en blanco porque su <main> estaba vacío. Ahora la plantilla muestra el título Comprar cómic, un mensaje y un enlace para volver al catálogo: comprar.html.

Verifiqué el cambio con python manage.py test catalogo; pasó correctamente. Actualiza la página en el navegador para ver el contenido.

Archivos que modificó:
comprar.html
test.py
//Ningún cambio relevante. La confusión se debió al utilizar la estructura de bs5 y los constantes errores que no me dejaban ver algo del formulario desechado antes de volver a la versión anterior del proyecto.

---

"una vez clickeado el botón "comprar" cuando se está en los detalles de un cómic, necesito que aquel botón de lleve a "compra.html" (esa parte ya está ok), lo que seguiría sería el presentarle al usuario un formulario, en donde se muestren los campos a rellenar, los cuales serían el nombre del cliente, su RUT, su correo y la cantidad de ejemplares."

r - Implementé el formulario en comprar.html con los campos nombre del cliente, RUT, correo y cantidad de ejemplares. El botón conserva el cómic seleccionado y abre su formulario correspondiente.

Al confirmar, se registra una reserva y se actualiza el stock; el formulario impide pedir más ejemplares de los disponibles. Las cuatro pruebas de catálogo pasaron con python manage.py test catalogo.

Archivos que modificó:
- forms.py
- views.py
- comprar.html
- detalle.html
- urls.py
- tests.py

---

"Gracias, necesito una validación del RUT, pues se pueden escribir letras (aparte de la K).

r - Agregué validación al campo RUT en `forms.py`: acepta números, separadores habituales y `K` solo como dígito verificador; normaliza `k` a `K` y rechaza otras letras. La validación también se aplica en el servidor, no solo en el navegador.

Verifiqué los casos con `python manage.py test catalogo`; las 6 pruebas pasaron.

Archivos que modificó:
- forms.py
- tests.py