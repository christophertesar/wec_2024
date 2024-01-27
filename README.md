# WEC 2024 - DEVELOPER DOCUMENTATION

![Ez-Note logo](https://github.com/christophertesar/wec_2024/assets/74273268/bdabbf0f-0039-4608-a079-6f3c28dc2c43)

## Description

Ez-Note is an intuitive voice note application designed to enhance productivity and accessibility. With features such as speech-to-text transcription, image to text transcription, and text to speech, Ez-Note is ideal for users looking to efficiently capture and organize their thoughts, schoolwork, and meetings.

All frontend content is located in the main.py. The api calls  are located in the Backend folder, and these are called by buttons on the frontent. The Database is locally stored int he project folder

## Features

- **Speech-to-Text**: Transcribe recorded audio to text using advanced speech recognition technology.
- **Image-to-Text**: Transcribe images of writing to text using advanced OCR.
- **Text-to-Speech**: Use Text-to-Speech to get your notes dicated to you.
- **File Management**: Save, organize, and retrieve voice notes and transcriptions with ease.
- **Custom File Naming**: Rename your files upon saving for better organization.
- **Dark Mode**: Built-in dark mode for reduced eye strain in low-light conditions.
- **UI Scaling**: Built-in UI Scaling for those with impaired vision.


## Getting Started

### Prerequisites

- Python 3.8 or later
- Pip for Python package installation

### Installation

1. Clone the repository to your local machine:

    ```sh
    git clone https://github.com/christophertesar/wec_2024/
    ```

2. Navigate to the project directory:

    ```sh
    cd wec_2024
    ```

3. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Download tesseract-ocr-w64-setup-5.3.3.20231005.exe from the main project folder


### Running the Application

To launch the WEC 2024 application, run the following command in the project directory:

```sh
python main.py
