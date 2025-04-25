import pytest
import time
import math
from func import es_primo

# GRUPO 1: PRUEBAS PARA NÚMEROS PRIMOS Y NO PRIMOS CONOCIDOS
@pytest.mark.parametrize("num", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31])
def test_numeros_primos(num):
    """
    Verifica que la función identifique correctamente los números primos conocidos.
    Estos números solo son divisibles por 1 y por sí mismos, por lo que deben
    ser identificados como primos.
    """
    assert es_primo(num) == True, f"Error: {num} debería ser primo"

@pytest.mark.parametrize("num", [0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20])
def test_numeros_no_primos(num):
    """
    Verifica que la función identifique correctamente los números no primos conocidos.
    Estos números tienen divisores adicionales además de 1 y ellos mismos, por lo que
    no deben ser identificados como primos. Los casos especiales 0 y 1 tampoco son
    primos por definición matemática.
    """
    assert es_primo(num) == False, f"Error: {num} no debería ser primo"

# GRUPO 2: PRUEBAS PARA CASOS ESPECIALES
def test_caso_especial_0():
    """
    Verifica que 0 no sea considerado primo.
    Por definición matemática, 0 no es un número primo ya que tiene infinitos divisores.
    """
    assert es_primo(0) == False, "Error: 0 no debería ser primo"

def test_caso_especial_1():
    """
    Verifica que 1 no sea considerado primo.
    Por definición matemática, 1 no es un número primo ya que solo tiene un divisor (él mismo).
    Un número primo debe tener exactamente dos divisores distintos.
    """
    assert es_primo(1) == False, "Error: 1 no debería ser primo"

def test_caso_especial_2():
    """
    Verifica que 2 sea considerado primo.
    2 es el único número primo par y el más pequeño de todos los números primos.
    """
    assert es_primo(2) == True, "Error: 2 debería ser primo"

# GRUPO 3: PRUEBAS PARA NÚMEROS NEGATIVOS
@pytest.mark.parametrize("num", [-1, -2, -3, -5, -11, -13])
def test_numeros_negativos(num):
    """
    Verifica que los números negativos no sean considerados primos.
    Por convención matemática, los números primos se definen solo para enteros positivos.
    """
    assert es_primo(num) == False, f"Error: {num} (negativo) no debería ser primo"

# GRUPO 4: PRUEBAS PARA TIPOS DE DATOS NO ENTEROS
@pytest.mark.parametrize("num", [2.3, 3.9, "tres", None, True, False])
def test_tipos_no_enteros(num):
    """
    Verifica que la función lance TypeError para entradas que no son enteros.
    La primalidad solo está definida para números enteros, por lo que la función
    debe rechazar otros tipos de datos con un error apropiado.
    """
    with pytest.raises(TypeError):
        es_primo(num)

# GRUPO 5: PRUEBAS PARA VALORES FLOTANTES ESPECIALES
def test_infinito_positivo():
    """
    Verifica que la función maneje correctamente el infinito positivo.
    Infinity no es un entero y no puede evaluarse como primo o no primo,
    por lo que debe lanzar un TypeError.
    """
    with pytest.raises(TypeError):
        es_primo(float('inf'))

def test_infinito_negativo():
    """
    Verifica que la función maneje correctamente el infinito negativo.
    -Infinity no es un entero y no puede evaluarse como primo o no primo,
    por lo que debe lanzar un TypeError.
    """
    with pytest.raises(TypeError):
        es_primo(float('-inf'))

def test_nan():
    """
    Verifica que la función maneje correctamente el valor NaN (Not a Number).
    NaN no representa un número válido y no puede evaluarse como primo o no primo,
    por lo que debe lanzar un TypeError.
    """
    with pytest.raises(TypeError):
        es_primo(float('nan'))

# GRUPO 6: PRUEBAS PARA PRECISIÓN EN PUNTO FLOTANTE
@pytest.mark.parametrize("num", [19.000000000000004, 23.000000000000004])
def test_precision_punto_flotante(num):
    """
    Verifica que la función maneje correctamente números de punto flotante
    que están extremadamente cerca de números enteros primos.
    Debido a la imprecisión inherente de los flotantes, estos valores deben
    ser tratados como sus enteros más cercanos para determinar su primalidad.
    """
    assert es_primo(num) == True, f"Error: {num} debería ser reconocido como primo"

def test_precision_flotante_cerca_no_primo():
    """
    Verifica que la función maneje correctamente números de punto flotante
    que están extremadamente cerca de números enteros no primos.
    """
    assert es_primo(4.0000000000000001) == False, "4.0000000000000001 debería ser reconocido como no primo"

