import platform
import psutil
from tabulate import tabulate
import subprocess

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
    print("\n=== GPU Information ===\n")
    if GPUtil:
        try:
            gpus = GPUtil.getGPUs()
            if not gpus:
                print("No NVIDIA GPU detected.")
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
        except Exception as e:
            print("Error while fetching GPU information:", e)
    else:
        print("GPUtil is not installed. Checking for other GPU devices...\n")
        try:
            result = subprocess.run(['lshw', '-C', 'display'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout:
                print(result.stdout.strip())
            else:
                print("No GPU information found. Ensure drivers are installed or run the command with super-user privileges.")
        except FileNotFoundError:
            print("`lshw` command not found. Please install it to check GPU information.")

def main():
    get_cpu_info()
    get_gpu_info()

if __name__ == "__main__":
    main()
