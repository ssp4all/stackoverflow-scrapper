from subprocess import PIPE, Popen
from queue import Queue
from threading import Thread
import os

def read(pipe, funcs):
    """Reads and pushes piped output to a shared queue and appropriate lists."""
    for line in iter(pipe.readline, b''):
        for func in funcs:
            func(line.decode("utf-8"))
    pipe.close()


def write(get):
    """Pulls output from shared queue and prints to terminal."""
    for line in iter(get, None):
        print(line)

def execute(command):
    """Executes a given command and clones stdout/err to both variables and the
    terminal (in real-time)."""
    
    process = Popen(
        command,
        cwd=None,
        shell=False,
        close_fds=True,
        stdout=PIPE,
        stderr=PIPE,
        bufsize=1
    )

    output, errors = [], []
    pipe_queue = Queue()  # Wowee, thanks CS 225

    # Threads for reading stdout and stderr pipes and pushing to a shared queue
    stdout_thread = Thread(target=read, args=(
        process.stdout, [pipe_queue.put, output.append]))
    stderr_thread = Thread(target=read, args=(
        process.stderr, [pipe_queue.put, errors.append]))

    # Thread for printing items in the queue
    writer_thread = Thread(target=write, args=(pipe_queue.get,))

    # Spawns each thread
    for thread in (stdout_thread, stderr_thread, writer_thread):
        thread.daemon = True
        thread.start()

    process.wait()

    for thread in (stdout_thread, stderr_thread):
        thread.join()

    pipe_queue.put(None)

    output = ' '.join(output)
    errors = ' '.join(errors)

    # File doesn't exist, for java, command[1] is a class name instead of a file
    if "java" != command[0] and not os.path.isfile(command[1]):
        return (None, None)
    else:
        return (output, errors)
