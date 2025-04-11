# InternetWhisper: Chatbot Conversacional de IA con Acceso a Internet

## Descripción del Proyecto

InternetWhisper es un chatbot conversacional de inteligencia artificial generativa inspirado en servicios como You.com y Google's Bard. Está diseñado para proporcionar información en tiempo real mediante el acceso a Internet. A diferencia de los asistentes virtuales tradicionales, que están limitados a conocimientos pre-entrenados, InternetWhisper puede buscar, analizar y sintetizar información actualizada de la web para responder consultas de los usuarios.

### Características principales:

- **Acceso a información en tiempo real**: Consulta Internet para proporcionar respuestas actualizadas y relevantes.
- **Caché vectorial con Redis**: Almacena información previamente recuperada para mejorar la eficiencia y reducir consultas redundantes.
- **Integración con Google Search**: Utiliza la API de búsqueda de Google para encontrar fuentes relevantes.
- **Procesamiento semántico avanzado**: Divide y analiza textos utilizando técnicas de NLP para mejorar la comprensión y relevancia.
- **Respuestas en tiempo real**: Implementa Server-Sent Events (SSE) para mostrar respuestas a medida que se generan.
- **Arquitectura modular**: Permite intercambiar componentes como scrapers y modelos de embeddings según las necesidades.

---

## Explicación Técnica

InternetWhisper está construido con una arquitectura modular que integra varias tecnologías para proporcionar respuestas precisas y contextuales.

### Arquitectura de la Aplicación:

1. **Capa de API (FastAPI)**:

   - Proporciona endpoints RESTful para la interacción con el chatbot.
   - Implementa Server-Sent Events (SSE) para streaming de respuestas en tiempo real.
   - Gestiona la autenticación y validación de solicitudes.

2. **Orquestador**:

   - Coordina el flujo de trabajo entre los diferentes componentes.
   - Gestiona el historial de conversaciones y el contexto.
   - Determina cuándo buscar nueva información o utilizar datos en caché.

3. **Sistema de Recuperación (Retrieval)**:

   - **Búsqueda Web**: Utiliza la API de Google para encontrar información relevante.
   - **Scraping**: Extrae contenido de páginas web mediante `ScraperLocal` (aiohttp) o `ScraperRemote` (Playwright).

4. **Procesamiento de Texto**:

   - Divide textos largos en fragmentos manejables mediante `LangChainSplitter` o `AdjSenSplitter`.
   - Utiliza Spacy para análisis lingüístico y segmentación de oraciones.
   - Convierte textos en embeddings vectoriales mediante `OpenAIEmbeddings`.

5. **Sistema de Caché Vectorial (Redis)**:

   - Almacena documentos y sus representaciones vectoriales.
   - Implementa búsqueda de similitud para recuperar información relevante.
   - Reduce la necesidad de consultas web repetidas.

6. **Generación de Respuestas**:
   - Utiliza el modelo GPT-3.5 Turbo de OpenAI para generar respuestas coherentes.
   - Incorpora información recuperada como contexto para mejorar la precisión.
   - Transmite tokens de respuesta en tiempo real al cliente.

### Flujo de Trabajo:

1. El usuario envía una consulta a través de la interfaz web.
2. El sistema analiza la consulta y determina si necesita información externa.
3. Si es necesario, realiza búsquedas web y extrae contenido relevante.
4. El contenido se procesa, se divide en fragmentos y se vectoriza.
5. Los vectores se almacenan en la caché Redis para uso futuro.
6. La información relevante se proporciona como contexto al modelo GPT-3.5.
7. El modelo genera una respuesta que se transmite al usuario en tiempo real.

---

## Pasos para Configurar Variables de Entorno

Para ejecutar InternetWhisper correctamente, es necesario configurar las siguientes variables de entorno:

1. Cree un archivo `.env` en la raíz del proyecto copiando el archivo `.env.example`:

   ```bash
   cp .env.example .env
   ```

