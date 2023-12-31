from PIL import Image

from cryptography.fernet import Fernet

def encrypt_text(text, password):
    key = password
    f = Fernet(key)
    token = f.encrypt(f"{text}".encode())
    return token
    
def hide_text(source_image_path, text, password, output_image_path):
    # Encrypt the text
    encrypted_text = encrypt_text(text, password)

    # Open the source image
    source_image = Image.open(source_image_path)
    source_pixels = source_image.load()

    # Check if the source image can hold the encrypted text
    max_text_length = source_image.size[0] * source_image.size[1] * 3
    if len(encrypted_text) > max_text_length:
        print("Error: Source image is too small to hide the text.")
        return

    # Convert the encrypted text to binary
    binary_text = ''.join(format(byte, '08b') for byte in encrypted_text)

    # Embed the binary text into the source image using LSB steganography
    text_index = 0
    for i in range(source_image.size[0]):
        for j in range(source_image.size[1]):
            # Get the RGB values of the source image pixel
            source_pixel = source_pixels[i, j]

            # Modify the LSBs of the source image pixel to hide the text
            modified_pixel = (
                source_pixel[0] & 0xFE | int(binary_text[text_index]),
                source_pixel[1] & 0xFE | int(binary_text[text_index+1]),
                source_pixel[2] & 0xFE | int(binary_text[text_index+2])
            )

            # Update the pixel in the source image
            source_pixels[i, j] = modified_pixel

            # Move to the next three bits of the binary text
            text_index += 3
            if text_index >= len(binary_text):
                break
        else:
            continue
        break

    # Save the resulting image
    source_image.save(output_image_path)
    print("Text hiding completed.")

source_image_path = 'D:\_CNS\image2.png'
output_image_path = 'D:\_CNS\output.png'
password = 'aubTy1HQbRRurbytmh_NJE2DV3QaNSh8A-ju4p3ZJCY='
text = 'Tommorrow Mass Bunk guys'

hide_text(source_image_path, text, password, output_image_path)

