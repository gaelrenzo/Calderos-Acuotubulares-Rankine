# Verificación y sustentación del artículo de calderos acuotubulares

## Alcance y diferencias entre los documentos

Se desarrolló el artículo **Balance térmico de un ciclo Rankine con caldero acuotubular y evaluación de su desempeño energético**, con el alcance provisional descrito en el archivo de instrucciones. El resultado es un estudio documental y una simulación; no contiene mediciones ni representa una central visitada.

| Aspecto | Temario | Rúbrica | Captura de la actividad |
|---|---|---|---|
| Tema | Calderos acuotubulares, trece apartados | Central de vapor con ciclo Rankine | Centrales solares |
| Entrega | No precisa fecha | `[16/11/2026]` | 11/11/2026, 22:00 |
| Extensión | Desarrollo temático | 6–10 páginas con referencias | Promedio de 10 páginas |
| Formato | Sin plantilla impuesta | A4, Times New Roman 11 pt, sencillo | PDF a dos columnas, máximo 100 MB |
| Evaluación | No precisa ponderación | 20 puntos: 18 escritos y 2 orales | Texto 30 %, sustentación 70 % |
| Nombre de archivo | No precisa | No precisa | `Grupo1_Centrales_Solares` para la actividad solar |

Se adoptó **calderos acuotubulares** por coherencia con el temario y con el cálculo Rankine de la rúbrica, como propone el archivo de instrucciones. Esto no confirma que el docente haya cambiado la actividad solar. El plazo operativo del usuario se tomó como las **22:00 del 11 de noviembre de 2026, hora de Lima**. Las diferencias administrativas no aparecen como una fecha unificada en el artículo.

El PDF se llama `Grupo1_Calderos_Acuotubulares.pdf`. No se utilizó el nombre de centrales solares para ocultar la diferencia. No se enviaron archivos al aula virtual ni a terceros.

Se utilizó IEEEtran en modo conferencia con A4 y opción 11 pt, manteniendo márgenes, columnas e interlineado de la clase. La fuente de texto de su distribución es Times compatible **Nimbus Roman**, incrustada; no es la fuente propietaria Times New Roman literal. Esta elección conserva la tipografía de la plantilla de referencia y debe distinguirse de una coincidencia exacta con la fuente indicada por la rúbrica. El formato no implica publicación ni aceptación IEEE.

La afiliación de trabajo procede del archivo de instrucciones: Escuela Profesional de Ingeniería Mecánica Eléctrica, Universidad Nacional del Altiplano, Puno, Perú. Se conservaron el orden y los cuatro nombres acreditados por el temario; no se agregaron correos, ORCID, códigos, docente ni financiación.

## Matriz de la rúbrica

Las páginas corresponden a la versión final de diez páginas. Se indica evidencia; no se garantiza calificación.

| Criterio | Puntaje máximo | Evidencia en el artículo y proyecto |
|---|---:|---|
| Cuadro de propiedades | 3 | Tabla III, p. 6: p, T, h, s, v, título y fase en cuatro estados. Tabla V, p. 8: variante no ideal. `datos/estados.csv`. |
| Procedimiento de propiedades | 3 | III-C, pp. 3–4: pares independientes de cada estado, bisección, saturación y reglas de mezcla. Ecs. 4–8. `scripts/modelo.py`. |
| Masa y energía en cuatro componentes | 4 | III-D, pp. 4–5; ecs. 9–17. Sustituciones en ecs. 25–31 y tabla IV, p. 6. Caudal de 10 kg/s conservado. |
| Eficiencia térmica y análisis | 3 | Ecs. 15–16 y 29–30; tabla IV. Variante irreversible; barridos de temperatura y dos presiones. Diferenciación de eficiencia de ciclo, caldero y combustible. |
| Diagrama T-s | 2 | Figura 3, p. 7: campana IF97, estados 1–4, sentido, escala, unidades, isóbaras y trayectorias calculadas. `datos/trayectorias_Ts.csv`. |
| Estructura y formato | 2 | Título, autores, resumen de 223 palabras, seis palabras clave, introducción, metodología, resultados, discusión, conclusiones y referencias. Diez páginas A4, dos columnas, 11 pt. Salvedad de fuente indicada arriba. |
| Redacción y referencias | 1 | Dieciséis referencias citadas y resueltas mediante BibTeX/IEEEtran; enlaces y alcance documentados. Sin citas ficticias ni referencias de ejemplo. |
| Sustentación | 2 | Guion de diez minutos y preguntas de discusión al final de esta nota. La evaluación depende del dominio y exposición de los integrantes. |

## Cobertura de los trece apartados del temario

