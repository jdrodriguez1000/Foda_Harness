La solucon esperada debera:
1. Estar divida en dos grandes bloques Motor e Instancia.
2. El harness qeu se va a construir en un motor instalable.
3. La instancia utilizara ese motor para replicar los flujos de trabajo de los cientificos de datos.
4. Cada instancia sera el trabajo sobre una empresa diferente con caracteristicas diferentes.
5. Las instancias podran ser escalables deacuerdo a las necesidades del cliente.

El harness **no comparte repositorio con el producto que construye**. Es un **motor reutilizable** que, al **instalarse**, crea la **instancia del proyecto en otra carpeta**. Conviven así **dos planos que nunca se mezclan**

- **Plano de construcción — el MOTOR.** Guarda las **definiciones canónicas** que se instalan (agentes, comandos de operación, skills, plantillas, esquemas de estado) y su propia **memoria de construcción** (`800_persistence/`: cómo *construimos el motor*). Sus comandos de raíz ejemplo: (`/next`, `/progress`) operan **sobre el motor**.

- **Plano de operación — la INSTANCIA (carpeta externa, una POR CLIENTE).** Recibe una copia de las definiciones y es donde realmente se **construye la solucion para una empresa ABC concreta**: el codigo, las iteraciones, los artefactos de cada fase y el **estado de runtime**. Ese estado **nunca vuelve** al repo del motor.

El **puente** entre ambos planos es un **instalador de terminal** (`./install.sh`): copia las definiciones del motor a la carpeta destino del cliente, inicializa su versionado git y deja listo el esqueleto de entrada. Como Claude Code solo auto-carga `.claude/`, lo privado del motor en la instancia (plantillas, configuración, runtime) vive en un namespace aparte que se promueve *just-in-time*.


El motor se llamará FODA: Forecast Optimization Driven Agentic. Por lo tanto todo lo que se utilice en el motor se llamara foda.

La instancia utilizara descripciones basadas en fda, por ejmplo si tenemos qeu crear un comando este se llamará fda-comando. 

