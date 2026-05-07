# Guía de Estudio: Naive Bayes en TicketAI

> Este doc es para ti. Nada formal. Solo lo que necesitas saber para responder preguntas técnicas difíciles sobre cómo funciona el modelo de este proyecto.

---

## Índice

1. [¿Qué hace el proyecto?](#s1)
2. [La Idea Central de Naive Bayes](#s2)
3. [El Problema del Underflow y Por Qué Usamos Logaritmos](#s3)
4. [Suavizamiento de Laplace](#s4)
5. [Multinomial vs Bernoulli vs Gaussiano](#s5)
6. [El Pipeline de Preprocesamiento](#s6)
7. [Bag of Words (BoW)](#s7)
8. [Training: Qué Calcula el Modelo](#s8)
9. [Predicción Paso a Paso](#s9)
10. [Métricas de Evaluación (Accuracy, Precision, Recall, F1)](#s10)
11. [Validación Cruzada K-Fold](#s11)
12. [Las Palabras Más Discriminativas por Clase](#s12)
13. [Por Qué el Accuracy Es Tan Alto (99.29%)](#s13)
14. [Limitaciones del Modelo](#s14)
15. [API: Endpoints del Backend](#s15)
16. [Preguntas Técnicas Típicas y Cómo Responderlas](#s16)
17. [Resumen Visual del Flujo Completo](#s17)
18. [Datos Clave para Memorizar](#s18)
19. [Mapa de Archivos del Proyecto](#s19)

---

<a id="s1"></a>

## 1. ¿Qué hace el proyecto?

Clasifica tickets de soporte al cliente en **11 categorías** (ACCOUNT, CANCEL, CONTACT, DELIVERY, FEEDBACK, INVOICE, ORDER, PAYMENT, REFUND, SHIPPING, SUBSCRIPTION) usando Naive Bayes Multinomial implementado **desde cero** — sin scikit-learn, sin TensorFlow, puro Python y matemáticas.

Dataset: **26,872 tickets** del dataset de Bitext en HuggingFace.

---

<a id="s2"></a>

## 2. La Idea Central de Naive Bayes

Antes de entrar en fórmulas, entiende la intuición:

> **¿A qué categoría pertenece este texto?**  
> Naive Bayes responde: _"a la categoría donde las palabras que aparecen en el texto son más probables de haber salido"_.

Es un clasificador probabilístico. Calcula la probabilidad de que un texto pertenezca a cada clase y elige la más alta.

### El teorema de Bayes (la base)

```
P(clase | texto) = P(texto | clase) × P(clase) / P(texto)
```

- **P(clase | texto)**: lo que queremos saber — dado el texto, ¿cuál es la probabilidad de cada clase?
- **P(texto | clase)**: qué tan probable es ver ese texto si la clase es X
- **P(clase)**: qué tan frecuente es la clase en el dataset (prior)
- **P(texto)**: probabilidad del texto en general — igual para todas las clases, así que se ignora

### El supuesto "naive" (ingenuo)

El modelo asume que **cada palabra es independiente de las demás dada la clase**.

En realidad esto es falso (las palabras tienen contexto entre sí), pero funciona sorprendentemente bien igual. De ahí el nombre "naive".

Con ese supuesto:

```
P(texto | clase) = P(palabra1 | clase) × P(palabra2 | clase) × ... × P(palabraN | clase)
```

Entonces la decisión final es:

```
clase_predicha = argmax[ P(clase) × P(w1|clase) × P(w2|clase) × ... × P(wN|clase) ]
```

---

<a id="s3"></a>

## 3. El Problema del Underflow y Por Qué Usamos Logaritmos

### El problema

Imagina que tienes 50 palabras en un texto y cada probabilidad es algo como `0.002`. Multiplicarlas:

```
0.002 × 0.002 × 0.002 × ... (50 veces)
= 0.002^50
≈ 1.12 × 10^-145
```

Eso es un número **tan pequeño** que la computadora simplemente lo redondea a `0.0` (underflow numérico). Cuando todos los valores son `0.0`, ya no puedes comparar nada.

### La solución: logaritmos

En lugar de multiplicar probabilidades, **sumamos sus logaritmos**. La razón es matemática:

```
log(A × B × C) = log(A) + log(B) + log(C)
```

Así la fórmula se convierte en:

```
score(clase) = log P(clase) + Σ log P(palabra_i | clase)
```

Los logaritmos de números pequeños son negativos pero manejables (por ejemplo, `log(0.002) ≈ -6.2`). La suma de muchos `-6.2` es `-310`, que la computadora maneja perfectamente.

**Resultado**: misma decisión (argmax), pero numéricamente estable.

### Cómo está en el código

En [`classifier.py` líneas 126–133](../backend/app/naive_bayes/classifier.py), el loop de predicción suma los log-likelihoods:

```python
for cls in self.classes:
    score = self.log_prior[cls]
    for token in tokens:
        if token in self.log_likelihood[cls]:
            score += self.log_likelihood[cls][token]
        else:
            score += self.log_likelihood[cls]["__UNSEEN__"]
    log_probs[cls] = score
```

Los `log_likelihood` se precalculan en [`fit()` líneas 88–101](../backend/app/naive_bayes/classifier.py):

```python
self.log_likelihood[cls][word] = math.log(
    (count + self.alpha) / denominator
)
```

---

<a id="s4"></a>

## 4. Suavizamiento de Laplace (Laplace Smoothing)

### El problema que resuelve

Si el modelo nunca vio la palabra "quantum" en tickets de DELIVERY durante el entrenamiento, entonces:

```
P("quantum" | DELIVERY) = 0
```

Y como multiplicas todo (o sumas en log), eso hace que la probabilidad de DELIVERY sea **0 para ese texto completo**, aunque todas las demás palabras señalen perfectamente a DELIVERY. Un solo cero lo arruina todo.

### La solución: sumar alpha

En lugar de `count(palabra, clase)` usas `count(palabra, clase) + α`:

```
P(palabra | clase) = (count(palabra, clase) + α) / (total_palabras_en_clase + α × |vocabulario|)
```

- `α = 1` es suavizamiento de Laplace estándar (también llamado "add-one smoothing")
- `α < 1` es suavizamiento Lidstone (más suave)

Con `α = 1`, **ninguna probabilidad es cero**. Las palabras nunca vistas reciben una probabilidad pequeña pero real.

El denominador también se ajusta (`+ α × |vocabulario|`) para que todo siga sumando 1.

### En el código

```python
# classifier.py — líneas 88-101
for cls in self.classes:
    self.log_likelihood[cls] = {}
    denominator = total_words_per_class[cls] + self.alpha * self.vocab_size

    for word in self.vocab:
        count = self.word_counts_per_class[cls].get(word, 0)
        self.log_likelihood[cls][word] = math.log(
            (count + self.alpha) / denominator
        )

    # Token especial para palabras fuera del vocabulario
    self.log_likelihood[cls]["__UNSEEN__"] = math.log(
        self.alpha / denominator
    )
```

Ver en código: [classifier.py](../backend/app/naive_bayes/classifier.py) — línea 22 (alpha default), líneas 88–101 (loop de likelihood), líneas 99–101 (token `__UNSEEN__`).

---

<a id="s5"></a>

## 5. Multinomial vs Bernoulli vs Gaussiano

Hay tres variantes de Naive Bayes. Este proyecto usa **Multinomial**.

| Variante        | ¿Qué modela?                             | Cuándo usar                        |
| --------------- | ---------------------------------------- | ---------------------------------- |
| **Multinomial** | Conteo de veces que aparece cada palabra | Texto, clasificación de documentos |
| **Bernoulli**   | Si la palabra aparece o no (0 o 1)       | Textos cortos, búsqueda binaria    |
| **Gaussiano**   | Features numéricas continuas             | Datos de sensores, datos tabulares |

**Multinomial** es el correcto para clasificar texto porque le importa cuántas veces aparece cada palabra, no solo si aparece.

---

<a id="s6"></a>

## 6. El Pipeline de Preprocesamiento

El modelo no ve el texto crudo. Antes de entrenar o predecir, el texto pasa por [`preprocess()`](../backend/app/naive_bayes/preprocessor.py) (líneas 30–60) en `preprocessor.py`:

```
texto crudo
    ↓
1. Eliminar placeholders como {{Order Number}}, {{Account ID}}
    ↓
2. Convertir a minúsculas
    ↓
3. Eliminar puntuación (solo letras)
    ↓
4. Tokenizar con NLTK word_tokenize()
    ↓
5. Eliminar stopwords en inglés ("the", "is", "at", "which"...)
    ↓
6. Stemming con Snowball Stemmer (compra → compra, running → run, orders → order)
    ↓
lista de tokens limpios
```

### ¿Por qué cada paso?

- **Placeholders** (línea 42 de [preprocessor.py](../backend/app/naive_bayes/preprocessor.py)): el dataset de Bitext tiene variables como `{{name}}` — se eliminan con la regex `\{\{.*?\}\}` (línea 27)
- **Minúsculas** (línea 45): "Order" y "order" son la misma palabra
- **Stopwords** (línea 23): palabras muy comunes que no discriminan entre clases
- **Stemming** (línea 24): "shipping", "shipped", "ships" → "ship". Reduce el vocabulario y agrupa variantes

Existe también [`tokenize_only()`](../backend/app/naive_bayes/preprocessor.py) (líneas 63–69) que hace lo mismo pero **sin stemming**, usada solo para mostrar los tokens al usuario en la respuesta del API.

### Vocabulario resultante

Después del preprocesamiento, el vocabulario tiene **2,509 tokens** únicos. Eso es el espacio de features del modelo.

---

<a id="s7"></a>

## 7. Bag of Words (BoW) — El Modelo de Representación

El modelo usa **Bag of Words**: cada documento se representa como un conteo de palabras, sin importar el orden.

```
"I want to cancel my order"
→ después de preprocesar: ["want", "cancel", "order"]
→ representación BoW: {"want": 1, "cancel": 1, "order": 1}
```

El orden no importa. "I want to cancel my order" y "cancel my order I want" producen el mismo vector.

**No se usa TF-IDF** en este proyecto — solo conteos crudos.

---

<a id="s8"></a>

## 8. Training: Qué Calcula el Modelo

Durante [`fit()` líneas 47–104](../backend/app/naive_bayes/classifier.py), el modelo calcula y guarda:

### 8.1 Log Prior — log P(clase)

```python
# classifier.py — líneas 82-83
for cls in self.classes:
    self.log_prior[cls] = math.log(self.class_counts[cls] / self.doc_count)
```

Por ejemplo, ACCOUNT tiene 5,986 de 26,872 docs:

```
log_prior["ACCOUNT"] = log(5986 / 26872) ≈ log(0.2228) ≈ -1.501
```

Esto refleja que ACCOUNT es la clase más frecuente.

### 8.2 Log Likelihood — log P(palabra | clase)

Para cada combinación (palabra, clase):

```python
log_likelihood[cls][word] = log((count(word en docs de cls) + alpha) / (total_words_in_cls + alpha * vocab_size))
```

Ver: [classifier.py](../backend/app/naive_bayes/classifier.py) líneas 88–101.

Esto se precalcula para **todas las 2,509 palabras × 11 clases = 27,599 entradas**.

---

<a id="s9"></a>

## 9. Predicción Paso a Paso

Dado un texto nuevo (función [`predict()`](../backend/app/naive_bayes/classifier.py) líneas 106–149):

**Paso 1** — Preprocesar igual que en training  
**Paso 2** — Para cada clase, calcular el score:

```
score(ACCOUNT) = log_prior[ACCOUNT] + sum(log_likelihood[ACCOUNT][token] for token in tokens)
```

**Paso 3** — La clase con mayor score es la predicción:

```
predicción = argmax(scores)
```

**Paso 4** — Convertir scores a probabilidades con softmax (líneas 196–203):

```python
confidences = softmax(log_probs)
```

### ¿Qué es softmax?

Transforma números arbitrarios (los scores en log-space) a probabilidades que sumen 1:

```
P(clase_i) = exp(score_i - max_score) / sum(exp(score_j - max_score) for all j)
```

El truco de restar `max_score` antes de exponenciar es otra protección contra overflow numérico. Implementado en [`_softmax()`](../backend/app/naive_bayes/classifier.py) (líneas 196–203).

---

<a id="s10"></a>

## 10. Métricas de Evaluación

> Todas las métricas están implementadas desde cero en [`evaluator.py`](../backend/app/naive_bayes/evaluator.py).

---

### 10.1 Accuracy (Exactitud)

**¿Qué mide?** Del total de predicciones, ¿cuántas acertó el modelo?

```
accuracy = predicciones_correctas / total_predicciones
```

**Implementación** ([`compute_accuracy()`](../backend/app/naive_bayes/evaluator.py) líneas 114–117):

```python
def compute_accuracy(y_true, y_pred):
    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    return correct / len(y_true)
```

**Resultado del modelo**: **99.29%** sobre el dataset completo.

**¿Cuándo puede engañar?** Si las clases estuvieran muy desbalanceadas (ej. 90% de tickets son ACCOUNT), un modelo que siempre predice ACCOUNT tendría 90% de accuracy sin haber aprendido nada. En este proyecto las clases están relativamente balanceadas, así que no es un problema grave.

---

### 10.2 Precision (Precisión)

**¿Qué mide?** De todos los tickets que el modelo clasificó como clase X, ¿cuántos realmente eran X?

```
Precision = TP / (TP + FP)
```

|                          | Predicho como X     | Predicho como otra clase |
| ------------------------ | ------------------- | ------------------------ |
| **Realmente X**          | TP (True Positive)  | FN (False Negative)      |
| **Realmente otra clase** | FP (False Positive) | TN (True Negative)       |

**Ejemplo concreto**: Si el modelo predijo 100 tickets como CANCEL y 95 de ellos realmente eran CANCEL → Precision = 95/100 = 0.95

**Implementación** ([evaluator.py](../backend/app/naive_bayes/evaluator.py) línea 142):

```python
precision = tp[cls] / (tp[cls] + fp[cls]) if (tp[cls] + fp[cls]) > 0 else 0.0
```

**¿Cuándo importa más?** Cuando el costo de un **falso positivo** es alto. Ejemplo: clasificar como REFUND un ticket que no lo es puede generar un reembolso innecesario.

---

### 10.3 Recall (Sensibilidad / Cobertura)

**¿Qué mide?** De todos los tickets que realmente son clase X, ¿cuántos detectó el modelo?

```
Recall = TP / (TP + FN)
```

**Ejemplo concreto**: Si hay 200 tickets reales de CANCEL y el modelo detectó 190 → Recall = 190/200 = 0.95

**Implementación** ([evaluator.py](../backend/app/naive_bayes/evaluator.py) línea 143):

```python
recall = tp[cls] / (tp[cls] + fn[cls]) if (tp[cls] + fn[cls]) > 0 else 0.0
```

**¿Cuándo importa más?** Cuando el costo de un **falso negativo** es alto. Ejemplo: no detectar un ticket de PAYMENT urgente puede dejar al cliente sin atención.

**El trade-off Precision vs Recall**: generalmente, si aumentas uno, bajas el otro. Un modelo que predice "todo es X" tiene Recall=1.0 pero Precision muy baja. Un modelo muy conservador tiene Precision alta pero Recall baja.

---

### 10.4 F1-Score

**¿Qué mide?** La **media armónica** entre Precision y Recall. Es un balance entre las dos.

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**¿Por qué media armónica y no promedio simple?**  
La media armónica castiga más los valores extremos. Si Precision=1.0 y Recall=0.0:

- Media simple = 0.5 (parece aceptable)
- Media armónica = 0.0 (refleja que el modelo es inútil)

**Implementación** ([evaluator.py](../backend/app/naive_bayes/evaluator.py) líneas 144–148):

```python
f1 = (
    2 * precision * recall / (precision + recall)
    if (precision + recall) > 0
    else 0.0
)
```

**Resultado del modelo**: F1 por clase varía entre 96.15% (DELIVERY) y >99% para la mayoría.

---

### 10.5 Macro F1

**¿Qué es?** El promedio del F1 de todas las clases, donde **cada clase pesa igual** sin importar cuántos ejemplos tiene.

```
Macro F1 = (F1_ACCOUNT + F1_CANCEL + ... + F1_SUBSCRIPTION) / 11
```

**Implementación** ([evaluator.py](../backend/app/naive_bayes/evaluator.py) línea 66):

```python
macro_f1 = sum(m["f1"] for m in per_class) / len(per_class)
```

**Resultado del modelo**: **99.28%** macro F1 en dataset completo.

**¿Por qué Macro y no Weighted?**

- **Macro F1**: trata todas las clases igual — útil cuando te importa el rendimiento en clases minoritarias
- **Weighted F1**: pondera por número de ejemplos — favorece las clases grandes

En soporte al cliente, un error en una clase pequeña (ej. SUBSCRIPTION) es tan importante como uno en una clase grande, así que Macro F1 es la métrica correcta.

---

### 10.6 Soporte (Support)

El campo `support` en cada clase ([evaluator.py](../backend/app/naive_bayes/evaluator.py) línea 151) es simplemente **cuántos ejemplos reales** de esa clase hay en el set de evaluación. Es útil para contextualizar las métricas: un F1 de 96% con support=5000 es mucho más significativo que con support=50.

---

### 10.7 Matriz de Confusión

Una tabla 11×11 (implementada en [`compute_confusion_matrix()`](../backend/app/naive_bayes/evaluator.py) líneas 94–111) donde:

- Filas = clase real
- Columnas = clase predicha
- La diagonal = aciertos
- Fuera de la diagonal = errores

```python
# evaluator.py — líneas 105-109
for true, pred in zip(y_true, y_pred):
    i = label_to_idx.get(true)
    j = label_to_idx.get(pred)
    if i is not None and j is not None:
        matrix[i][j] += 1
```

Las clases con más confusión son DELIVERY, SHIPPING, ORDER — tiene sentido porque sus tickets se parecen semánticamente.

---

<a id="s11"></a>

## 11. Validación Cruzada K-Fold

### ¿Por qué no basta medir en el mismo dataset de entrenamiento?

Si mides el modelo con los mismos datos que usó para aprender, el resultado es artificialmente alto (el modelo "memorizó" esos datos). Necesitas evaluarlo en datos que **no vio**.

### ¿Qué es K-Fold?

1. Divide el dataset en **K partes iguales** (folds)
2. Entrena con K-1 folds, evalúa con el fold restante
3. Repite K veces, cada vez usando un fold distinto como validación
4. Promedia los resultados

Con **K=5** (función [`k_fold_cross_validation()`](../backend/app/naive_bayes/evaluator.py) líneas 11–91):

- Cada iteración entrena con ~21,498 ejemplos y valida con ~5,374
- Los 5 folds combinados cubren todos los datos exactamente una vez

### Resultados del proyecto

```
Mean Accuracy: 99.14% ± 0.04%
Mean Macro F1: 99.13% ± 0.04%
```

La desviación estándar de ±0.04% indica que el modelo es **extremadamente estable** entre folds — no hay overfitting significativo.

---

<a id="s12"></a>

## 12. Las Palabras Más Discriminativas por Clase

El modelo puede calcular qué palabras son más características de cada clase usando [`get_top_words()`](../backend/app/naive_bayes/classifier.py) (líneas 171–194):

```
discriminative_score(word, class) = log P(word | class) - avg(log P(word | other_classes))
```

Si una palabra tiene score alto para CANCEL, significa que aparece mucho en CANCEL pero poco en las demás clases. Estas palabras "discriminativas" son las que el modelo más usa para tomar decisiones.

Esto está expuesto en el endpoint `GET /api/v1/model/top-words?class=CANCEL&n=20`.

---

<a id="s13"></a>

## 13. Por Qué el Accuracy Es Tan Alto (99.29%)

Esto es lo que te van a preguntar. Varios factores:

1. **El dataset es de alta calidad**: Bitext fue diseñado específicamente para este tipo de clasificación, con categorías bien definidas y sin ruido excesivo
2. **Las categorías son semánticamente distintas**: un ticket de INVOICE no se parece mucho a uno de DELIVERY en vocabulario
3. **Preprocesamiento efectivo**: stemming reduce variación de vocabulario, stopwords quita ruido
4. **Laplace smoothing funciona bien aquí**: el vocabulario es grande y los textos son del mismo dominio (support tickets)
5. **Multinomial NB es adecuado**: el modelo de conteo de palabras captura bien las diferencias de dominio en soporte al cliente

### ¿Es sospechoso un 99.29%?

Es alto, pero válido en este contexto. El K-Fold lo confirma (99.14% fuera del training set). Si hubiera overfitting severo, el K-Fold bajaría mucho.

Las clases con menor F1 son DELIVERY (96.15%) y SHIPPING (98.50%), que se confunden entre sí — exactamente lo que esperarías intuitivamente.

---

<a id="s14"></a>

## 14. Limitaciones del Modelo

Para responder preguntas críticas:

- **No entiende contexto**: "I don't want to cancel" tiene la palabra "cancel" y puede clasificarse mal
- **Bag of Words ignora el orden**: el modelo ve las mismas palabras sin importar estructura sintáctica
- **El supuesto de independencia es falso**: las palabras correlacionan entre sí en el mundo real
- **No maneja sarcasmo ni ironía**: texto como "great, my order is lost again" puede confundirse
- **Vocabulario fijo**: palabras fuera del vocabulario de entrenamiento reciben el tratamiento de `__UNSEEN__`
- **Sensible al preprocesamiento**: si cambia el stemmer o las stopwords, el vocabulario cambia y el modelo necesita reentrenarse

---

<a id="s15"></a>

## 15. API: Endpoints del Backend

El backend es **FastAPI** con todos los routers montados bajo `/api/v1` (ver [main.py](../backend/app/main.py) líneas 92–96). Los 4 grupos de rutas son:

```
/api/v1/auth        → autenticación JWT
/api/v1/tickets     → CRUD de tickets
/api/v1/classifier  → clasificación de texto
/api/v1/model       → métricas y analítica del modelo
```

---

### 15.1 Auth — [routers/auth.py](../backend/app/routers/auth.py)

#### `POST /api/v1/auth/login`

- **Recibe** (body JSON):
  ```json
  { "email": "admin@example.com", "password": "secret" }
  ```
- **Responde** (200):
  ```json
  {
    "access_token": "<JWT>",
    "refresh_token": "<JWT>",
    "user": { "id": "u-001", "email": "...", "role": "admin" }
  }
  ```
- **Errores**: 401 si credenciales inválidas — código: [auth.py](../backend/app/routers/auth.py) línea 17

#### `POST /api/v1/auth/refresh`

- **Recibe** (body JSON): `{ "refresh_token": "<JWT>" }`
- **Responde** (200): `{ "access_token": "<nuevo JWT>" }`
- **Errores**: 401 si el refresh token es inválido o expirado — código: [auth.py](../backend/app/routers/auth.py) línea 32

#### `POST /api/v1/auth/logout`

- **Requiere**: header `Authorization: Bearer <token>`
- **Responde**: 204 No Content. El JWT es stateless — nada que invalidar en el servidor.
- **Código**: [auth.py](../backend/app/routers/auth.py) línea 46

#### `GET /api/v1/auth/me`

- **Requiere**: header `Authorization: Bearer <token>`
- **Responde** (200): `{ "id": "u-001", "email": "admin@example.com", "role": "admin" }`
- **Código**: [auth.py](../backend/app/routers/auth.py) línea 52

---

### 15.2 Classifier — [routers/classifier.py](../backend/app/routers/classifier.py)

#### `POST /api/v1/classifier/predict`

- **Recibe** (body JSON):

  ```json
  { "text": "I need to cancel my subscription immediately" }
  ```

  Schema: [models/prediction.py](../backend/app/models/prediction.py) línea 4 — `PredictRequest`.

- **Responde** (200):

  ```json
  {
    "category": "CANCEL",
    "confidences": { "ACCOUNT": 0.000012, "CANCEL": 0.978543, ... },
    "log_probs":   { "ACCOUNT": -45.23,   "CANCEL": -12.01,   ... },
    "tokens": ["need", "cancel", "subscription", "immediately"],
    "processing_ms": 1.34
  }
  ```

  - `category`: clase con mayor score (argmax)
  - `confidences`: probabilidades después del softmax (suman 1.0)
  - `log_probs`: scores crudos en log-space antes del softmax
  - `tokens`: tokens **sin stemming** (para mostrar al usuario)
  - `processing_ms`: tiempo de inferencia

  Schema respuesta: [models/prediction.py](../backend/app/models/prediction.py) líneas 8–13 — `PredictionResponse`.

- **Errores**: 422 si el texto está vacío, 503 si el modelo no está cargado
- **Código**: [routers/classifier.py](../backend/app/routers/classifier.py) líneas 9–19

---

### 15.3 Tickets — [routers/tickets.py](../backend/app/routers/tickets.py)

Los tickets se **auto-clasifican** al crearse: el router llama al modelo internamente (líneas 28–39).

#### `POST /api/v1/tickets`

- **Recibe** (body JSON):
  ```json
  {
    "subject": "Order not delivered",
    "description": "My package was supposed to arrive yesterday..."
  }
  ```
- **Responde** (200, `TicketResponse`):
  ```json
  {
    "id": "t-abc123",
    "subject": "Order not delivered",
    "description": "...",
    "predicted_category": "DELIVERY",
    "confidences": { "DELIVERY": 0.94, "SHIPPING": 0.04, ... },
    "final_category": null,
    "status": "open",
    "created_by": "u-001",
    "assignee_id": null,
    "created_at": "2026-05-06T19:00:00",
    "updated_at": "2026-05-06T19:00:00"
  }
  ```
  `predicted_category` lo asigna el modelo automáticamente. `final_category` es null hasta que un agente lo corrija.

#### `GET /api/v1/tickets`

- **Recibe** (query params, todos opcionales):
  - `status` — filtrar por estado (`open`, `closed`, etc.)
  - `category` — filtrar por categoría (`CANCEL`, `DELIVERY`, etc.)
  - `q` — búsqueda de texto libre
  - `assignee` — ID del agente asignado
  - `page` / `size` — paginación (default 1 / 20, máximo size 100)
- **Responde** (200): `{ "items": [...], "total": 150, "page": 1, "size": 20, "pages": 8 }`

#### `GET /api/v1/tickets/{ticket_id}`

- **Recibe**: `ticket_id` en la URL
- **Responde** (200): `TicketResponse`
- **Errores**: 404

#### `PATCH /api/v1/tickets/{ticket_id}`

- **Recibe** (body JSON, todos opcionales): `{ "status": "closed", "final_category": "SHIPPING", "assignee_id": "u-002" }`
- **Responde** (200): `TicketResponse` actualizado
- **Errores**: 404

#### `DELETE /api/v1/tickets/{ticket_id}`

- **Responde**: 204 No Content — **Errores**: 404

Schema: [models/ticket.py](../backend/app/models/ticket.py)

---

### 15.4 Model Analytics — [routers/model_analytics.py](../backend/app/routers/model_analytics.py)

Todos los endpoints leen del archivo `evaluation_data` cargado en startup (excepto `top-words` que usa el modelo en memoria).

#### `GET /api/v1/model/info`

- **Responde** (200): `{ "version": "1.0.0", "trained_at": "...", "vocab_size": 2509, "doc_count": 26872, "classes": [...] }`
- **Código**: [model_analytics.py](../backend/app/routers/model_analytics.py) línea 21

#### `GET /api/v1/model/metrics`

- **Responde** (200): `{ "accuracy": 0.9929, "macro_f1": 0.9928, "per_class": [{ "class": "ACCOUNT", "precision": 0.9981, "recall": 0.9975, "f1": 0.9978, "support": 5986 }, ...] }`
- **Código**: [model_analytics.py](../backend/app/routers/model_analytics.py) línea 27

#### `GET /api/v1/model/confusion-matrix`

- **Responde** (200): `{ "labels": ["ACCOUNT", ...], "matrix": [[5980, 2, ...], ...] }` — `matrix[i][j]` = ejemplos de clase real `i` predichos como `j`
- **Código**: [model_analytics.py](../backend/app/routers/model_analytics.py) línea 33

#### `GET /api/v1/model/kfolds`

- **Responde** (200): `{ "k": 5, "folds": [...], "mean": { "accuracy": 0.9914, "macro_f1": 0.9913 }, "std": { "accuracy": 0.0004, ... } }`
- **Código**: [model_analytics.py](../backend/app/routers/model_analytics.py) línea 39

#### `GET /api/v1/model/top-words`

- **Recibe** (query): `class` (requerido), `n` (opcional, default 20, máx 100)
- **Ejemplo**: `GET /api/v1/model/top-words?class=CANCEL&n=10`
- **Responde** (200): `[{ "word": "cancel", "weight": 4.821 }, { "word": "unsubscrib", "weight": 4.103 }, ...]`
  - Palabras en forma **stemmed**. `weight` = score discriminativo (cuánto más probable es la palabra en esta clase vs las demás)
- **Errores**: 404 si la categoría no existe, 503 si el modelo no está cargado
- **Código**: [model_analytics.py](../backend/app/routers/model_analytics.py) líneas 45–57

#### `GET /health`

- **Responde**: `{ "status": "ok", "model_loaded": true }` — Código: [main.py](../backend/app/main.py) línea 87

---

<a id="s16"></a>

## 16. Preguntas Técnicas Típicas y Cómo Responderlas

**¿Por qué Naive Bayes y no una red neuronal?**

> Naive Bayes es interpretable, rápido de entrenar, no necesita GPU, funciona bien con texto cuando las clases son semánticamente distintas. Para este tipo de clasificación de soporte al cliente con categorías claras, es suficiente y más explicable.

**¿Qué es alpha y cómo lo eligieron?**

> Es el parámetro de suavizamiento de Laplace (línea 22 de [classifier.py](../backend/app/naive_bayes/classifier.py)). Alpha=1 es el valor clásico ("add-one smoothing"). Se puede tunear con validación cruzada, pero 1.0 es el punto de partida estándar y funcionó bien.

**¿Por qué se usan logaritmos?**

> Para evitar underflow numérico. Multiplicar muchas probabilidades pequeñas resulta en números tan pequeños que la computadora los redondea a cero. Los logaritmos convierten multiplicaciones en sumas, que son numéricamente estables.

**¿Qué significa que el modelo sea "generativo"?**

> Naive Bayes es un modelo generativo porque modela P(palabras | clase) — cómo se genera el texto a partir de la clase. Contrasta con modelos discriminativos (como regresión logística) que modelan P(clase | palabras) directamente.

**¿Cómo manejan palabras que no estaban en el vocabulario?**

> Con el token `__UNSEEN__` (líneas 99–101 de [classifier.py](../backend/app/naive_bayes/classifier.py)). Al entrenar, se precalcula la probabilidad de Laplace para una palabra con count=0 en cada clase, y eso es lo que se usa cuando el modelo ve una palabra nueva.

**¿Por qué softmax al final?**

> Los scores en log-space no son probabilidades — son números negativos sin cota. Softmax los normaliza para que sumen 1 y sean interpretables como "confianza". Implementado en [`_softmax()`](../backend/app/naive_bayes/classifier.py) líneas 196–203.

**¿Cómo saben que no hay overfitting?**

> El K-Fold Cross Validation con 5 folds muestra 99.14% de accuracy en datos no vistos, versus 99.29% en el set completo. La diferencia de 0.15% es mínima — el modelo generaliza bien.

**¿Qué harías para mejorar el modelo?**

> (1) TF-IDF en vez de conteos crudos, (2) ajustar alpha con búsqueda de hiperparámetros, (3) n-gramas (bigrams) para capturar frases frecuentes, (4) modelo discriminativo como regresión logística o SVM para comparar.

**¿Por qué Macro F1 y no Weighted F1?**

> Macro F1 trata todas las clases igual. En soporte al cliente, ignorar tickets de SUBSCRIPTION es tan malo como ignorar ACCOUNT, sin importar que ACCOUNT tenga 3x más ejemplos.

**¿Qué es la matriz de confusión y cómo la lees?**

> Tabla 11×11. Fila = clase real, columna = clase predicha. La diagonal son aciertos. Fuera de la diagonal son errores. Si `matrix[DELIVERY][SHIPPING]` es alto, el modelo confunde DELIVERY con SHIPPING — exactamente lo que ocurre aquí.

---

<a id="s17"></a>

## 17. Resumen Visual del Flujo Completo

```
Dataset (26,872 tickets)
        |
        ▼
   Preprocesamiento
   (lowercase → tokenize → stopwords → stemming)
        |
        ▼
   Vocabulario: 2,509 tokens
        |
        ▼
        FIT
   ┌──────────────────────────────────────┐
   │ log_prior[clase] = log P(clase)      │
   │                                      │
   │ log_likelihood[clase][word] =        │
   │   log((count + α) / (total + α×|V|))│
   └──────────────────────────────────────┘
        |
        ▼
   model.pkl (serializado)


        PREDICCIÓN
        texto nuevo
            |
            ▼
       preprocesar
            |
            ▼
   score(clase) = log_prior[clase]
                + Σ log_likelihood[clase][token]
            |
            ▼
   clase = argmax(scores)
   confianza = softmax(scores)
            |
            ▼
   {"category": "CANCEL", "confidence": 0.97, ...}
```

Referencias de código del flujo:

| Paso                   | Archivo                                                                      |
| ---------------------- | ---------------------------------------------------------------------------- |
| Preprocesamiento       | [preprocessor.py](../backend/app/naive_bayes/preprocessor.py) — líneas 30–60 |
| fit() — log prior      | [classifier.py](../backend/app/naive_bayes/classifier.py) — líneas 82–83     |
| fit() — log likelihood | [classifier.py](../backend/app/naive_bayes/classifier.py) — líneas 88–101    |
| Serialización          | [model_io.py](../backend/app/naive_bayes/model_io.py)                        |
| predict() — scoring    | [classifier.py](../backend/app/naive_bayes/classifier.py) — líneas 106–149   |
| predict() — softmax    | [classifier.py](../backend/app/naive_bayes/classifier.py) — líneas 196–203   |

---

<a id="s18"></a>

## 18. Datos Clave para Memorizar

| Dato                   | Valor                                 |
| ---------------------- | ------------------------------------- |
| Dataset                | Bitext Customer Support (HuggingFace) |
| Número de docs         | 26,872                                |
| Número de clases       | 11                                    |
| Tamaño del vocabulario | 2,509 tokens                          |
| Alpha (Laplace)        | 1.0                                   |
| K en K-Fold            | 5                                     |
| Accuracy full dataset  | 99.29%                                |
| Macro F1 full dataset  | 99.28%                                |
| Mean Accuracy K-Fold   | 99.14% ± 0.04%                        |
| Mean Macro F1 K-Fold   | 99.13% ± 0.04%                        |
| Clase con menor F1     | DELIVERY (96.15%)                     |
| Backend                | FastAPI (Python)                      |
| Implementación         | Desde cero, sin scikit-learn          |

---

<a id="s19"></a>

## 19. Mapa de Archivos del Proyecto

| Archivo                                                                 | Qué hace                                                                             | Líneas clave             |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------ |
| [classifier.py](../backend/app/naive_bayes/classifier.py)               | Clase `NaiveBayesMultinomial`: `fit()`, `predict()`, `get_top_words()`, `_softmax()` | 47–104, 106–149, 171–203 |
| [preprocessor.py](../backend/app/naive_bayes/preprocessor.py)           | Pipeline de texto: `preprocess()`, `tokenize_only()`                                 | 30–60, 63–69             |
| [evaluator.py](../backend/app/naive_bayes/evaluator.py)                 | Métricas: accuracy, precision, recall, F1, K-Fold, confusion matrix                  | 11–91, 94–157            |
| [model_io.py](../backend/app/naive_bayes/model_io.py)                   | Serialización/deserialización del modelo entrenado                                   | —                        |
| [routers/classifier.py](../backend/app/routers/classifier.py)           | Endpoint `POST /api/v1/classifier/predict`                                           | 9–19                     |
| [routers/model_analytics.py](../backend/app/routers/model_analytics.py) | Endpoints `GET /api/v1/model/*`                                                      | 21–57                    |
| [routers/tickets.py](../backend/app/routers/tickets.py)                 | CRUD de tickets con auto-clasificación                                               | 24–87                    |
| [routers/auth.py](../backend/app/routers/auth.py)                       | Login, refresh, logout, me                                                           | 16–54                    |
| [models/prediction.py](../backend/app/models/prediction.py)             | Schemas `PredictRequest` y `PredictionResponse`                                      | 4–13                     |
| [models/metrics.py](../backend/app/models/metrics.py)                   | Schemas de respuesta para analítica del modelo                                       | 4–47                     |
| [models/ticket.py](../backend/app/models/ticket.py)                     | Schemas de ticket (create, update, response, paginated)                              | 4–34                     |
| [main.py](../backend/app/main.py)                                       | App FastAPI, lifespan, montaje de routers                                            | 61–96                    |
| [scripts/train.py](../backend/scripts/train.py)                         | Script para entrenar y guardar el modelo                                             | —                        |