| Apartado | Cobertura |
|---|---|
| 1. Introducción, definición y evolución | Sección I, p. 1; definición de equipo y contexto histórico. |
| 2. Fundamentos | II-B y III: transferencia, circulación, propiedades y ciclo; VI-A: combustión. |
| 3. Clasificación | II-A, pp. 1–2; tabla I: acuotubular/pirotubular, domos, A/D/O, presión, circulación y combustibles. |
| 4. Componentes | II-C y figura 1, pp. 2–3: domos, tubos, hogar, economizador, sobrecalentador, aire y gases; recalentador distinguido del caso simple. |
| 5. Funcionamiento | II-C y figura 1: recorridos; VI-A: arranque, operación y parada. |
| 6. Instrumentación y control | VI-A, p. 9: señales de presión, temperatura y caudal; nivel de uno, dos y tres elementos, llama y protecciones. |
| 7. Agua y purgas | VI-B, p. 9: depósitos, corrosión, arrastre, tratamientos y extensión de balance con purga. |
| 8. Capacidad y balance | III-D a III-G y IV: kg/h, MW, BHP, método directo/indirecto, consumo y pérdidas agregadas. |
| 9. Ventajas y limitaciones | Tabla I y VI-C, pp. 9–10. |
| 10. Aplicaciones | VI-C: centrales, minería según demanda, azúcar, papel, petroquímica, uso naval y HRSG. |
| 11. Mantenimiento y seguridad | VI-C: limpieza, inspecciones, espesores, fallas, pruebas y alcance de ASME/Ley 29783. |
| 12. Conclusiones | VII, p. 10, vinculadas a los resultados calculados. |
| 13. Bibliografía | Dieciséis fuentes, pp. 10; archivo `referencias.bib` y registro de consulta. |

## Datos, supuestos y resultados

Las entradas seleccionadas son **8 MPa, 480 °C, 10 kPa y 10 kg/s**; no se cuenta con aprobación documentada del docente para esos valores ni se presentan como datos asignados. El líquido sale saturado del condensador; no se consideran pérdidas de presión, variaciones cinéticas o potenciales, extracciones, fugas, auxiliares externos ni purga en el caso base. La bomba y la turbina son adiabáticas. El caso ideal tiene eficiencias isentrópicas unitarias; el segundo caso adopta 0,85 en turbina y 0,80 en bomba.

| Magnitud | Ideal | No ideal |
|---|---:|---:|
| Trabajo de bomba [kJ/kg] | 8,058356 | 10,072944 |
| Trabajo de turbina [kJ/kg] | 1240,195557 | 1054,166223 |
| Calor recibido [kJ/kg] | 3149,656039 | 3147,641451 |
| Calor rechazado [kJ/kg] | 1917,518838 | 2103,548172 |
| Trabajo neto [kJ/kg] | 1232,137201 | 1044,093279 |
| Eficiencia del ciclo [%] | 39,119738 | 33,170655 |
| Potencia neta de eje [MW] | 12,321372 | 10,440933 |
| Título de escape | 0,801613 | 0,879382 |
| Residuo [kJ/kg] | -2,273737 × 10⁻¹³ | 4,547474 × 10⁻¹³ |

Las propiedades proceden de **IAPWS-IF97 mediante CoolProp 8.0.0**, con `IF97::Water`. Se ejecutó Python 3.14.0, NumPy 2.5.4 y Matplotlib 3.11.2. Los pares son (p,x) en 1, (p,s) en 2 ideal, (p,T) en 3 y (p,s) en 4 ideal. La variante obtiene las salidas a partir de (p,h). En región monofásica se usa bisección de las ecuaciones directas; en mezcla, extremos de saturación y regla de mezcla. Las cifras impresas se redondean después de calcular.

La eficiencia del caldero **0,90 sobre PCI**, el combustible representado por metano con **PCI nominal de 50 000 kJ/kg** y el factor eléctrico **0,97** son supuestos de escenario. No se dispone de composición, análisis calorimétrico ni datos de gases para medir pérdidas individuales. El complemento de 0,90 es pérdida agregada implícita; no es una auditoría indirecta. El rendimiento eléctrico reducido no incluye todos los auxiliares de una central.

Sensibilidad: cinco valores para cada una de las tres variables, manteniendo las demás entradas constantes, en ambos modelos. Los CSV incluyen 30 ejecuciones de barrido, aunque la condición base se repite en cada serie. No son 30 ensayos independientes ni observaciones estadísticas. La tabla de estados y las figuras se regeneran desde el programa. Las trayectorias T-s no se trazaron uniendo estados arbitrariamente.

El ejemplo de purga del 2 % es una extensión local, excluida del ciclo cerrado tabulado. El caudal de refrigeración es una estimación por calor sensible con cp y ΔT supuestos; no representa consumo de reposición ni un diseño de torre.

