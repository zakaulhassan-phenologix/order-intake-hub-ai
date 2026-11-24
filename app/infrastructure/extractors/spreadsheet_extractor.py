import csv
import io
import logging

from app.infrastructure.extractors.base_extractor import BaseExtractor, ExtractedDocument

logger = logging.getLogger(__name__)


class SpreadsheetExtractor(BaseExtractor):
    supported_extensions: tuple[str, ...] = (".xlsx", ".xls", ".csv")

    async def extract(self, file_bytes: bytes, filename: str) -> ExtractedDocument:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext in ("xlsx", "xls"):
            return self._extract_xlsx(file_bytes, filename)
        if ext == "csv":
            return self._extract_csv(file_bytes, filename)
        raise ValueError(f"SpreadsheetExtractor does not handle '.{ext}' files.")

    def _extract_xlsx(self, file_bytes: bytes, filename: str) -> ExtractedDocument:
        try:
            import openpyxl
        except ImportError as exc:
            raise ImportError("openpyxl is required for XLSX extraction.") from exc

        wb = openpyxl.load_workbook(io.BytesIO(file_bytes), read_only=True, data_only=True)
        all_tables: list[list[list[str]]] = []
        text_blocks: list[str] = []
        total_rows = 0

        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            rows = [[str(cell) if cell is not None else "" for cell in row] for row in ws.iter_rows(values_only=True)]
            all_tables.append(rows)
            total_rows += len(rows)
            text_blocks.append(f"=== Sheet: {sheet_name} ===\n" + "\n".join("\t".join(r) for r in rows))

        wb.close()
        return ExtractedDocument(
            text="\n\n".join(text_blocks),
            tables=all_tables,
            page_count=len(wb.sheetnames),
            source_type="xlsx",
            needs_ocr=False,
            metadata={"filename": filename, "sheet_names": wb.sheetnames, "total_rows": total_rows},
        )

    def _extract_csv(self, file_bytes: bytes, filename: str) -> ExtractedDocument:
        text = file_bytes.decode("utf-8-sig", errors="replace")
        rows = [list(row) for row in csv.reader(io.StringIO(text))]
        return ExtractedDocument(
            text="\n".join("\t".join(row) for row in rows),
            tables=[rows],
            page_count=1,
            source_type="csv",
            needs_ocr=False,
            metadata={"filename": filename, "row_count": len(rows), "col_count": max((len(r) for r in rows), default=0)},
        )
