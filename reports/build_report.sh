#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
SOURCE_HTML="$SCRIPT_DIR/report_source.html"
DOCX_OUT="$SCRIPT_DIR/report.docx"
PDF_OUT="$SCRIPT_DIR/report.pdf"
TMP_TXT="$SCRIPT_DIR/.report_build_tmp.txt"

textutil -convert docx "$SOURCE_HTML" -output "$DOCX_OUT"
textutil -convert txt "$SOURCE_HTML" -output "$TMP_TXT"
cupsfilter -m application/pdf "$TMP_TXT" > "$PDF_OUT"
rm -f "$TMP_TXT"
