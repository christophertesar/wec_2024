from PIL import Image
import pytesseract as ocr

# need to add if path error occurs. Copy paste file location where pytesseract was downloaded
# download is found in backend folder named tesseract-ocr-w64-setup... .exe
# replace USERPATH with appropriate username

# ocr.pytesseract.tesseract_cmd = r'C:\Users\USERPATH\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def image_to_text(file_name):

    # Open image file, convert to text using pytesseract
    image_object = Image.open(file_name)
    ocr_text = ocr.image_to_string(image_object)

    # Construct the output file name by removing the extension from the input file name and appending "_OCR.txt"
    output_text_file = file_name.split('.')[0] + "_OCR.txt"

    # Save the summarized text to the text file
    with open(output_text_file, 'w', encoding='utf-8') as file:
        file.write(ocr_text) 

    print("Summary saved to", output_text_file)
