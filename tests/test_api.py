import pytest
from src.main import clean_phone

def test_clean_phone():
    # Teste com formato brasileiro completo
    assert clean_phone("(11) 98765-4321") == "+55 11 98765 4321"
    
    # Teste sem DDD (deve manter apenas dígitos)
    assert clean_phone("98765-4321") == "987654321"
    
    # Teste com código de país explícito
    assert clean_phone("+55 11 987654321") == "+55 11 98765 4321"
    
    # Teste com código de país implícito (55)
    assert clean_phone("5511987654321") == "+55 11 98765 4321"
    
    # Teste com espaços diferentes
    assert clean_phone("11 98765 4321") == "+55 11 98765 4321"
    
    # Teste com traços
    assert clean_phone("11-98765-4321") == "+55 11 98765 4321"
    
    # Teste com número internacional (não deve modificar)
    assert clean_phone("+1 123 456 7890") == "+1 123 456 7890"
    
    # Teste com número incompleto (menos de 8 dígitos)
    assert clean_phone("1234-567") == "1234567"
