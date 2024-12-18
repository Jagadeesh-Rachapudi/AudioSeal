import platform
import psutil
from tabulate import tabulate

# Try to import GPUtil to get GPU information
try:
    import GPUtil
except ImportError:
    GPUtil = None

def get_cpu_info():
    print("\n=== CPU Information ===\n")
    cpu_info = {
        "Processor": platform.processor(),
        "Architecture": platform.architecture()[0],
        "Cores (Logical)": psutil.cpu_count(logical=True),
        "Cores (Physical)": psutil.cpu_count(logical=False),
        "CPU Frequency": f"{psutil.cpu_freq().max:.2f} MHz" if psutil.cpu_freq() else "N/A",
        "Total RAM": f"{round(psutil.virtual_memory().total / 1e9, 2)} GB"
    }
    for key, value in cpu_info.items():
        print(f"{key}: {value}")

def get_gpu_info():
    if not GPUtil:
        print("\nGPUtil is not installed. Skipping GPU info.\n")
        return

    print("\n=== GPU Information ===\n")
    gpus = GPUtil.getGPUs()
    if not gpus:
        print("No GPU found.")
        return

    gpu_list = []
    for gpu in gpus:
        gpu_list.append((
            gpu.id,
            gpu.name,
            f"{gpu.memoryTotal} MB",
            f"{gpu.memoryUsed} MB",
            f"{gpu.memoryFree} MB",
            f"{gpu.load * 100:.2f}%",
            f"{gpu.temperature} °C"
        ))

    print(tabulate(gpu_list, headers=["ID", "Name", "Total Memory", "Used Memory", "Free Memory", "Load", "Temperature"]))

def main():
    get_cpu_info()
    get_gpu_info()

if __name__ == "__main__":
    main()
