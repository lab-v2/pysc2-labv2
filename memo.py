import subprocess
import atexit
import os
import time
filename = "multiunit_runtime_tank.py"

# specify the command line arguments
arg1 = "[[left,up,left],[left,up,left]]"
arg2 = "[[up,nop,up],[up,nop,up]]"
from memory_profiler import memory_usage

# Run the Python file using the mprof command-line tool
# start_time = time.time()
process = subprocess.Popen(["python", filename, arg1, arg2])
# end_time = time.time()
# total_time = end_time - start_time
# Register a function to print the memory usage results
pid = os.getpid()

# Register a function to print the memory usage results
def print_memory_usage():
    try:
        mem_usage = memory_usage(pid)
        #print("Total time taken:", total_time, "seconds")
        print(f"Memory usage: {mem_usage[-1]} MiB")

        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
    except ProcessLookupError:
        print("Error: Process ID not found")

atexit.register(print_memory_usage)
start_time = time.time()
# Wait for the process to finish
try:
    process.wait()
except KeyboardInterrupt:
    process.kill()
    process.wait()