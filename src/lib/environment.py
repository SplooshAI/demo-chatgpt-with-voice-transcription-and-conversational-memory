# This module manages environment variables and .env file loading
import os
from dotenv import load_dotenv

def load_environment_variables(base_path):
    dotenv_path = os.path.join(base_path, '.env')
    load_dotenv(dotenv_path)

    env_sample_path = os.path.join(base_path, '.env.sample')
    with open(env_sample_path, 'r') as file:
        required_env_vars = [line.split('=')[0] for line in file if line.strip() and not line.startswith('#')]
        missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_env_vars:
        print("💥 Missing environment variables ->\n\n\t", ', '.join(missing_env_vars))
        print("\nPlease ensure that src/.env exists and that you have defined the missing environment variables identified above to run this application.\n")
        exit(1)
