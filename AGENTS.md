# AGENTS

Instrucciones para agentes de IA. Antes de cualquier fase, lee [`WORKFLOW.md`](WORKFLOW.md) (flujo, paradas y mapa de documentación); sigue las convenciones de [`CONTRIBUTING.md`](CONTRIBUTING.md). Aquí solo está lo específico de la IA.

## 1. Principios

- Entre las paradas ⏸ de WORKFLOW, encadena los pasos sin esperar órdenes e informa al llegar a la siguiente. Detente antes solo ante una ambigüedad que cambie el resultado.
- No inventes decisiones de producto: pregunta o regístralas como pregunta abierta.
- Nunca afirmes que una comprobación pasó si no la has ejecutado.
- Tras cada push, espera al CI y corrige los fallos dentro del alcance antes de informar; no entregues un PR en rojo.
- Ante un dato duplicado o contradictorio, prevalece su dueño según el [mapa de documentación](WORKFLOW.md#2-mapa-de-documentación); señala la duplicación.
- Lo que encuentres fuera del alcance no lo arregles: propónlo como Issue en la siguiente parada.

## 2. Contexto

Lee solo lo que afecta al trabajo y amplía cuando aparezca una dependencia:

1. La historia (Issue), su épica y sus bloqueos.
2. Los requisitos que cita, en `docs/REQUIREMENTS.md`.
3. Las specs afectadas en `openspec/specs/` y el cambio en curso en `openspec/changes/`.
4. `docs/ARCHITECTURE.md` y los ADR y contratos de los componentes afectados.
5. El código y los tests implicados.

Ante dudas de alcance o prioridad, consulta `docs/PROJECT.md`. Al retomar una historia, deduce en qué paso está por la rama, `tasks.md` y el estado del PR antes de actuar.

## 3. Autonomía y límites

**Sin pedir permiso puedes:**

- leer, explorar, crear ramas y hacer commits locales;
- ejecutar los checks, `verify`, `sync` y `openspec validate`;
- actualizar la documentación y ajustar tareas dentro del alcance aprobado (infórmalo en la siguiente parada);
- publicar correcciones en un PR en revisión, incluidas las de un CI en rojo;
- crear las etiquetas y las Issues de un desglose aprobado.

**Nunca:**

- Mergear un PR, hacer push directo a `main` o `dev`, ni reescribir historia ya publicada.
- Cerrar Issues a mano ni crear tags o releases: se cierran con `Closes` y los crea el CI al mergear. Si el workflow falla, informa.
- Cambiar PROJECT, REQUIREMENTS o ROADMAP fuera de un plan aprobado.
- Decidir por tu cuenta que una historia no necesita OpenSpec.
- Desactivar la validación de `archive`.
- Versionar secretos o credenciales.

## 4. OpenSpec

- **Configuración:** `openspec/config.yaml` (contexto y reglas de los artefactos). Instalación: [WORKFLOW §3](WORKFLOW.md#3-herramientas).
- **Etapas:** `explore`, `propose`, `apply`, `update`, `verify`, `sync` y `archive`; el nombre del comando o skill depende de la herramienta. Cuándo se para y cuándo se encadena: [WORKFLOW §6](WORKFLOW.md#6-fase-3--ejecución-de-una-historia).
- **Siempre en las historias.** Solo se ejecuta una sin OpenSpec si la persona lo pide de forma explícita; tu estimación del tamaño no lo autoriza. Definición, planificación y release no lo usan.
- **Trabajo sin Issue:** propón crear una historia o un bug. Si la persona prefiere hacerlo directamente, trabaja sin OpenSpec, en una rama propia y con PR.
- **Un cambio por historia**, en kebab-case (`add-briefing-form`). Si la historia no cabe en un cambio, propón dividirla.
- **Tareas:** al implementar, la fuente de verdad es `tasks.md`; las casillas de la historia se marcan al publicar el PR.
- **Sin cambio de comportamiento** (refactor, test, chore o docs): sin delta de specs y archive con `--skip-specs`. No inventes requisitos para superar la validación.

## 5. GitHub

- Antes de crear Issues, crea las etiquetas que falten según `docs/ISSUE_LABELS.md` (nombre, descripción y color).
- Construye el cuerpo de cada Issue desde su plantilla de `.github/ISSUE_TEMPLATE/` y aplica las etiquetas de forma explícita: `gh` no lo hace solo.
- Registra jerarquía y bloqueos con las relaciones nativas (`gh issue create --parent N --blocked-by M`); crea antes las Issues de las que dependen.
- Si falta autenticación o permiso de escritura, di qué hay que configurar; no des el trabajo por hecho.

## 6. Ingeniería

- KISS, DRY, SOLID y separación de responsabilidades; componentes cohesionados y sustituibles.
- Reutiliza lo existente antes de crear abstracciones; evita las prematuras.
- Cambios enfocados: sin refactors ajenos a la historia ni ampliaciones de alcance.

## 7. Tests

- Elige el tipo (unitario, integración o E2E) según el comportamiento y el riesgo.
- Usa TDD cuando haya una unidad de comportamiento con sentido propio que se pueda probar de forma independiente; decide por la lógica y los resultados observables, no por el número de líneas.
- No escribas tests solo para subir la cobertura.
- `verify` y `openspec validate` comprueban artefactos; no sustituyen a los tests ni a los checks.
