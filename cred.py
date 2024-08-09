import bcrypt

# Generate a salt
salt = bcrypt.gensalt()

# Hash the password with the salt
password = "your_password".encode('utf-8')
hashed_password = bcrypt.hashpw(password, salt)

# Print the salt and hashed password
print("Salt:", salt)
print("Hashed Password:", hashed_password)
