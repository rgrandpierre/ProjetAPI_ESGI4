# 📘 FastAPI Orders API

## 🚀 Introduction
Cette API permet aux utilisateurs authentifiés de gérer des commandes (CRUD). Elle utilise OAuth2 avec JWT pour l'authentification.

## 📌 Installation

Assurez-vous d'avoir Python installé, puis :
```sh
pip install fastapi uvicorn
```
Lancez le serveur avec :
```sh
uvicorn main:app --reload
```
L'API sera accessible sur `http://127.0.0.1:8000`.

## 🔑 Authentification

Avant d'effectuer des requêtes sécurisées, obtenez un token JWT :
### 🔹 Obtenir un token
**POST `/authenticate`**
```sh
curl -X POST "http://127.0.0.1:8000/authenticate" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin"}'
```
**Réponse :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer"
}
```
Utilisez ce token pour toutes les requêtes suivantes avec le header `Authorization: Bearer <TOKEN>`.

---
## 📌 Endpoints

### 🔹 Créer un utilisateur
**POST `/users`**
```sh
curl -X POST "http://127.0.0.1:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"username": "new_user", "password": "securepass"}'
```
**Réponse :**
```json
{"message": "User created"}
```

### 🔹 Lister les commandes
**GET `/orders`** _(authentification requise)_
```sh
curl -X GET "http://127.0.0.1:8000/orders" \
     -H "Authorization: Bearer <TOKEN>"
```
**Réponse :**
```json
{"orders": [...], "user": "admin"}
```

### 🔹 Créer une commande
**POST `/orders`** _(authentification requise)_
```sh
curl -X POST "http://127.0.0.1:8000/orders" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{"product": "Laptop", "quantity": 2}'
```
**Réponse :**
```json
{
  "id": 1,
  "product": "Laptop",
  "quantity": 2,
  "user": "admin"
}
```

### 🔹 Mettre à jour une commande (PUT)
**PUT `/orders/{order_id}`** _(authentification requise)_
```sh
curl -X PUT "http://127.0.0.1:8000/orders/1" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{"product": "Smartphone", "quantity": 5}'
```

### 🔹 Modifier partiellement une commande (PATCH)
**PATCH `/orders/{order_id}`** _(authentification requise)_
```sh
curl -X PATCH "http://127.0.0.1:8000/orders/1" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{"quantity": 10}'
```

### 🔹 Supprimer une commande
**DELETE `/orders/{order_id}`** _(authentification requise)_
```sh
curl -X DELETE "http://127.0.0.1:8000/orders/1" \
     -H "Authorization: Bearer <TOKEN>"
```
**Réponse :**
```json
{"message": "Order deleted"}
```

---
## 🛠️ Technologies utilisées
- FastAPI
- OAuth2 JWT
- Curl (pour les tests)

📌 **Auteur :** _Votre Nom_
📌 **Licence :** MIT

