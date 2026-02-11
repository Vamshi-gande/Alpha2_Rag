"""
Download invoice dataset from Hugging Face
"""
from datasets import load_dataset
import json
from pathlib import Path
from PIL import Image


def download_invoice_dataset(
    dataset_name: str = "katanaml-org/invoices-donut-data-v1",
    output_dir: str = "data",
    save_images: bool = False
):
    """
    Download invoice dataset and extract structured data
    
    Args:
        dataset_name: HuggingFace dataset identifier
        output_dir: Directory to save processed data
        save_images: Whether to save invoice images locally
    """
    print(f"Downloading dataset: {dataset_name}")
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    if save_images:
        Path(f"{output_dir}/images").mkdir(exist_ok=True)
    
    # Load dataset
    ds = load_dataset(dataset_name)
    
    # Process train split
    processed_data = []
    
    for idx, item in enumerate(ds['train']):
        # Extract ground truth (invoice data)
        ground_truth = json.loads(item['ground_truth'])
        
        invoice_data = {
            "id": f"invoice_{idx}",
            "file_name": item.get('file_name', f"invoice_{idx}"),
            "data": ground_truth.get('gt_parse', {}),
            "metadata": {
                "source_index": idx,
                "has_image": 'image' in item
            }
        }
        
        processed_data.append(invoice_data)
        
        # Optionally save images
        if save_images and 'image' in item:
            img_path = f"{output_dir}/images/invoice_{idx}.png"
            item['image'].save(img_path)
    
    # Save processed data
    output_file = f"{output_dir}/invoices_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(processed_data)} invoices")
    print(f"Saved to {output_file}")
    
    # Show sample structure
    print("\nSample invoice structure:")
    print(json.dumps(processed_data[0], indent=2))
    
    return processed_data


if __name__ == "__main__":
    download_invoice_dataset(
        dataset_name="katanaml-org/invoices-donut-data-v1",
        output_dir="data",
        save_images=False  # Set True if you want to save invoice images
    )