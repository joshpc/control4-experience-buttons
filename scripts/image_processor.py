from PIL import Image
import shutil
from pathlib import Path

class ImageProcessor:
    def __init__(self, input_image: str, output_dir: Path):
        self.input_image = input_image
        self.output_dir = output_dir
        self.icons_path = output_dir / "icons" / "device"

    def process_images(self):
        """Generate all required image sizes and variations"""
        self.icons_path.mkdir(parents=True, exist_ok=True)

        try:
            img = Image.open(self.input_image)
            self._generate_experience_icons(img)
            self._create_device_icons()
            return True
        except Exception as e:
            print(f"Error processing images: {str(e)}")
            return False

    def _generate_experience_icons(self, img: Image.Image):
        """Generate experience icons in all required sizes"""
        sizes = [1024, 512, 300, 90, 70, 32, 16]

        for size in sizes:
            resized = img.copy()
            resized.thumbnail((size, size), Image.Resampling.LANCZOS)
            output_path = self.icons_path / f"experience_{size}.png"
            resized.save(output_path, "PNG")
            print(f"Generated: {output_path}")

    def _create_device_icons(self):
        """Create device_sm.png and device_lg.png from existing experience icons"""
        shutil.copy(
            self.icons_path / "experience_32.png",
            self.output_dir / "icons" / "device_sm.png"
        )
        shutil.copy(
            self.icons_path / "experience_90.png",
            self.output_dir / "icons" / "device_lg.png"
        )
