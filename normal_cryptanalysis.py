from PIL import Image
import re
import nltk
from nltk.corpus import words

nltk.download('words')
english_words = set(words.words())

def extract_text_from_image(image_path, bit_depth):
    image = Image.open(image_path)
    width, height = image.size

    binary_text = ""
    for w in range(width):
        for h in range(height):
            pixel = image.getpixel((w, h))
            lsb = pixel[-1] & ((1 << bit_depth) - 1)  # Extract LSB bits based on bit depth
            binary_text += format(lsb, f'0{bit_depth}b')

    text = ""
    for i in range(0, len(binary_text), 8):
        byte = binary_text[i:i+8]
        if byte == '00000000':  # Check for null terminator
            break
        text += chr(int(byte, 2))  # Convert binary to ASCII character

    return text

def analyze_hidden_text(hidden_text):
    hidden_text = re.sub(r'[^a-zA-Z\s]', '', hidden_text.lower())

    words = hidden_text.split()

    if not words:
        return 0.0  # Return 0 if no alphabetic characters found

    english_word_count = sum(word in english_words or word + 's' in english_words or word + 'es' in english_words for word in words)
    english_word_percentage = (english_word_count / len(words)) * 100

    return english_word_percentage

# Example usage
steganographic_image_path = 'D:\_CNS\output.png'
bit_depths = [5,1,2,3,4]  # Adjust the bit depths to try different LSB extraction approaches

for bit_depth in bit_depths:
    hidden_text = extract_text_from_image(steganographic_image_path, bit_depth)
    print(f"\nExtracted Text with LSB bit depth {bit_depth}:")
    print(hidden_text)

    percentage = analyze_hidden_text(hidden_text)
    print(f"English Word Percentage: {percentage:.2f}%")
