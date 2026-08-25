# Task 01 --- AI Intake Form & Data Extraction UI

## Objective

Build the first version of the Streamlit application for the AI-led
Cancellation Request Processing workflow.

This task is focused on: 1. Uploading an intake form/document. 2.
Supporting PDF, image, DOCX, and TXT inputs. 3. Sending the uploaded
document to an AI extraction engine. 4. Extracting fields and values. 5.
Displaying extracted information in a table. 6. Providing an
AI-suggested value only when a field value cannot be extracted. 7.
Allowing the user to extract another document. 8. Exporting the
displayed table to Excel.

Do not implement eligibility validation, CLIC case creation, routing,
status updates, or analytics in this task.

## Initial UI

The initial screen must contain: - File upload field. - `Extract`
button.

Supported formats: - PDF - PNG - JPG/JPEG - DOCX - TXT

The Extract button must be disabled when no file is selected and enabled
when a valid file is selected.

## Extraction Flow

``` text
File Upload
    ↓
Extract Button
    ↓
Identify Document Type
    ↓
Read / Prepare Document
    ↓
OCR where required
    ↓
AI Analysis
    ↓
Structured Field Extraction
    ↓
Suggested Values for Missing Fields
    ↓
Display Extracted Data Table
```

Show a spinner/progress indication while processing.

## Document Processing

### PDF

Support both text-based and scanned PDFs. - Text PDF → text extraction →
AI. - Scanned PDF → rendering/OCR/multimodal AI → AI.

### Images

Support PNG/JPG/JPEG. Use OCR and/or multimodal AI for labels, values,
form fields, tables, printed text, and handwriting where supported.

### DOCX

Extract paragraphs, tables, headings, and form-like structures.

### TXT

Read the text directly and send it to the extraction service.

Do not assume fixed field positions.

## AI Extraction Service

Create:

``` python
extract_document_data(uploaded_file) -> ExtractionResult
```

The UI must not contain document parsing or LLM-specific logic.

The AI should dynamically identify fields present in the uploaded intake
form rather than relying on a hard-coded field list.

Use a unified LLM gateway so OpenAI/Llama can be supported without
changing the UI.

## Extraction Table

After successful extraction, display an `Extracted Data` table with
exactly these columns:

  --------------------------------------------------------------------------
  Field Type     Field Name     Field Value    Extracted from Suggested
                                               Document       value
  -------------- -------------- -------------- -------------- --------------

  --------------------------------------------------------------------------

### Field Type

AI-determined type/category such as Text, Number, Date, Boolean, Email,
Phone, Account, Address, or Identifier.

### Field Name

The field/label identified in the intake document. Preserve the original
label where possible.

### Field Value

The value explicitly extracted from the document. If no usable value is
found, leave this column empty. Never put a guessed value here.

### Extracted from Document

Allowed values are only `Yes` and `No`. - Yes = a usable value was
identified in the uploaded document. - No = no usable value was found.

### Suggested value

Populate this column **only when Field Value is empty**.

Example:

``` text
Field Value: John Smith
Suggested value:
```

If no value was extracted:

``` text
Field Value:
Suggested value: Not available
```

Never overwrite an extracted value with a suggestion.

AI suggestions must not be presented as facts. Do not hallucinate
sensitive information such as account numbers, card numbers, or customer
identifiers.

## Structured AI Response

Use a validated structure such as:

``` json
{
  "fields": [
    {
      "field_type": "Text",
      "field_name": "Customer Name",
      "field_value": "John Smith",
      "extracted_from_document": true,
      "suggested_value": ""
    },
    {
      "field_type": "Date",
      "field_name": "Cancellation Date",
      "field_value": "",
      "extracted_from_document": false,
      "suggested_value": "Not available"
    }
  ]
}
```

Validate the AI response using Pydantic or an equivalent typed schema.

Retain source/provenance internally where possible:

``` json
{
  "field_name": "Customer Name",
  "field_value": "John Smith",
  "extracted_from_document": true,
  "source": {
    "document": "intake_form.pdf",
    "page": 1
  }
}
```

## UI After Extraction

Display:

``` text
Uploaded File:
customer_cancellation_form.pdf

Extracted Data

| Field Type | Field Name | Field Value | Extracted from Document | Suggested value |
|------------|------------|-------------|--------------------------|-----------------|
| Text       | Name       | John Smith  | Yes                      |                 |
| Date       | Cancel Dt. |             | No                       | Not available   |

[ Extract Another File ]    [ Export ]
```

