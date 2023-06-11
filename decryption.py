from PIL import Image

def decrypt_text(encrypted_bytes, password):
    # Convert the encrypted bytes and password to bytes
    password_bytes = password.encode()

    # XOR each byte of the encrypted bytes with the corresponding byte of the password
    decrypted_bytes = bytes(encrypted_byte ^ password_byte for encrypted_byte, password_byte in zip(encrypted_bytes, password_bytes))

    # Convert the decrypted bytes to text
    decrypted_text = decrypted_bytes.decode()

    return decrypted_text

def extract_text(image_path, password):
    # Open the image
    image = Image.open(image_path)
    pixels = image.load()

    # Initialize variables
    binary_text = ""
    text_length = 0

    # Extract the binary text from the LSBs of the image pixels
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # Get the RGB values of the image pixel
            pixel = pixels[i, j]

            # Extract the LSBs and append them to the binary text
            binary_text += str(pixel[0] & 0x01)
            binary_text += str(pixel[1] & 0x01)
            binary_text += str(pixel[2] & 0x01)

            # Check if the end of text marker is reached
            if binary_text[-16:] == "0000000000000000":
                text_length = len(binary_text) - 16
                break
        if text_length > 0:
            break

    # Check if the end of text marker was found
    if text_length == 0:
        print("Error: Text not found in the image.")
        return ""

    # Convert the binary text to bytes
    encrypted_text = bytes(int(binary_text[i:i+8], 2) for i in range(0, text_length, 8))

    # Decrypt the text
    decrypted_text = decrypt_text(encrypted_text, password)

    return decrypted_text

output_image_path = 'D:\_CNS\output.png'
password = 'secret_password'

decrypted_text = extract_text(output_image_path, password)
print('Decrypted Text:', decrypted_text)
