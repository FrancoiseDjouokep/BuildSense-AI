import pytest
from fastapi import HTTPException

from app.modules.upload.service import detect_mime_type, validate_filename_and_content


@pytest.mark.parametrize(
    ("filename", "header", "expected"),
    [
        ("plan.pdf", b"%PDF-1.7", "application/pdf"),
        ("plan.png", b"\x89PNG\r\n\x1a\n", "image/png"),
        ("plan.jpg", b"\xff\xd8\xff\xe0", "image/jpeg"),
        ("plan.tiff", b"II*\x00", "image/tiff"),
    ],
)
def test_accepts_supported_file_with_matching_signature(
    filename: str, header: bytes, expected: str
) -> None:
    assert detect_mime_type(header) == expected
    assert validate_filename_and_content(filename, header) == expected


def test_rejects_mismatched_extension_and_content() -> None:
    with pytest.raises(HTTPException, match="does not match"):
        validate_filename_and_content("plan.pdf", b"\x89PNG\r\n\x1a\n")


def test_rejects_unknown_extension() -> None:
    with pytest.raises(HTTPException, match="Unsupported file extension"):
        validate_filename_and_content("plan.exe", b"MZ")