def test_precision_flotante_cerca_primo():
    """
    Verifica que la función maneje correctamente números de punto flotante
    que están extremadamente cerca de números enteros primos.
    """
    assert es_primo(5.0000000000000001) == True, "5.0000000000000001 debería ser reconocido como primo"

# GRUPO 7: PRUEBAS PARA EFICIENCIA CON NÚMEROS GRANDES
def test_eficiencia_numero_primo_grande():
    """
    Verifica que la función pueda identificar eficientemente un número primo grande.
    Esta prueba evalúa tanto la corrección (debe identificar 1000003 como primo)
    como la eficiencia (debe hacerlo en un tiempo razonable).
    """
    start_time = time.time()
    result = es_primo(1000003)
    end_time = time.time()
    execution_time = end_time - start_time
    
    assert result == True, "1000003 debería ser primo"
    assert execution_time < 1, f"La función es ineficiente: tomó {execution_time} segundos"

def test_eficiencia_numero_no_primo_grande():
    """
    Verifica que la función pueda identificar eficientemente un número no primo grande.
    1000004 = 2 * 500002, por lo que no es primo y la función debería identificarlo
    correctamente y de manera eficiente.
    """
    start_time = time.time()
    result = es_primo(1000004)
    end_time = time.time()
    execution_time = end_time - start_time
    
    assert result == False, "1000004 no debería ser primo"
    assert execution_time < 1, f"La función es ineficiente: tomó {execution_time} segundos"

def test_numero_muy_grande():
    """
    Verifica que la función maneje correctamente números extremadamente grandes.
    Prueba tanto un número primo grande (10^9 + 7) como un número no primo grande (10^9 + 8).
    """
    # Un número primo muy grande
    big_prime = 10**9 + 7  # 1,000,000,007 es un primo conocido
    assert es_primo(big_prime) == True, f"{big_prime} debería ser primo"
    
    # Un número no primo muy grande
    big_non_prime = 10**9 + 8  # 1,000,000,008 = 2^3 * 5^1 * 2500000
    assert es_primo(big_non_prime) == False, f"{big_non_prime} no debería ser primo"

# GRUPO 8: PRUEBAS PARA FORMATOS ESPECIALES DE ENTEROS
def test_entero_binario():
    """
    Verifica que la función maneje correctamente enteros expresados en formato binario.
    Los enteros binarios son enteros válidos y deben evaluarse correctamente.
    """
    assert es_primo(0b11) == True, "0b11 (3 en decimal) debería ser primo"
    assert es_primo(0b100) == False, "0b100 (4 en decimal) no debería ser primo"

def test_entero_octal():
    """
    Verifica que la función maneje correctamente enteros expresados en formato octal.
    Los enteros octales son enteros válidos y deben evaluarse correctamente.
    """
    assert es_primo(0o7) == True, "0o7 (7 en decimal) debería ser primo"
    assert es_primo(0o10) == False, "0o10 (8 en decimal) no debería ser primo"

def test_entero_hexadecimal():
    """
    Verifica que la función maneje correctamente enteros expresados en formato hexadecimal.
    Los enteros hexadecimales son enteros válidos y deben evaluarse correctamente.
    """
    assert es_primo(0x11) == True, "0x11 (17 en decimal) debería ser primo"
    assert es_primo(0x12) == False, "0x12 (18 en decimal) no debería ser primo"

# GRUPO 9: PRUEBAS PARA TIPOS DE DATOS INUSUALES
def test_numero_complejo():
    """
    Verifica que la función rechace correctamente números complejos.
    La primalidad no está definida para números complejos, por lo que
    la función debe lanzar un TypeError.
    """
    with pytest.raises(TypeError):
        es_primo(3+0j)

def test_string_numerico():
    """
    Verifica que la función rechace correctamente strings que parecen números.
    Aunque "17" parece un número primo, la función debe rechazarlo porque
    es un string, no un entero.
    """
    with pytest.raises(TypeError):
        es_primo("17")

# GRUPO 10: PRUEBAS PARA COMPORTAMIENTO CON ARGUMENTOS MÚLTIPLES
def test_multiples_argumentos():
    """
    Verifica que la función maneje correctamente el caso de recibir múltiples argumentos.
    La función está diseñada para recibir un solo argumento, por lo que debe fallar
    apropiadamente si se le pasan más.
    """
    with pytest.raises(TypeError):
        es_primo(5, 7)  # Intentar pasar dos números primos
