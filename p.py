import pdfplumber

# Ask user for file name and search text
pdf_file = "pdfs/30.pdf"
search_text = input("Enter text to search: ").lower()

try:
    with pdfplumber.open(pdf_file) as pdf:
        found = False
        print(f"\nSearching for '{search_text}' in {pdf_file}...\n")

        # Loop through each page
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            # Split text into lines for better readability
            lines = text.split('\n')

            for line_num, line in enumerate(lines, start=1):
                if search_text in line.lower():
                    print(f"Page {page_num}, Line {line_num}: {line.strip()}")
                    found = True

        if not found:
            print("No matching text found in the PDF.")

except FileNotFoundError:
    print("Error: PDF file not found.")
except Exception as e:
    print(f"An error occurred: {e}")
