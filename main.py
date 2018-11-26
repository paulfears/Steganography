import PIL
from PIL import Image as img
import urllib.request as url
import numpy
import io

def encode_text(text, bits_per_char=7):
    text+="\0"
    def convert_to_padded_binary(char):
        bin_value = bin(ord(char))[2:]
        return '0'*(bits_per_char-len(bin_value))+bin_value
    return map(convert_to_padded_binary, text)
    
def decode_text(byte_array):
    def bin_to_char(byte_string):
        return chr(int(byte_string, 2))
        
    return ''.join(map(bin_to_char, byte_array))
    
def get_pil_image(uri):
    image = img.open(io.BytesIO(url.urlopen(uri).read()))
    return image

def decode_text_from_image(pil_image, bits_per_char=7):
    image = pil_image
    pixels = image.load()
    width = image.size[0]
    height = image.size[1]
    output = ""
    last_char = ""
    sequence = ''
    kill = False
    for y in range(height):
        if(kill):
            break
        for x in range(width):
            
            if(kill):
                break
            for i in range(3):
                last_bit = bin(pixels[x,y][i])[2:][-1]
                
                sequence += last_bit
                if(len(sequence) == bits_per_char):
                    last_char = chr(int(sequence, 2))
                    sequence = ''
                    if(last_char == '\0'):
                        kill = True
                        break
                    
                    output+=last_char
    return output
                    
    
                
        

def calculate_max_text_size(pil_image):
    return pil_image.size[0]*pil_image.size[1]
  
def hide_text_in_image(pil_image, text):
    def sub_last_bit_in_int(num, bit):
        num = list(bin(num)[2:])
        num[-1] = str(bit)
        return int(''.join(num), 2)    
    image = pil_image
    pixels = pil_image.load()
    bits = ''.join(encode_text(text))
    bit_length = len(bits)
    width = image.size[0]
    height = image.size[1]
    bit_index = 0
    kill = False
    for y in range(height):
        if(kill):
            break
        for x in range(width):
            colors = list(pixels[x,y])
            for i in range(3):
                colors[i] = sub_last_bit_in_int(colors[i], bits[bit_index])
                bit_index+=1
                if(bit_index>bit_length-1):
                    kill = True
                    break
            pixels[x,y] = tuple(colors)
            if(kill):
                break
                
    return pil_image



if(__name__ == '__main__'):
    img1 = get_pil_image("https://s7d9.scene7.com/is/image/zumiez/cat_max/adidas-Men-s-Trefoil-Curved-Bill-Khaki-Strapback-Hat-_272694.jpg")
    """
    pixels1 = img1.load()
    
    for i in range(100):
        print(pixels1[i,0])
    
    img2 = hide_text_in_image(img1, "hello world")
    pixels2 = img2.load()
    for i in range(100):
        print(pixels2[i,0])
    """
    img2 = hide_text_in_image(img1, "hello world and this is a really really really long string hopefully it works")
    text = decode_text_from_image(img2)
    print(text)
    
