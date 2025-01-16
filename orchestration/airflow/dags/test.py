import os
import pwd

# Get user ID
user_id = os.getuid()

# Get username
user_info = pwd.getpwuid(user_id)
user_name = user_info.pw_name

print(f"User ID: {user_id}")
print(f"User Name: {user_name}")