## Fuentes y verificaciones numéricas

Se verificaron h, s y v frente a los tres puntos de la tabla 5 de la release IF97 (300 K a 3 MPa; 300 K a 80 MPa; 500 K a 3 MPa). El mayor error relativo fue **2,81 × 10⁻⁹**, inferior al umbral 10⁻⁷. Ver `datos/verificacion_IF97.csv`.

Se reprodujo además el caso docente MIT a 3 MPa, 460 °C y 7,384 kPa: **35,89509 %**, frente a **35,9 %** de la referencia; el título fue **0,851695**, frente a **0,851** del documento. El rendimiento concuerda al redondeo; el título muestra una diferencia pequeña por las propiedades tabuladas originales. Ver `datos/comparacion_MIT.csv`. Esta comparación no valida una central real.

Los textos completos del aula virtual no estaban entre los archivos recibidos. No se afirmó haberlos leído. Se utilizaron las fuentes públicas del registro `fuentes/Registro_de_fuentes.md`. La referencia sugerida de Çengel no se reutilizó sin consulta suficiente. Babcock & Wilcox se limita a la muestra pública; ASME, a la ficha editorial; el registro de Ley 29783 se utiliza sin afirmar una evaluación jurídica consolidada. La referencia del artículo de CoolProp se verificó en la documentación oficial del software.

## Guion de diez minutos

| Tiempo | Integrante sugerido | Explicación y apoyo |
|---|---|---|
| 0:00–2:15 | Aquiles Taylor Ramos Yapo | Presentar pregunta y objetivo. Explicar acuotubular frente a pirotubular y el recorrido del ciclo en figura 2. Declarar que es un caso analítico con entradas elegidas. Distinguir la frontera agua–vapor de la del combustible. |
| 2:15–4:45 | Renzo Gabriel Mamani Galindo | Usar tabla III y figura 3. Explicar los pares independientes; por qué saturación necesita título; qué significa «no aplica». Mostrar x₄=(s₃−s_f)/(s_g−s_f) y describir IF97. No memorizar seis decimales: comprender presión, fase y unidades. |
| 4:45–7:15 | Dilmar Humberto Siguayro Coila | Derivar el balance estacionario y aplicarlo a los cuatro equipos. Sustituir entalpías en trabajo neto y eficiencia. Presentar 12,32 MW y 39,12 %. Explicar el residuo y por qué un cierre algebraico no prueba exactitud experimental. Comparar 33,17 % no ideal. |
| 7:15–10:00 | Steven Alex Mayta Lampa | Interpretar figura 4: aumentar T mejora título; bajar p_c o subir p_b puede aumentar humedad. Diferenciar 90 % del caldero de 39,12 % del ciclo. Cerrar con límites: refrigeración, materiales, agua, purgas y falta de mediciones. |

Ensayo recomendado: respetar los cortes de tiempo y que cada integrante pueda explicar cualquier estado y componente. Las tablas completas están en el artículo; durante la exposición conviene señalar solo las filas necesarias.

## Preguntas para cinco minutos de discusión

1. **¿Por qué p y T no bastan en saturación?** Porque están ligados por la curva de saturación. Se necesita título u otra propiedad que identifique la fracción de vapor.
2. **¿Por qué no hay título en 2 y 3?** Son líquido comprimido y vapor sobrecalentado. El título describe una mezcla bifásica en equilibrio.
3. **¿39,12 % es la eficiencia del caldero?** Es la eficiencia del ciclo respecto del calor recibido por el agua. El 90 % supuesto relaciona ese calor con el combustible; su producto da 35,21 % combustible–eje ideal.
4. **¿Cómo puede bajar la humedad cuando empeora la turbina?** La expansión irreversible extrae menos trabajo y deja mayor entalpía en el escape. Mejora el título a esa presión, pero reduce potencia y aumenta el rechazo térmico.
5. **¿Por qué no elegir siempre la menor presión del condensador?** Por humedad, vacío, volumen de escape, capacidad de refrigeración y condiciones ambientales. El barrido no optimiza costos ni dimensiones.
6. **¿Un residuo casi cero demuestra que el modelo es realista?** No. El balance se cierra algebraicamente con las mismas entalpías. Los puntos IAPWS y el caso MIT comprueban implementación y procedimiento, no una instalación.
7. **¿Por qué usar `IF97::Water`?** Para seleccionar explícitamente la formulación industrial pedida. `Water` solo utiliza otro backend por defecto.
8. **¿Por qué el consumo de combustible no ideal baja levemente a caudal fijo?** Porque la bomba añade más entalpía al agua y reduce ligeramente el calor externo necesario. La potencia neta cae mucho más; no es una mejora de consumo por unidad de trabajo.
9. **¿Qué limita un acuotubular?** Circulación, materiales, control y calidad del agua. El menor diámetro ayuda frente a presión, pero no elimina el peligro ni la necesidad de inspección.
10. **¿Qué falta para evaluar una central?** Medidas con incertidumbre, auxiliares, pérdidas de presión, composición de combustible, condiciones de refrigeración, purgas y datos del fabricante.

