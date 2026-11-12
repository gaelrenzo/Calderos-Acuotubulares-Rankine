# Balance térmico de un ciclo Rankine con caldero acuotubular

Artículo analítico en español, A4, dos columnas y diez páginas. Los cuatro autores y la afiliación figuran en `main.tex`. No representa mediciones de una instalación. Consultar `Verificacion_y_sustentacion.md` para el alcance, las discrepancias entre los insumos y el apoyo oral.

## Reproducir con LaTeX instalado

Se utilizó el MiKTeX ya instalado en esta máquina, con pdfLaTeX y BibTeX. No se sustituyó la distribución. La clase IEEEtran 1.8b y el estilo IEEEtran.bst 1.14 se incluyen sin modificar y conservan sus avisos LPPL. La opción `11pt` es una opción soportada de la clase; no se ajustaron márgenes, interlineado ni ancho de columnas.

Requisitos: Python 3.12 o posterior compatible con las versiones fijadas; `pdflatex`, `bibtex` y `pdftocairo` (o `pdftoppm`) en PATH. La ejecución verificada utilizó Python 3.14.0. En PowerShell, desde la carpeta del proyecto:

```powershell
python -m pip install -r requirements.txt
python scripts/compilar.py
```

El comando regenera propiedades, balances, sensibilidad, tablas y figuras; después ejecuta pdfLaTeX, BibTeX y dos pasadas adicionales de pdfLaTeX. Produce `Grupo1_Calderos_Acuotubulares.pdf` en esta carpeta y registra las comprobaciones en `build/`.

Si solo se desea recompilar el artículo con los resultados incluidos:

```powershell
python scripts/compilar.py --sin-modelo
```

Alternativa cuando latexmk y su intérprete Perl estén operativos:

```powershell
python scripts/modelo.py
latexmk -pdf main.tex
```

Los paquetes LaTeX son `fontenc`, `inputenc`, `babel` con español, `cite`, `amsmath`, `amssymb`, `graphicx`, `booktabs`, `array`, `hyperref` y `pgf`, habituales en MiKTeX o TeX Live. Una instalación mínima puede requerir incorporarlos. El proyecto no depende de una cuenta de Overleaf ni de un servicio de compilación en línea.

Las cuatro figuras se componen con el backend PGF de Matplotlib y el mismo pdfLaTeX instalado. Su preámbulo selecciona `ptm` con codificación T1: texto Times/Nimbus Roman y matemática Computer Modern, igual que en IEEEtran. Los rótulos y las escalas se verifican a su tamaño final, conservando PDF vectorial y fuentes incrustadas. `pdftocairo` genera las vistas PNG a partir del PDF ya compuesto, para que las dos versiones compartan la misma tipografía. La auditoría rechaza figuras con familias distintas de las usadas por el artículo.

## Archivos

- `main.tex`, `referencias.bib`: texto y referencias numéricas IEEE.
- `IEEEtran.cls`, `IEEEtran.bst`, `IEEEtran_README.txt`, `LPPL-1.3c.txt`: recursos y licencia de la plantilla.
- `scripts/modelo.py`: IF97, inversión de propiedades, balances, verificaciones y gráficos.
- `scripts/esquemas.py`: dibujos técnicos del ciclo y del caldero (solo matplotlib + pdfLaTeX).
- `scripts/contraste_tablas.py`: contraste IF97 vs. tablas SQLite de Tablas.KchaParedes (`--repo RUTA` para regenerar).
- `scripts/compilar.py`: compilación local y controles de salida.
- `scripts/auditar.py`, `scripts/empaquetar.py`: auditoría adicional y creación del ZIP portable.
- `datos/`: CSV con unidades, JSON con cifras y versiones, tablas y macros generadas.
- `figuras/`: cuatro figuras PDF vectoriales y vistas PNG generadas.
- `fuentes/Registro_de_fuentes.md`: enlaces, alcance de consulta y procedencia de la plantilla.
- `insumos/`: copias intactas de los documentos recibidos para trazabilidad; no se ejecutan como código.
- `Verificacion_y_sustentacion.md`: matriz de criterios, supuestos, verificación y guion oral.

## Modelo

Base: 8 MPa, 480 °C, 10 kPa y 10 kg/s. Caso ideal y variante con eficiencias isentrópicas de turbina 0,85 y bomba 0,80. `IF97::Water` es explícito: usar solamente `Water` seleccionaría otro backend. Las inversiones monofásicas resuelven las ecuaciones directas por bisección y los estados bifásicos usan propiedades saturadas y regla de mezcla. No se fuerza a cero el residuo energético.

Los CSV usan punto decimal para facilitar lectura informática; el artículo utiliza coma decimal. Las cifras del caso, los extremos de sensibilidad y las tablas se insertan desde archivos generados. No se redondean las entalpías antes del balance. Los puntos de verificación se conservan en `verificacion_IF97.csv`; la reproducción del ejemplo MIT se conserva en `comparacion_MIT.csv`.

Cambiar los supuestos exige revisar también los textos de interpretación y el número de páginas; el programa controla diez páginas para esta versión publicada. La identidad de datos y texto extraído es la comprobación de reproducción; los bytes de un PDF pueden cambiar por fechas y metadatos de compilación.

## Inspección del PDF

Las diez páginas se revisaron visualmente tras renderizarlas, además de controlar texto seleccionable, referencias, incrustación de fuentes, tamaño y ausencia de desbordamientos. Se utilizó `pdftoppm` de MiKTeX y se contrastó con PyMuPDF 2.1 para descartar artefactos del rasterizador en las líneas vectoriales. Para repetir el render, con `pdftoppm` en PATH:

```powershell
pdftoppm -r 150 -png Grupo1_Calderos_Acuotubulares.pdf build/pagina
pdffonts Grupo1_Calderos_Acuotubulares.pdf
pdfinfo Grupo1_Calderos_Acuotubulares.pdf
python scripts/auditar.py
```

No se necesita descargar los textos de referencia para ejecutar el modelo. Los enlaces documentan el método y su consulta; no se redistribuyen libros ni el código ASME completo.