2. Configure las siguientes variables en el archivo `.env`:

   | Variable               | Descripción                                      | Ejemplo                                                                                                                      |
   | ---------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
   | HEADER_ACCEPT_ENCODING | Codificación aceptada para solicitudes HTTP      | gzip                                                                                                                         |
   | HEADER_USER_AGENT      | Agente de usuario para solicitudes HTTP          | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 (gzip) |
   | GOOGLE_API_HOST        | Host de la API de Google Search                  | https://www.googleapis.com/customsearch/v1?                                                                                  |
   | GOOGLE_FIELDS          | Campos a recuperar de la API de Google           | items(title, displayLink, link, snippet,pagemap/cse_thumbnail)                                                               |
   | GOOGLE_API_KEY         | Clave API para Google Custom Search              | your-google-api-key                                                                                                          |
   | GOOGLE_CX              | ID del motor de búsqueda personalizado de Google | your-custom-search-engine-id                                                                                                 |
   | OPENAI_API_KEY         | Clave API para acceder a los servicios de OpenAI | your-openai-api-key                                                                                                          |

### Obtención de claves API:

- **Google API Key y CX**: Visite Google Custom Search para crear una clave API y un motor de búsqueda personalizado.
- **OpenAI API Key**: Regístrese en OpenAI para obtener una clave API.

---

## Pasos para Correr la Aplicación Localmente

### Requisitos previos:

- Docker y Docker Compose instalados
- Git
- Claves API configuradas (ver sección anterior)

### Instalación y ejecución:

1. Clone el repositorio:

   ```bash
   git clone https://github.com/yourusername/InternetWhisper.git
   cd InternetWhisper
   ```

2. Configure las variables de entorno como se describió en la sección anterior.

3. Construya y ejecute la aplicación con Docker Compose:
   ```bash
   docker-compose build
   docker-compose up
   ```

### Configuración opcional:

- **Selección de Scraper**: El proyecto incluye dos opciones de scraper:

  - `ScraperLocal`: Utiliza aiohttp para web scraping (predeterminado).
  - `ScraperRemote`: Utiliza Playwright en un contenedor separado para un mejor renderizado de JavaScript.
    Para cambiar entre scrapers, modifique el archivo `orchestrator/main.py` y descomente los servicios correspondientes en `docker-compose.yml`.

- **Selección de Embeddings**: Por defecto se utiliza `OpenAIEmbeddings`, pero puede configurar otras opciones según sea necesario.

### Acceda al chatbot:

Abra su navegador web y vaya a [http://localhost:8501/](http://localhost:8501/) para interactuar con InternetWhisper.

---

## Definición OpenAPI de la API

InternetWhisper genera automáticamente documentación OpenAPI que describe todos los endpoints disponibles, parámetros requeridos y respuestas esperadas.

### Acceso a la documentación OpenAPI:

Con la aplicación en ejecución, visite:

- **Documentación Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Documentación ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Exploración de endpoints:

- La interfaz Swagger UI permite probar los endpoints directamente desde el navegador.
- Puede expandir cada endpoint para ver detalles sobre parámetros, cuerpos de solicitud y respuestas.

### Importancia de la documentación OpenAPI:

- **Desarrollo de clientes**: Facilita la creación de clientes en diferentes lenguajes de programación.
- **Integración**: Permite a otros desarrolladores integrar InternetWhisper en sus aplicaciones.
- **Pruebas**: Proporciona una forma sencilla de probar la API sin necesidad de código adicional.
- **Comprensión**: Ayuda a entender la estructura y capacidades de la API sin necesidad de revisar el código fuente.

### Uso de la documentación:

- **Para desarrolladores**: Utilice la documentación como referencia para entender cómo interactuar con la API.
- **Para integración**: Exporte la especificación OpenAPI en formato JSON o YAML para generar clientes en diferentes lenguajes.
- **Para pruebas**: Utilice la interfaz Swagger UI para probar rápidamente los endpoints y entender su comportamiento.

---

¡Disfrute explorando y modificando InternetWhisper para sus necesidades específicas! Este chatbot conversacional de IA representa un avance significativo en la capacidad de los asistentes virtuales para proporcionar información actualizada y relevante del mundo real.
