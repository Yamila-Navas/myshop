# 🛍️ MyShop – Django Online Shop

Proyecto de **tienda online**

---

## 🚀 Funcionalidades implementadas

### 🧱 Catálogo de productos

* Modelos de productos y categorías
* Administración completa desde Django Admin
* Vistas y templates para listado y detalle de productos

### 🛒 Carrito de compras

* Carrito basado en **sessions**
* Agregar, eliminar y actualizar cantidades
* Context processor para acceso global al carrito
* Persistencia del carrito entre requests

### 📦 Órdenes

* Registro de órdenes de clientes
* Modelos de órdenes e ítems de orden
* Integración con el panel de administración

### ⚡ Tareas asíncronas

* Uso de **Celery** para tareas en background
* **RabbitMQ** como message broker
* Monitoreo de tareas con **Flower**

### 💳 Pagos con Stripe

* Integración de **Stripe Checkout**
* Uso de tarjetas de prueba
* Webhooks para notificaciones de pago
* Asociación de pagos Stripe con órdenes

### 📄 Gestión avanzada de órdenes

* Exportación de órdenes a CSV
* Acciones personalizadas en el admin
* Generación de **facturas PDF**
* Envío de PDFs por email

### 🧾 PDFs

* Generación dinámica de PDFs con **WeasyPrint**
* Templates HTML para facturas

### 🎟️ Cupones y descuentos

* Sistema de cupones
* Aplicación de cupones al carrito
* Integración de cupones con Stripe
* Inclusión de cupones en órdenes y PDFs

### 🤖 Recomendaciones

* Motor de recomendaciones
* Productos sugeridos basados en compras previas

---

## 🧰 Tecnologías usadas

* Python 3.12
* Django 5+
* SQLite (desarrollo)
* Celery
* RabbitMQ
* Stripe API
* WeasyPrint
* sorl-thumbnail
* django-localflavor

---

## ▶️ Ejecución del proyecto

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Para Celery:

```bash
celery -A core worker -l info
```

Para Flower:

```bash
celery -A core flower
```

---

## 📚 Estado del proyecto

✔ Proyecto funcional
✔ Base sólida para una tienda real

---

Hecho con paciencia, mate y mucho Django 💙