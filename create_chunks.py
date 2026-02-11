"""
Create semantic chunks from invoice data
"""
import json
from typing import List, Dict
from pathlib import Path


def format_invoice_as_text(invoice_data: Dict) -> str:
    """
    Convert structured invoice data to searchable text
    
    Args:
        invoice_data: Parsed invoice fields
    
    Returns:
        Formatted text representation
    """
    text_parts = []
    
    # Common invoice fields (adjust based on actual structure)
    field_mapping = {
        'company': 'Company',
        'vendor': 'Vendor',
        'invoice_number': 'Invoice Number',
        'invoice_date': 'Date',
        'due_date': 'Due Date',
        'total': 'Total Amount',
        'subtotal': 'Subtotal',
        'tax': 'Tax',
        'address': 'Address',
        'items': 'Line Items'
    }
    
    for field, label in field_mapping.items():
        if field in invoice_data:
            value = invoice_data[field]
            
            # Handle nested structures
            if isinstance(value, list):
                if value:  # Non-empty list
                    text_parts.append(f"{label}: {', '.join(str(v) for v in value)}")
            elif isinstance(value, dict):
                text_parts.append(f"{label}: {json.dumps(value)}")
            elif value:  # Non-empty value
                text_parts.append(f"{label}: {value}")
    
    # Add any other fields not in mapping
    for key, value in invoice_data.items():
        if key not in field_mapping and value:
            text_parts.append(f"{key}: {value}")
    
    return "\n".join(text_parts)


def create_invoice_chunks(
    data_file: str = "data/invoices_data.json",
    output_file: str = "data/chunks.json"
) -> List[Dict]:
    """
    Create searchable chunks from invoice data
    
    Each invoice becomes one chunk (invoices are already atomic)
    """
    print(f"Loading invoice data from {data_file}")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        invoices = json.load(f)
    
    chunks = []
    
    for invoice in invoices:
        # Convert invoice to searchable text
        text = format_invoice_as_text(invoice['data'])
        
        # Add file name context
        full_text = f"Invoice: {invoice['file_name']}\n\n{text}"
        
        chunks.append({
            "id": invoice['id'],
            "text": full_text,
            "metadata": {
                "file_name": invoice['file_name'],
                "source_index": invoice['metadata']['source_index'],
                "has_image": invoice['metadata']['has_image'],
                "structured_data": invoice['data']  # Keep original structured data
            }
        })
    
    # Save chunks
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    
    print(f"Created {len(chunks)} invoice chunks")
    print(f"Saved to {output_file}")
    
    # Show sample
    print("\nSample chunk:")
    print(chunks[0]['text'][:500])
    
    return chunks


if __name__ == "__main__":
    chunks = create_invoice_chunks(
        data_file="data/invoices_data.json",
        output_file="data/chunks.json"
    )