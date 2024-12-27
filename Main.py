import fitz  # PyMuPDF
import os
import time


class Book:
    def __init__(self, title=None, external_company_id=None):
        self.title = title
        self.external_company_id = external_company_id
        self.pages = []
        self.figures = []
        self.texts = []
        self.book_id = None

    def validate_book_attributes(self):
        if not self.title:
            raise ValueError("Book title is required.")
        # Add other validation as needed.

    def get_title(self):
        return self.title

    def get_external_company_id(self):
        return self.external_company_id

    def get_texts(self):
        return self.texts

    def set_book_id(self, book_id):
        self.book_id = book_id

    def add_text(self, text):
        self.texts.append(text)

    def get_figures(self):
        return self.figures


class Page:
    def __init__(self, title, page_number, text, images):
        self.title = title
        self.page_number = page_number
        self.text = text
        self.images = images
        self.metadata = {}


class PDFImporter:
    def _read_pdf(self, filename: str, external_company_id: str = None, force: bool = False) -> None:
        print("Reading PDF file:", filename)
        file_path = self.get_local_file_path(filename)

        title = filename.replace(".pdf", "")

        # Open the PDF using PyMuPDF
        doc = fitz.open(file_path)

        # Create the book object
        book = Book(title=title, external_company_id=external_company_id)

        # Open a text file to save extracted text
        with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
            # Loop through each page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)

                # Extract text from the page
                page_text = page.get_text("text")
                text_file.write(f"--- Page {page_num + 1} ---\n")
                text_file.write(page_text)
                text_file.write("\n\n")

                # Extract images from the page
                image_list = self._extract_images_from_page(page, doc)

                # Add page data to book
                page_obj = Page(title=title, page_number=page_num, text=page_text, images=image_list)
                book.add_text(page_text)  # Adding text to book's texts
                book.figures.extend(image_list)  # Adding images to book's figures list

        print("Total pages to import:", len(book.get_texts()))

        # Call method to import the book
        self.import_book(book)

    def _extract_images_from_page(self, page, doc) -> list:
        """ Extract images from a given page and save them to a list """
        image_list = []
        image_list_info = page.get_images(full=True)

        for img_index, img in enumerate(image_list_info):
            xref = img[0]  # The image reference
            base_image = self._get_image_from_xref(xref, doc)
            image_filename = f"extracted_images/page_{page.number}_img_{img_index + 1}.png"

            # Save image to disk
            with open(image_filename, "wb") as img_file:
                img_file.write(base_image)

            image_list.append(image_filename)

        return image_list

    def _get_image_from_xref(self, xref: int, doc) -> bytes:
        """ Retrieve an image from a given xref (reference) in PyMuPDF """
        base_image = doc.extract_image(xref)
        return base_image["image"]

    def get_local_file_path(self, filename: str) -> str:
        """ Adjust to use the provided full file path """
        return filename  # Directly returning the provided path

    def import_book(self, book: Book) -> str:
        # Check book data condition
        print("[Weaviator] Check book data received...")
        book.validate_book_attributes()

        # Start importing the book
        start = time.time()
        print(f"[Weaviator] Importing '{book.get_title()}' book...")

        # Simulating a batch processing (you will implement your storage logic)
        company_id = "mock_company_id"
        book_id = "mock_book_id"

        print("[Weaviator] Book ID:", book_id)

        if company_id is not None:
            print("[Weaviator] Adding company reference to book...")

        # Add text objects to batch (text pages from the book)
        total_text = len(book.get_texts())
        count = 0
        for index, text in enumerate(book.get_texts()):
            print(f"[Weaviator] Adding text {index + 1}/{total_text} to batch...")
            count += 1

        # Add images (figures or images from the book)
        total_images = len(book.get_figures())
        for index, image in enumerate(book.get_figures()):
            print(f"[Weaviator] Adding image {index + 1}/{total_images} to batch...")

        # Simulating successful processing and import
        stop = time.time()
        print("[Weaviator] Import completed in {:.2f} seconds".format(stop - start))
        return book_id


# Driver code to run the extraction process
if __name__ == "__main__":
    # Path to your PDF file
    pdf_file = "/home/bayu-budianto/Downloads/JUDO JAKARTA OPEN 2024 - results CADET.pdf"

    # Create directory to save extracted images if it doesn't exist
    if not os.path.exists("extracted_images"):
        os.makedirs("extracted_images")

    # Instantiate the PDFImporter class
    pdf_importer = PDFImporter()
    pdf_importer._read_pdf(pdf_file)
