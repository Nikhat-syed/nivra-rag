"""
Stage 3 — PDF Extraction Engine (Docling + Graceful Fallback)
Extracts structured text and tables from all PDFs in data/raw_pdfs/
and saves them as formatted text files in data/processed/.
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def extract_pdf_content(pdf_path: Path) -> str:
    """
    Extract text and table structures from a single PDF using Docling,
    falling back to pypdf or PyMuPDF if Docling fails or is unavailable.
    """
    text_content = ""
    
    # Try Docling extraction first (preserves rich layout and tables)
    try:
        from docling.document_converter import DocumentConverter
        converter = DocumentConverter()
        result = converter.convert(str(pdf_path))
        text_content = result.document.export_to_markdown()
        if text_content and len(text_content.strip()) > 50:
            logger.info(f"Successfully extracted with Docling: {pdf_path.name}")
            return text_content
    except Exception as e:
        logger.warning(f"Docling extraction failed or skipped for {pdf_path.name}: {e}. Falling back to pypdf.")

    # Fallback to PyPDF
    try:
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        extracted_pages = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_pages.append(f"--- PAGE {i+1} ---\n" + page_text)
        text_content = "\n\n".join(extracted_pages)
        if text_content and len(text_content.strip()) > 20:
            logger.info(f"Successfully extracted with pypdf fallback: {pdf_path.name}")
            return text_content
    except Exception as e:
        logger.warning(f"pypdf extraction failed for {pdf_path.name}: {e}")

    # Fallback to raw bytes decoding if standard text is embedded
    try:
        with open(pdf_path, "rb") as f:
            raw = f.read()
            # Basic text recovery from stream
            decoded = raw.decode("utf-8", errors="ignore")
            lines = [line.strip() for line in decoded.splitlines() if len(line.strip()) > 10 and not line.startswith("%PDF")]
            text_content = "\n".join(lines)
            if len(text_content.strip()) > 30:
                logger.info(f"Extracted plain text stream fallback: {pdf_path.name}")
                return text_content
    except Exception as e:
        logger.error(f"All extraction methods failed for {pdf_path.name}: {e}")

    return ""

def process_all_pdfs(raw_dir: str = None, processed_dir: str = None):
    """
    Scans raw_dir for PDFs, extracts content, and writes to processed_dir.
    Prints a detailed execution summary scaling cleanly to 100+ documents.
    """
    base_dir = Path(__file__).resolve().parent.parent.parent
    if raw_dir is None:
        raw_dir = base_dir / "data" / "raw_pdfs"
    else:
        raw_dir = Path(raw_dir)

    if processed_dir is None:
        processed_dir = base_dir / "data" / "processed"
    else:
        processed_dir = Path(processed_dir)

    processed_dir.mkdir(parents=True, exist_ok=True)
    pdf_files = list(raw_dir.glob("*.pdf"))

    if not pdf_files:
        logger.warning(f"No PDF files found in {raw_dir}. Please place scheme PDFs in data/raw_pdfs/")
        return {"total": 0, "success": 0, "failed": 0}

    logger.info(f"Starting ingestion process for {len(pdf_files)} PDF file(s) in {raw_dir}...")
    
    success_count = 0
    failed_count = 0
    processed_summary = []

    for pdf_path in pdf_files:
        out_txt_filename = pdf_path.stem + ".txt"
        out_txt_path = processed_dir / out_txt_filename
        
        content = extract_pdf_content(pdf_path)
        
        if content and len(content.strip()) > 0:
            with open(out_txt_path, "w", encoding="utf-8") as f:
                f.write(content)
            success_count += 1
            char_count = len(content)
            processed_summary.append((pdf_path.name, out_txt_filename, "SUCCESS", char_count))
        else:
            logger.warning(f"Skipped corrupt/empty PDF: {pdf_path.name}")
            failed_count += 1
            processed_summary.append((pdf_path.name, out_txt_filename, "FAILED (Unreadable)", 0))

    # Print Summary Report
    print("\n" + "="*70)
    print("                STAGE 3: INGESTION SUMMARY REPORT                 ")
    print("="*70)
    print(f"Total Source PDFs Found : {len(pdf_files)}")
    print(f"Successfully Extracted  : {success_count}")
    print(f"Failed / Unreadable     : {failed_count}")
    print("-" * 70)
    for src, dst, status, length in processed_summary:
        print(f" • {src:<35} -> {dst:<35} | {status:<10} | ({length} chars)")
    print("="*70 + "\n")

    return {
        "total": len(pdf_files),
        "success": success_count,
        "failed": failed_count,
        "summary": processed_summary
    }

if __name__ == "__main__":
    process_all_pdfs()
