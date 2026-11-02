import platform
import psutil


def system_snapshot():
    snapshot = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_percent": psutil.virtual_memory().percent,
        "cuda": False,
        "gpu": "Unavailable",
        "vram_percent": None,
        "pytorch": "Unavailable",
        "torchvision": "Unavailable",
    }
    try:
        import torch
        snapshot["pytorch"] = torch.__version__
        snapshot["cuda"] = torch.cuda.is_available()
        if snapshot["cuda"]:
            snapshot["gpu"] = torch.cuda.get_device_name(0)
            snapshot["vram_percent"] = round(torch.cuda.memory_allocated(0) / max(torch.cuda.get_device_properties(0).total_memory, 1) * 100, 1)
        try:
            import torchvision
            snapshot["torchvision"] = torchvision.__version__
        except Exception:
            pass
    except Exception:
        pass
    return snapshot
