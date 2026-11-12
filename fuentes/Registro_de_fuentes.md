# Registro de fuentes y límites de consulta

Consulta realizada el 11 de noviembre de 2026. Se distinguieron documentos originales recibidos, fuentes técnicas públicas, referencias editoriales y resultados propios. Las páginas se abrieron y se leyó su contenido pertinente; no se tomaron datos de una central real ni de artículos no disponibles del aula.

| Fuente | Evidencia utilizada | Alcance |
|---|---|---|
| [IAPWS R7-97(2012)](https://iapws.org/technical-guidance/release/IF97-Rev) y [release PDF](https://iapws.org/technical-guidance/release/IF97-Rev.download) | Definición IF97, regiones y tabla 5 | Se descargó y extrajo el PDF de 49 páginas. Se usaron los tres puntos de la tabla 5 para comprobar h, s y v. |
| [CoolProp IF97](https://coolprop.org/fluid_properties/IF97.html) | Backend `IF97::Water`, unidades y distinción respecto de `Water` | Software ejecutado: 8.0.0. |
| [Cita oficial de CoolProp](https://coolprop.org/citation.html) | Bell, Wronski, Quoilin y Lemort, 2014, vol. 53(6), pp. 2498–2508; DOI 10.1021/ie4033999 | Metadatos verificados en la documentación del software; no se atribuye lectura del artículo completo. |
| [Babcock & Wilcox, muestra Steam 42](https://www.babcock.com/assets/PDF-Downloads/Steam-42-Sample.pdf) | Portada, copyright, edición 42, editor Gregory L. Tomei, año 2015 y contexto introductorio | Muestra pública de 17 páginas; no libro completo. No se redistribuye en el ZIP. |
| [Spirax Sarco, Water Tube Boilers](https://www.spiraxsarco.com/learn-about-steam/the-boiler-house/water-tube-boilers) | Configuración, presión, circulación y secciones | Documento técnico del fabricante, sin fecha editorial atribuida. |
| [Boiler Efficiency and Combustion](https://www.spiraxsarco.com/learn-about-steam/the-boiler-house/boiler-efficiency-and-combustion) | Bases caloríficas, aire y pérdidas | No se usan sus apartados históricos de legislación como normativa actual. |
| [Water for the Boiler](https://www.spiraxsarco.com/learn-about-steam/the-boiler-house/water-for-the-boiler) | Depósitos, corrosión, arrastre y tratamiento | Síntesis general; sin dosis ni límites de química supuestos. |
| [Methods of Detecting Water Level](https://www.spiraxsarco.com/learn-about-steam/the-boiler-house/methods-of-detecting-water-level-in-steam-boilers) | Señales de nivel, alarmas y funciones de protección | No se trasladan exigencias británicas como obligaciones peruanas. |
| [Automatic Level Control Systems](https://www.spiraxsarco.com/learn-about-steam/the-boiler-house/automatic-level-control-systems) | Control de uno, dos y tres elementos | Marco explicativo, sin parametrizar un controlador real. |
| [Controlling TDS](https://www.spiraxsarco.com/learn-about-steam/the-boiler-house/controlling-tds-in-the-boiler-water) | Concentración de sólidos y conductividad | Se distingue descripción de purgas del circuito cerrado calculado. |
| [Boiler Ratings](https://www.spiraxsarco.com/learn-about-steam/the-boiler-house/boiler-ratings) | Evaporación convencional y BHP | Equivalencia aproximada 15,65 kg/h desde y a 100 °C, unos 9,81 kW. |
| [Carmichael, Rankine Cycle, MIT OCW](https://ocw.mit.edu/courses/2-611-marine-power-and-propulsion-fall-2006/resources/09rankine/) | PDF de cinco páginas, fechado 24/10/2005; 3 MPa, 460 °C, 7,384 kPa, eficiencia 0,359 y título 0,851 | Se abrió el PDF completo y se inspeccionaron sus páginas pertinentes. Se reprodujeron sus condiciones con el modelo; la discrepancia pequeña en título se explica por las tablas de origen. Curso publicado como otoño de 2006; el documento está fechado en 2005. |
| [Carmichael, Rankine Cycle vs. Pressure and Temperature](https://ocw.mit.edu/courses/2-611-marine-power-and-propulsion-fall-2006/resources/10rankine_v_p_t/) | PDF de cuatro páginas fechado 14/10/2005 | Barridos de presión y temperatura; comparación cualitativa y uso de temperatura media de aporte. |
| [EPA, Catalog of CHP Technologies, Section 4](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P1010CJX.TXT) | Septiembre de 2014; autores Darrow, Tidball, Wang y Hampson; fronteras, aplicaciones y referencia 33–45 % sobre PCS | Rango contextual del documento, no estadística actual de 2026 ni validación de una planta de 12 MW. |
| [ASME BPVC.I-2025](https://www.asme.org/codes-standards/find-codes-standards/bpvc-i-bpvc-section-i-rules-construction-power-boilers) | Ficha oficial y denominación Rules for Construction of Power Boilers | Sin acceso al código íntegro; no se certifica diseño ni cumplimiento. |
| [Ley 29783, registro del Congreso](https://www.leyes.congreso.gob.pe/DetLeyNume_1p.aspx?xNorma=6&xNumero=29783&xTipoNorma=0) | Título y fecha oficial de publicación, 20/08/2011 | Los intentos de obtener el PDF de la ley devolvieron 403. Se utilizó únicamente el registro oficial y no se afirmaron artículos específicos ni una revisión legal consolidada. |

La referencia sugerida de Çengel, Boles y Kanoğlu no se incorporó: no se dispuso de texto consultado suficiente para usarla como respaldo. Tampoco se incorporaron los artículos del aula, que no estaban entre los archivos disponibles. Se prefirieron documentos públicos efectivamente abiertos.

## Plantilla

Se consultaron el [IEEE Author Center](https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/authoring-tools-and-templates/) y la [plantilla oficial en Overleaf](https://www.overleaf.com/latex/templates/ieee-conference-template/grfzhhncsfqn). El proyecto utiliza IEEEtran en modo `conference`, papel A4 y opción soportada `11pt`.

Los recursos se obtuvieron de CTAN:

- [IEEEtran.cls](https://mirrors.ctan.org/macros/latex/contrib/IEEEtran/IEEEtran.cls), versión 1.8b, 26/08/2015.
- [IEEEtran.bst](https://mirrors.ctan.org/macros/latex/contrib/IEEEtran/bibtex/IEEEtran.bst), versión 1.14.
- [README de distribución](https://mirrors.ctan.org/macros/latex/contrib/IEEEtran/README).
- [Licencia LPPL 1.3c](https://www.latex-project.org/lppl/lppl-1-3c.txt).

Se conservaron los avisos de contribución y licencia. Se retiraron textos, autores y bibliografía de ejemplo. El uso del formato no implica envío, aceptación ni publicación IEEE.