Use a Streamlit table/dataframe component.

## Extract Another File

Add an `Extract Another File` button after extraction.

When clicked: - Clear the current uploaded file. - Clear extraction
result. - Clear extracted table. - Reset relevant session state. -
Return to the initial upload screen. - Preserve application/model
configuration.

## Export

Add an `Export` button after successful extraction.

Generate an Excel workbook containing exactly the data displayed in the
table.

Required columns: - Field Type - Field Name - Field Value - Extracted
from Document - Suggested value

Use `openpyxl` and Streamlit `st.download_button()`.

Recommended filename:

``` text
extracted_data_<timestamp>.xlsx
```

Do not add hidden fields to the exported workbook.

## Session State

Maintain:

``` python
st.session_state["uploaded_file"]
st.session_state["extraction_result"]
st.session_state["extracted_table"]
st.session_state["workflow_step"]
```

Recommended states:

``` text
INITIAL
EXTRACTING
EXTRACTED
```

Flow:

``` text
INITIAL → EXTRACTING → EXTRACTED
EXTRACTED → Extract Another File → INITIAL
```

## Error Handling

Handle: - Unsupported file - Empty file - Corrupt file - OCR failure -
Document parsing failure - AI API failure - Invalid AI response - Schema
validation failure - Excel generation failure

Show user-friendly errors. Never expose API keys, secrets, stack traces,
or sensitive provider details.

## Suggested Project Structure

``` text
project/
├── app.py
├── ui/
│   └── intake_ui.py
├── services/
│   ├── document_processor.py
│   ├── extraction_service.py
│   └── export_service.py
├── llm/
│   ├── gateway.py
│   ├── openai_adapter.py
│   └── llama_adapter.py
├── models/
│   └── extraction.py
├── utils/
│   └── session_state.py
├── tests/
│   ├── test_document_processor.py
│   ├── test_extraction_service.py
│   └── test_export_service.py
├── requirements.txt
└── README.md
```

## Acceptance Criteria

### Initial Screen

-   [ ] File upload field is displayed.
-   [ ] PDF is supported.
-   [ ] PNG is supported.
-   [ ] JPG/JPEG is supported.
-   [ ] DOCX is supported.
-   [ ] TXT is supported.
-   [ ] Extract is disabled when no file is selected.
-   [ ] Extract becomes enabled when a valid file is selected.

### AI Extraction

-   [ ] Clicking Extract analyzes the selected file with AI.
-   [ ] PDFs can be analyzed.
-   [ ] Images can be analyzed.
-   [ ] DOCX files can be analyzed.
-   [ ] TXT files can be analyzed.
-   [ ] Scanned/image-based documents can be processed.
-   [ ] AI returns structured field data.
-   [ ] AI response is schema validated.

### Table

-   [ ] Extracted Data table appears after successful extraction.
-   [ ] Table contains Field Type.
-   [ ] Table contains Field Name.
-   [ ] Table contains Field Value.
-   [ ] Table contains Extracted from Document.
-   [ ] Table contains Suggested value.
-   [ ] Extracted from Document contains only Yes/No.
-   [ ] Suggested value is populated only when Field Value is empty.
-   [ ] Extracted values are never overwritten by suggestions.

### Actions

-   [ ] Extract Another File is displayed after extraction.
-   [ ] Extract Another File resets the extraction state.
-   [ ] Export is displayed after successful extraction.
-   [ ] Export generates an `.xlsx` file.
-   [ ] Excel contains exactly the five displayed columns.
-   [ ] Excel contains all displayed rows.
-   [ ] Download is provided through Streamlit.

### Quality

-   [ ] UI is separated from document processing and AI services.
-   [ ] Credentials are not exposed.
-   [ ] Errors are handled gracefully.
-   [ ] Unit tests are implemented.
-   [ ] README includes setup and execution instructions.

## Out of Scope

Do not implement: - Eligibility validation - Business rules - HITL
approval workflow - CLIC case creation - CLIC template mapping -
Routing - Status updates - Reporting - Analytics

## Expected User Flow

``` text
Application Opens
       ↓
File Upload
       ↓
No File → Extract Disabled
       ↓
File Selected
       ↓
Extract Enabled
       ↓
Click Extract
       ↓
AI Analyzes Document
       ↓
Extracted Data Table
       ↓
┌─────────────────────────────┐
│ Extract Another File        │
│ Export                      │
└─────────────────────────────┘
```