Priorizar cuatro o cinco preguntas según el tiempo. La discrepancia con el tema solar es administrativa y está registrada; no debe presentarse una confirmación docente inexistente.

## Registro final de entrega

### Cambios del 11/11/2026 (cierre)

- **Figuras 1 y 2 rehechas como dibujos técnicos** (`scripts/esquemas.py`): caldero de dos domos en corte (hogar con paredes de agua, quemador, haz convectivo, descendente, sobrecalentador, economizador, precalentador de aire, ventilador, chimenea y purga) y ciclo con símbolos de equipo (turbina con generador, condensador de superficie con haz de tubos, bomba centrífuga con motor). Sustituyen a los diagramas de bloques. Son ilustrativos y no a escala.
- **Contraste con las tablas del grupo** ([Tablas.KchaParedes](https://github.com/dilmar231gabriel-ops/Tablas.KchaParedes), commit 6b33d48): el mismo caso (8 MPa, 480 °C, 10 kPa) resuelto con la base SQLite e interpolación lineal se compara con IF97 en la tabla III del artículo. Las diferencias en h1–h4, x4 y η son menores de 0,04 % (η = 39,12 % en ambos). Script: `scripts/contraste_tablas.py`; datos: `datos/contraste_tablas.csv` y `datos/tablas_kchaparedes_solution.json`. Se añadió la referencia [9].
- Recompilado: 10 páginas A4, sin cajas desbordadas ni referencias indefinidas.


Comprobaciones completadas el 11 de noviembre de 2026, antes de las 22:00 de Lima:

- **Compilación local:** MiKTeX 24.1, pdfTeX 1.40.25 y BibTeX 0.99d instalados en la máquina. Secuencia pdfLaTeX → BibTeX → pdfLaTeX → pdfLaTeX, sin errores, citas o referencias indefinidas, caracteres ausentes ni desbordamientos `Overfull`.
- **Composición:** diez páginas A4, cuerpo a dos columnas, título y autores a ancho completo. Sin portada separada, índice, páginas vacías ni textos de plantilla. Tablas y figuras numeradas y citadas. Texto seleccionable en las diez páginas.
- **Resumen y referencias:** 223 palabras, seis palabras clave, 16 entradas bibliográficas citadas y 16 destinos HTTPS distintos en el PDF. No hay referencias sin citar ni claves sin resolver.
- **Fuentes:** todas las fuentes detectadas por `pdffonts` están incrustadas, incluidas las de las figuras vectoriales. Se conserva la salvedad de Nimbus Roman frente a Times New Roman literal.
- **Inspección visual:** se revisaron las páginas 1 a 10. Se renderizó con `pdftoppm` de MiKTeX y se contrastó con PyMuPDF 2.1 porque el primer rasterizador generaba artefactos en líneas vectoriales; el contraste confirmó trazos continuos en el PDF. Se verificaron rótulos, tablas, ecuaciones y ausencia de superposiciones o cortes.
- **Tamaño:** 398 690 bytes, aproximadamente 0,40 MB, por debajo de 100 MB.
- **Reproducción:** se extrajo el ZIP a una carpeta nueva, se regeneraron datos y figuras y se compiló nuevamente con el mismo MiKTeX. El PDF regenerado tiene diez páginas y texto extraído idéntico. Doce archivos de datos, propiedades, trayectorias, macros y tablas se compararon byte a byte y coincidieron. Los bytes del PDF difieren por metadatos de fecha, como es esperable.
- **Integridad:** CRC del ZIP comprobado. Se incluyen clase, estilo BibTeX y licencia, código, datos, figuras, bibliografía, instrucciones de reproducción, copias de insumos y esta nota. Se excluyen cachés, renders intermedios y PDFs ajenos. Se verificaron los SHA-256 de los originales, que permanecen intactos.

Los registros legibles por máquina están en `datos/validacion_pdf.json`, `datos/revision_figuras.json` y `datos/reproduccion_verificada.json`. La huella del texto extraído es `7ce4d8a698f0314fd27e22b1176893ef5397493395a1b0036df4d6a52c8a5e05`.

El PDF está completo bajo el alcance acuotubular adoptado. La correspondencia con la actividad solar de la captura y la aprobación docente de los datos elegidos no quedan acreditadas por los archivos disponibles. Esta salvedad administrativa no se oculta mediante cambios de título o nombre de archivo.
