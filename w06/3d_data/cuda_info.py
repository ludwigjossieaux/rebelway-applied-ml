import torch

print("=" * 50)
print("PyTorch CUDA Information")
print("=" * 50)

print(f"\nPyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"\nCUDA Version: {torch.version.cuda}")
    print(f"\nNumber of CUDA Devices: {torch.cuda.device_count()}")

    for i in range(torch.cuda.device_count()):
        print(f"\n--- Device {i} ---")
        print(f"Name: {torch.cuda.get_device_name(i)}")
        print(f"Compute Capability: {torch.cuda.get_device_capability(i)}")
        print(f"Total Memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")
        print(f"Multi Processor Count: {torch.cuda.get_device_properties(i).multi_processor_count}")
else:
    print("\nNo CUDA devices available.")

print("\n" + "=" * 50)
