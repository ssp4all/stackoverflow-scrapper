from execution import execute


def get_error_message(file_path, language):
    """Gives error message after execution"""

    if language == 'java':
        file_path = [f.replace('.class', '') for f in file_path]
    
    # Compiles the file and pipes stdout
    output, error = execute([language] + file_path)  # Execute file
    if (output, error) == (None, None):  # Invalid file
        return

    if error == '':
        return None
    elif language == "python3":
        # Non-compiler errors
        if any(e in error for e in ["KeyboardInterrupt", "SystemExit", "GeneratorExit"]):
            return None
        else:
            return error.split('\n')[-2].strip()
    elif language == "node":
        return error.split('\n')[4][1:]
    elif language == "go run":
        return error.split('\n')[1].split(": ", 1)[1][1:]
    elif language == "ruby":
        error_message = error.split('\n')[0]
        return error_message[error_message.rfind(": ") + 2:]
    elif language == "javac":
        m = re.search(r'.*error:(.*)', error.split('\n')[0])
        return m.group(1) if m else None
    elif language == "java":
        for line in error.split('\n'):
            # Multiple error formats
            m = re.search(r'.*(Exception|Error):(.*)', line)
            if m and m.group(2):
                return m.group(2)

            m = re.search(r'Exception in thread ".*" (.*)', line)
            if m and m.group(1):
                return m.group(1)
