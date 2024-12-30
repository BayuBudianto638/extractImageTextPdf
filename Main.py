import fitz  # PyMuPDF
import os

class Page:
    def __init__(self, title, page_number, text, images):
        self.title = title
        self.page_number = page_number
        self.text = text
        self.images = images
        self.metadata = {}

class Book:
    def __init__(self, title, external_company_id=None):
        self.title = title
        self.external_company_id = external_company_id
        self.texts = []  # Store text from pages
        self.figures = []  # Store image paths

    def add_text(self, text):
        """ Add extracted text to the book """
        self.texts.append(text)

    def add_figure(self, figure):
        """ Add figure (image) to the book """
        self.figures.append(figure)

class PDFImporter:
    def __init__(self):
        pass

    def get_local_file_path(self, filename: str):
        """Simulate getting local file path for the PDF."""
        return filename  # Placeholder implementation

    def _extract_images_from_page(self, page, doc, page_num) -> list:
        """ Extract images from a given page and return a list of image streams with indices """
        image_list = []
        image_list_info = page.get_images(full=True)

        for img_index, img in enumerate(image_list_info):
            xref = img[0]  # The image reference
            base_image = self._get_image_from_xref(xref, doc)

            # Save image directly to the disk without using a file stream
            image_path = f"extracted_images/page_{page_num}_image_{img_index}.png"
            with open(image_path, "wb") as img_file:
                img_file.write(base_image)  # Save the raw image data

            # Append image information to the list (including the saved image path)
            image_list.append({
                "index": img_index,  # Image index
                "page": page_num,  # Page number where the image is located
                "path": image_path  # Path to the saved image
            })

        return image_list

    def _get_image_from_xref(self, xref: int, doc) -> bytes:
        """ Retrieve an image from a given xref (reference) in PyMuPDF """
        base_image = doc.extract_image(xref)
        return base_image["image"]

    def _read_pdf(self, filename: str, external_company_id: str = None, force: bool = False) -> str:
        print("Reading PDF file:", filename)
        file_path = self.get_local_file_path(filename)

        title = filename.replace(".pdf", "")
        doc = fitz.open(file_path)

        # Directory to store extracted images
        image_save_dir = "extracted_images"
        if not os.path.exists(image_save_dir):
            os.makedirs(image_save_dir)

        book = Book(title=title, external_company_id=external_company_id)

        all_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # Extract images and save them to disk with unique filenames
            image_list = self._extract_images_from_page(page, doc, page_num)
            for img_info in image_list:
                image_path = img_info["path"]

                # Upload image to the bucket
                print(f"Uploaded image to bucket: {image_path}")

                # Add image to the book's figures list
                book.add_figure(img_info)

            # Add page text to the book
            page_text = page.get_text("text")
            book.add_text(page_text)

        self.import_book(book)

        return all_text

    def import_book(self, book: Book):
        """ Simulate storing the book data including text and images """
        print(f"Importing book: {book.title}")

        # Process each text (page's text)
        for page_text in book.texts:
            print(f"Text from page: \n{page_text}")

        # Process the images (page figures)
        for figure in book.figures:
            print(f"Image saved: {figure['path']}")

# Driver code to run the extraction process
if __name__ == "__main__":
    # Path to your PDF file
    pdf_file = "/home/bayu-budianto/Downloads/Learn_from_Defect_Build_No_01_Floor_Epoxy_Coating_Peeling_Off.pdf"  # Change to your file path

    # Instantiate the PDFImporter class
    pdf_importer = PDFImporter()

    # Read the PDF, extract images and text, and upload images to the bucket
    pdf_importer._read_pdf(pdf_file)
