import torch
print(f"CUDA Mevcut mu?: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Ekran Kartı İsmi: {torch.cuda.get_device_name(0)}")