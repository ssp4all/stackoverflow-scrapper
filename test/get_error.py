# This file will extract error from file passed as extension

########################################
# Get file type by knowing its extension
########################################
def get_language(file_path):
    if file_path.endswith(".py"):
        return "python3"
    elif file_path.endswith(".js"):
        return "node"
    elif file_path.endswith(".go"):
        return "go run"
    elif file_path.endswith(".rb"):
        return "ruby"
    elif file_path.endswith(".class"):
        return "java"
    else:
        return ''#Unknown filetype


########################################
# Extract error 
########################################
def get_error_message():
    pass

