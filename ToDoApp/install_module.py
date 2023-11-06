

def install_framework(framework_name:str):
    try:
        import framework_name
    except ImportError:
        import subprocess
        subprocess.check_call(["pip3", "install", framework_name])
        import psycopg2


if __name__ == "__main__":
    install_framework("pandas")
    