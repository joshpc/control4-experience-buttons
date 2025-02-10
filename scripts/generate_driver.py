import sys
from pathlib import Path
from image_processor import ImageProcessor
from driver_generator import DriverGenerator, DriverConfig


def get_user_input():
    """Get all required information from user interactively"""
    print("\n=== Control4 UI Button Driver Generator ===\n")

    # Get device information
    device_name = input("Enter device name [generates uibutton_<devicename> driver] (e.g., xbox): ").strip()
    manufacturer = input("Enter manufacturer name (e.g., Microsoft): ").strip()
    model_name = input("Enter model name (e.g., Xbox Series X): ").strip()
    creator = input("Enter creator name (default: Unknown): ").strip() or "Unknown"

    # Get image path
    while True:
        image_path = input("\nEnter path to source image (PNG format recommended): ").strip()
        if Path(image_path).exists():
            break
        print("Error: File does not exist. Please try again.")

    # Get optional settings
    print("\n=== Optional Settings ===")
    print("Press Enter to use defaults")

    version = input("Enter driver version (default: 100): ").strip() or "100"
    min_os = input("Enter minimum OS version (default: 2.9.0): ").strip() or "2.9.0"

    documentation = input("Enter driver documentation (Press Enter for default): ").strip()
    if not documentation:
        documentation = f"""Control4 UI Button Driver for the {model_name}

Although it is not possible to control this device from Control4 this driver enables it to be displayed on the Control4 UI and for the Control4 system to switch the necessary AV settings."""

    return DriverConfig(
        device_name=device_name,
        manufacturer=manufacturer,
        model_name=model_name,
        creator=creator,
        version=version,
        min_os=min_os,
        documentation=documentation
    ), image_path


def main():
    try:
        # Get information interactively
        config, image_path = get_user_input()
        driver_name = f"uibutton_{config.device_name.lower()}"
        base_path = Path(driver_name)

        print("\nGenerating driver...")

        # Generate driver files
        generator = DriverGenerator(config)
        generator.generate(base_path)

        # Process images
        processor = ImageProcessor(image_path, base_path)
        if not processor.process_images():
            print("Failed to process images")
            sys.exit(1)

        print("\n=== Driver Generation Complete ===")
        print(f"Driver location: {driver_name}/")
        print("\nNext steps:")
        print("1. Test the driver in Composer")
        print("2. If sharing via GitHub, update .github/workflows/release.yml")
        print("3. Create a .c4z file by zipping the contents (not the folder)")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
