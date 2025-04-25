# def es_primo(num):
#     for i in range(2, num):
#         if num % i == 0:
#             return False
#     return True


# if __name__ == "__main__":
#     print(es_primo(5))

import math

def es_primo(num):
    # Validación de tipos
    if isinstance(num, bool):
        raise TypeError("El input no debe ser un valor booleano.")
    
    if not isinstance(num, (int, float)):
        raise TypeError("El input debe ser un número entero.")
    
    # Manejo de valores flotantes especiales
    if isinstance(num, float):
        if math.isnan(num) or math.isinf(num):
            raise TypeError("El input no puede ser NaN o infinito.")
        
        # Manejo de números de punto flotante normales
        if abs(num - round(num)) < 1e-9:
            num = round(num)
        else:
            raise TypeError("El input debe ser un número entero.")
    
    # Convertir a entero después de validaciones
    num = int(num)
    
    # Casos especiales y números negativos
    if num < 2:
        return False
    
    # Caso especial para 2 y 3
    if num < 4:
        return True
    
    # Optimización: verificar divisibilidad por 2 y 3 primero
    if num % 2 == 0 or num % 3 == 0:
        return False
    
    # Optimización: verificar solo hasta la raíz cuadrada
    # y solo números de la forma 6k±1
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    
    return True