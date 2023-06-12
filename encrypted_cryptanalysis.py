from PIL import Image
import nltk

# Download the NLTK corpus if not already downloaded
nltk.download('punkt')
nltk.download('words')

# Get the English words corpus
english_words = set(nltk.corpus.words.words())

def extract_text(image_path):
    # Open the image
    image = Image.open(image_path)
    pixels = image.load()

    # Extract the LSBs from each pixel
    binary_text = ""
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # Get the RGB values of the image pixel
            pixel = pixels[i, j]

            # Extract the LSBs and append them to the binary text
            binary_text += str(pixel[0] & 0x01)
            binary_text += str(pixel[1] & 0x01)
            binary_text += str(pixel[2] & 0x01)

    # Convert the binary text to bytes
    extracted_text = ""
    for i in range(0, len(binary_text), 8):
        byte = binary_text[i : i + 8]
        extracted_text += chr(int(byte, 2))

    return extracted_text

def cryptanalysis(encrypted_image_path):
    # Extract the hidden text from the encrypted image
    extracted_text = extract_text(encrypted_image_path)

    if extracted_text:
        # Tokenize the extracted text into sentences
        sentences = nltk.sent_tokenize(extracted_text)

        # Check if the extracted sentences contain valid English words
        valid_sentences = []
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            valid_words = [word for word in words if word.lower() in english_words]
            if valid_words:
                valid_sentences.append(sentence)

        if valid_sentences:
            print("Cryptanalysis successful.")
            print("Valid English sentences found in the extracted text:")
            for sentence in valid_sentences:
                print(sentence)
        else:
            print("Cryptanalysis failed. No valid English sentences found.")
    else:
        print("Cryptanalysis failed. No hidden text found.")

# Provide the path to the encrypted image
encrypted_image_path = "D:\_CNS\output.png"

# Perform cryptanalysis
cryptanalysis(encrypted_image_path)
