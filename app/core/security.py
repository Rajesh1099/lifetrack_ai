from pwdlib import PasswordHash  # Imports the password hashing utility.
from app.core.config import settings  # Imports application settings

password_hash = PasswordHash.recommended()  # Creates a recommended Argon2 password hasher.




def hash_password(password: str) -> str:  # Accepts a password string and returns its hash.
    return password_hash.hash(password)  # Converts the original password into a secure hash.


def verify_password(  # Defines a function to verify a password.
    plain_password: str,  # Password entered by the user.
    hashed_password: str  # Previously stored password hash.
) -> bool:  # Returns True if the password matches, otherwise False.
    return password_hash.verify(  # Checks the entered password against the stored hash.
        plain_password,  # Password entered during login.
        hashed_password  # Hash retrieved from the database.
    )

