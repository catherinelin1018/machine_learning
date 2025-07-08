import shutil
import random
from pathlib import Path
from typing import List, Dict

def create_output_dirs(base_dir: Path, splits: List[str], categories: List[str]) -> None:
    for split in splits:
        for category in categories:
            path = base_dir / split / category
            path.mkdir(parents=True, exist_ok=True)

def load_images_from_category(category_dir: Path) -> List[Path]:
    return [p for p in category_dir.rglob("*") if p.is_file()]

def split_dataset(images: List[Path], split_ratio: List[float]) -> Dict[str, List[Path]]:
    total = len(images)
    n_train = int(total * split_ratio[0])
    n_val = int(total * split_ratio[1])
    n_test = total - n_train - n_val

    return{
        "train": images[:n_train],
        "val": images[n_train:n_train + n_val],
        "test": images[n_train + n_val:]
    }

def move_images(splits: Dict[str, List[Path]], base_dir: Path, category: str) -> None:
    for split_name, image_paths in splits.items():
        for path in image_paths:
            target_path = base_dir / split_name / category / path.name
            shutil.move(str(path), str(target_path))

def delete_original_category_dir(base_dir: Path, category: str) -> None:
    original_dir = base_dir / category
    if original_dir.exists():
        shutil.rmtree(original_dir)

def process_dataset(base_dir_str: str, categories: List[str], split_ratio: List[float]) -> None:
    base_dir = Path(base_dir_str)
    create_output_dirs(base_dir, ["train", "val", "test"], categories)

    for category in categories:
        image_paths = load_images_from_category(base_dir/category)
        random.shuffle(image_paths)
        splits = split_dataset(image_paths, split_ratio)
        move_images(splits, base_dir, category)
        delete_original_category_dir(base_dir, category)
        print(f"{category}: train={len(splits["train"])}, val={len(splits["val"])}, test={len(splits["test"])}")

if __name__ == "__main__":
    process_dataset(
        base_dir_str="./datasets/Interior-Exterior Scene Classification",
        categories=["Interior", "Exterior"],
        split_ratio=[0.8, 0.1, 0.1]
    )