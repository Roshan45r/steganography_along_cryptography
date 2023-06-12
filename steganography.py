from PIL import Image

def hide_text_in_image(image_path, output_path, secret_text):
    image = Image.open(image_path)
    width, height = image.size

    binary_text = ''.join(format(ord(char), '08b') for char in secret_text)
    text_length = len(binary_text)

    if text_length > (width * height):
        raise ValueError("Text too long to fit in the image!")

    index = 0
    for w in range(width):
        for h in range(height):
            if index < text_length:
                pixel = list(image.getpixel((w, h)))
                pixel[-1] = int(binary_text[index])
                new_pixel = tuple(pixel)
                image.putpixel((w, h), new_pixel)
                index += 1

    image.save(output_path)

# Example usage
image_path = 'D:\_CNS\image.png'
output_path = 'D:\_CNS\normal_steganography_output.png'
secret_text = "This is a secret message!"

hide_text_in_image(image_path, output_path, secret_text)

print("Hidden!")
