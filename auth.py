import hashlib

def hash_password(password):
    """Genera un hash SHA-256 para una contraseña dada."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password_hash, provided_password):
    """Verifica una contraseña proporcionada contra un hash almacenado."""
    return stored_password_hash == hash_password(provided_password)
