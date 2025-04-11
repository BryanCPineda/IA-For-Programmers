# Importaciones necesarias para construir la API
from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import datetime

# Base de datos simulada para almacenar usuarios
fake_db = {"users": {}}

# Instancia de la aplicación FastAPI
app = FastAPI()

# Modelo de datos para recibir una lista de números
class Payload(BaseModel):
    numbers: List[int]

# Modelo de datos para la búsqueda binaria (lista de números y un objetivo)
class BinarySearchPayload(BaseModel):
    numbers: List[int]
    target: int

# Clave secreta y algoritmo para la generación y verificación de tokens JWT
SECRET_KEY = "ultra_secret_pass123"
ALGORITHM = "HS256"

# Función para verificar el token JWT recibido como parámetro de consulta
def verify_token(token: str = Query(..., description="Token de autenticación")):
    """
    Verifica el token JWT recibido por query parameter.
    Si el token es inválido o no contiene un usuario, lanza una excepción HTTP 401.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return username

# Ruta base para devolver la base de datos simulada
@app.get("/")
def read_root():
    """
    Devuelve la base de datos simulada.
    """
    return fake_db

# Ruta para ordenar una lista de números usando Bubble Sort
@app.post("/bubble-sort")
def bubble_sort(payload: Payload, token: str = Query(..., description="Token de autenticación")):
    """
    Recibe una lista de números y los ordena con Bubble Sort.
    Requiere autenticación mediante un token en query param.
    """
    verify_token(token)  # Verifica el token antes de procesar
    
    numbers = payload.numbers
    if not isinstance(numbers, list):
        raise HTTPException(status_code=400, detail="Formato incorrecto. Se espera una lista de números.")

    n = len(numbers)
    for i in range(n):
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    
    return {"numbers": numbers}

# Ruta para filtrar números pares de una lista
@app.post("/filter-even")
def filter_even(payload: Payload, token: str = Query(..., description="Token de autenticación")):
    """
    Filtra los números pares de una lista.
    Requiere autenticación mediante un token en query param.
    """
    verify_token(token)  # Verifica el token antes de procesar
    
    numbers = payload.numbers
    even_numbers = [num for num in numbers if num % 2 == 0]
    return {"even_numbers": even_numbers}

# Ruta para sumar los elementos de una lista
@app.post("/sum-elements")
def sum_elements(payload: Payload, token: str = Query(..., description="Token de autenticación")):
    """
    Suma los elementos de una lista.
    Requiere autenticación mediante un token en query param.
    """
    verify_token(token)  # Verifica el token antes de procesar
    
    numbers = payload.numbers
    total_sum = sum(numbers)
    return {"sum": total_sum}

# Ruta para encontrar el valor máximo en una lista
@app.post("/max-value")
def max_value(payload: Payload, token: str = Query(..., description="Token de autenticación")):
    """
    Encuentra el valor máximo en una lista.
    Requiere autenticación mediante un token en query param.
    """
    verify_token(token)  # Verifica el token antes de procesar
    
    numbers = payload.numbers
    if not numbers:
        raise HTTPException(status_code=400, detail="The list is empty")
    max_num = max(numbers)
    return {"max": max_num}

# Ruta para realizar una búsqueda binaria en una lista
@app.post("/binary-search")
def binary_search(payload: BinarySearchPayload, token: str = Query(..., description="Token de autenticación")):
    """
    Realiza una búsqueda binaria en una lista.
    Requiere autenticación mediante un token en query param.
    """
    verify_token(token)  # Verifica el token antes de procesar
    
    numbers = payload.numbers
    target = payload.target

    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == target:
            return {"found": True, "index": mid}
        elif numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return {"found": False, "index": -1}

# Modelo de datos para registrar y autenticar usuarios
class User(BaseModel):
    username: str
    password: str

# Contexto de encriptación para las contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para encriptar contraseñas
def get_password_hash(password):
    """
    Encripta una contraseña usando bcrypt.
    """
    return pwd_context.hash(password)

# Ruta para registrar un nuevo usuario
@app.post("/register")
def register(user: User):
    """
    Registra un nuevo usuario en la base de datos simulada.
    """
    if user.username in fake_db["users"]:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed_password = get_password_hash(user.password)
    fake_db["users"][user.username] = hashed_password
    return {"message": "User registered successfully"}

# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    """
    Crea un token JWT con datos y una fecha de expiración opcional.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Ruta para autenticar un usuario y devolver un token JWT
@app.post("/login")
def login(user: User):
    """
    Autentica un usuario y devuelve un token JWT si las credenciales son válidas.
    """
    if user.username not in fake_db["users"]:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    hashed_password = fake_db["users"][user.username]
    if not pwd_context.verify(user.password, hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales Inválidas")
    access_token_expires = datetime.timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token}


