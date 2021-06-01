from PyPDF2 import PdfFileReader


class PdfReader:
    def __init__(self, path_to_file: str):
        self.path_to_file = path_to_file
        self.pdf_content = ""

    def read_pdf_content(self):
        if self.pdf_content:
            self.pdf_content = ""

        with open(self.path_to_file, 'rb') as pdf_file:
            pdf_reader = PdfFileReader(pdf_file)
            number_of_pages = pdf_reader.numPages

            for i in range(0, number_of_pages):
                self.pdf_content += self.__read_page(pdf_reader, i)

        return self.pdf_content

    def __read_page(self, pdf_reader: PdfFileReader, page_number: int):
        return pdf_reader.getPage(page_number).extractText()

    def is_contains(self, value: str):
        if not self.pdf_content:
            self.pdf_content = self.read_pdf_content()

        return value in self.pdf_content
