# Servicios web con Flask: jedi.py

Introducción práctica a servicios web (API REST) usando Flask, con un ejemplo mínimo que administra una lista de personajes Jedi en memoria. Este README explica qué hace `jedi.py`, cómo correrlo en GitHub Codespaces, cómo consumirlo con `curl` desde otra terminal del mismo Codespace, y cómo exponer el puerto públicamente para probarlo desde Postman fuera de Codespaces.

## Antes de empezar

1. Genera tu propio repositorio a partir de este repositorio plantilla (botón **Use this template**), nombrado como A0XXXXXXX-intro-servicios-web, donde A0XXXXXXX es tu matrícula.
2. Abre un Codespace en tu repositorio: botón **Code → Codespaces → Create codespace on main**.

## 1. Qué hacen los servicios web de jedi.py

`jedi.py` es una API construida con Flask que mantiene una lista de jedis en memoria (se reinicia cada vez que el programa se vuelve a ejecutar):

```python
jedis = [
    {"name": 'Yoda', "id": 1},
    {"name": 'Luke', "id": 2},
    {"name": 'Obi wan', "id": 3}
]
```

Expone las siguientes rutas:

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/` | Devuelve el texto `Hello World!`, solo para confirmar que el servidor está corriendo |
| GET | `/api/jedis` | Devuelve la lista completa de jedis en formato JSON |
| POST | `/api/jedi` | Recibe un jedi en el cuerpo de la petición (JSON) y lo agrega a la lista |
| PUT | `/api/jedi` | Recibe un jedi en el cuerpo (debe incluir `id`), busca ese `id` en la lista y actualiza sus campos |
| DELETE | `/api/jedi` | Recibe un `id` en el cuerpo, busca ese jedi en la lista y lo elimina |

En POST, PUT y DELETE, el servidor lee el cuerpo de la petición con `request.get_json()`, así que siempre hay que enviar el `Content-Type: application/json` y el cuerpo en formato JSON. Si en PUT o DELETE el `id` no existe en la lista, el servicio responde con `{"message": "jedi id not found"}`.

El servidor corre en el puerto 5001 y escucha en todas las interfaces de red del contenedor (`host="0.0.0.0"`), lo cual es justo lo que se necesita para que Codespaces pueda reenviar ese puerto más adelante.

## 2. Cómo correr jedi.py en Codespaces

1. Abre el repositorio en un Codespace (`Code` → `Codespaces` → `Create codespace on main`). El `.devcontainer` de este repositorio solo trae instalada la extensión de Python para VS Code, así que Flask hay que instalarlo manualmente.
2. En la terminal del Codespace, instala Flask:
   ```bash
   pip install flask
   ```
3. Corre el servidor:
   ```bash
   python3 jedi.py
   ```
4. Deberías ver algo como:
   ```
    * Serving Flask app 'jedi'
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:5001
   ```
   Codespaces normalmente detecta que se abrió el puerto 5001 y muestra una notificación; puedes dejarla pasar por ahora (la usamos en la sección 4). El servidor se queda corriendo en esta terminal, así que para las siguientes pruebas vamos a necesitar una segunda terminal.

## 3. Consumir los servicios desde otra terminal de Codespaces con curl

Con `jedi.py` corriendo en la primera terminal, abre una segunda terminal en el mismo Codespace (ícono de `+` en el panel de terminal, o `Terminal` → `New Terminal`). Como ambas terminales viven dentro del mismo contenedor, aquí todavía usamos `localhost`.

**Probar que el servidor responde:**
```bash
curl http://localhost:5001/
```
Respuesta esperada: `Hello World!`

**Obtener la lista de jedis (GET):**
```bash
curl http://localhost:5001/api/jedis
```
Respuesta esperada:
```json
[{"id":1,"name":"Yoda"},{"id":2,"name":"Luke"},{"id":3,"name":"Obi wan"}]
```

**Agregar un jedi nuevo (POST):**
```bash
curl -X POST http://localhost:5001/api/jedi \
  -H "Content-Type: application/json" \
  -d '{"id": 4, "name": "Ahsoka"}'
```
Respuesta esperada (el jedi que se acaba de agregar):
```json
{"id":4,"name":"Ahsoka"}
```
Si vuelves a hacer el GET de `/api/jedis`, Ahsoka ya debería aparecer en la lista.

**Actualizar un jedi existente (PUT):**
```bash
curl -X PUT http://localhost:5001/api/jedi \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "Maestro Yoda"}'
```
Respuesta esperada (la lista completa, ya con el cambio aplicado):
```json
[{"id":1,"name":"Maestro Yoda"}, {"id":2,"name":"Luke"}, ...]
```

**Eliminar un jedi (DELETE):**
```bash
curl -X DELETE http://localhost:5001/api/jedi \
  -H "Content-Type: application/json" \
  -d '{"id": 2}'
```
Respuesta esperada: la lista completa sin el jedi con `id` 2.

**Probar un id que no existe (PUT o DELETE):**
```bash
curl -X DELETE http://localhost:5001/api/jedi \
  -H "Content-Type: application/json" \
  -d '{"id": 999}'
```
Respuesta esperada: `{"message": "jedi id not found"}`

> Nota: el repositorio también incluye `post.py` y `put.py`, dos scripts de Python equivalentes a los ejemplos de arriba pero usando la librería `requests` en vez de `curl` (necesitan `pip install requests`). Son útiles para ver cómo se consumiría este mismo servicio desde código Python en lugar de la línea de comandos.

## 4. Exponer el puerto como público para consumirlo desde Postman

Mientras el puerto 5001 esté en modo privado (el valor por defecto), solo se puede acceder a él desde dentro del propio Codespace. Para probarlo desde Postman, que corre fuera de Codespaces, hay que hacerlo público.

1. Con `jedi.py` corriendo, ve a la pestaña **Ports** del panel inferior de Codespaces (junto a Terminal). Debería aparecer una fila con el puerto `5001`; si no aparece, agrégala manualmente con **Add Port** y escribe `5001`.
2. En esa fila, haz clic derecho (o el menú de tres puntos) sobre el puerto 5001 y selecciona **Port Visibility** → **Public**.
3. Copia la URL que Codespaces generó para ese puerto, con un formato parecido a:
   ```
   https://<nombre-del-codespace>-5001.app.github.dev
   ```
4. En Postman, crea una nueva petición usando esa URL en vez de `localhost`, por ejemplo:
   - `GET https://<nombre-del-codespace>-5001.app.github.dev/api/jedis`
   - `POST https://<nombre-del-codespace>-5001.app.github.dev/api/jedi`, con el header `Content-Type: application/json` y el body en formato `raw / JSON`, igual que en los ejemplos de `curl` de la sección 3.
5. Cuando termines las pruebas, regresa el puerto a **Private**: mientras esté en público, cualquier persona con esa URL puede usar la API sin autenticación.

## Resumen rápido

1. `pip install flask` y `python3 jedi.py` para levantar el servidor (puerto 5001).
2. Desde otra terminal del mismo Codespace, probar los endpoints con `curl` usando `localhost:5001`.
3. Para usarlo desde Postman fuera de Codespaces, hacer público el puerto 5001 en la pestaña Ports y usar la URL generada (`https://...app.github.dev`) en vez de `localhost`.
