import PIL
from PIL import Image as img
import urllib.request as url
import base64
import io
import math
import os

class binary_file:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'rb')
        self.size = os.path.getsize(filename)
        self.current_pos = 0
        print(len(self.file.read()))
    def load_file(file_path):
        self.file = open(io.BytesIO(url.urlopen(uri).read()), 'rb')
        


    def __del__(self):
        self.file.close()
    def __iter__(self):
        return self
    def __next__(self):
        nb = self.next_byte()
        if(nb):
            return nb
        raise StopIteration()
    def get_size(self):
        return self.size
    def get_filename(self):
        return self.filename
    def next_byte(self):
        try:
            byte = self.file.read(1)
            byte = bin(ord(byte))[2:]
        except TypeError:
            return False
        return '0'*(8-len(byte))+byte



class data_img:

    def __init__(self,img_path, bits_per_char=8):
        self.pil_image = data_img.load_image(img_path)
        self.max_data_size = data_img
        self.bits_per_char = bits_per_char
        self.pixels = self.pil_image.load()
        self.width, self.height = self.pil_image.size      

    def load_image(img_path):
        def get_pil_image(uri):
            image = img.open(io.BytesIO(url.urlopen(uri).read()))
            return image
        if(str(type(img_path)).startswith("<class 'PIL")): # a clunky check to see if img_path is a PIL image
            pil_image = img_path
        if(os.path.exists(img_path)):
            pil_image = img.open(img_path)
        else:
            try:
                pil_image = get_pil_image(img_path)
            except ValueError:
                raise FileNotFoundError("the file is not found")
        return pil_image

    def map_over_pixels(self, start=0):
        total_px = self.width*self.height
        wi = 0
        hi = 0
        i = start
        while i < total_px:
            wi = i%self.width
            hi = i//self.width
            i +=1
            yield (wi, hi)

    def set_bit(self, index, new_bit_value):
        px_index = index//3
        bit_index = index%3
        wi = px_index%self.width
        hi = px_index//self.width
        num = list(self.pixels[wi, hi])[bit_index]
        bin_value = list(bin(num)[2:])
        bit = bin_value[-1]
        bin_value[-1] = new_bit_value
        new_number = int(''.join(bin_value), 2)
        pixel_values = list(self.pixels[wi,hi])
        pixel_values[bit_index] = new_number
        self.pixels[wi,hi] = tuple(pixel_values) 

    def map_over_bits(self, start=0, bits_per_px=3, end = None):
        total_px = self.width*self.height
        if(end == None):
            end = total_px*bits_per_px
        wi = (start//3)%self.width
        hi = (start//3)//self.width
        i = start
        while i < total_px*bits_per_px and i<end:
            wi = (i//3)%self.width
            hi = (i//3)//self.width
            px = self.pixels[wi,hi]
            yield str(list(bin(px[i%3])[2:])[-1])
            i+=1

    def get_bits(self, start, end):
        return ''.join(list(self.map_over_bits(start=start, end=end)))


    def store_bits(self, bitstring, start=0, bits_per_px=3):
        total_px = self.width*self.height
        wi = (start//3)%self.width
        hi = (start//3)//self.width
        i = start
        j = 0
        new_value = list(self.pixels[wi, hi][:start%bits_per_px])
        while i < total_px*bits_per_px and j<len(bitstring):
            wi = (i//3)%self.width
            hi = (i//3)//self.width
            px = self.pixels[wi,hi]
            new_num = list(bin(px[i%3])[2:])
            new_num[-1] = bitstring[j]
            new_num = int(''.join(new_num), 2)
            new_value.append(new_num)
            if(len(new_value)%bits_per_px == 0):
                self.pixels[wi, hi] = tuple(new_value)
                new_value = []
            i+=1
            j+=1
        if(len(new_value) > 0):
            tmp = len(new_value)
            for i in range(bits_per_px-tmp):
                new_value.append(px[len(new_value)])
            self.pixels[wi, hi] = tuple(new_value)
        return self

    def encode_binary_file(self,filename, bits_per_px=3, bits_per_char=8, start=0):
        file = binary_file(filename)
        data = ''
        data+= data_img.encode_text(file.get_filename(), add_null=True)
        with open(filename, 'rb') as f:
            contents = f.read(4)
            while contents:
                print(str(base64.urlsafe_b64encode(contents))[2:-1])
                data += data_img.encode_text(str(base64.urlsafe_b64encode(contents))[2:-1], add_null=False)
                contents = f.read(4)
        data+=('0'*8)
        pos = start+len(data)-1
        self.resize_image_to_data(len(data))
        self.store_bits(data, start=start)
        return self

    def decode_binary_file(self, start=0):
        pos = start
        char = ''
        filename = ''
        size = ''
        file_contents = ""
        while char != '\0':
            byte = list(self.map_over_bits(start=pos, end=pos+8))
            char = chr(int(''.join(byte), 2))
            filename+=char
            pos +=8
        
        char = ''
        filename = filename[:-1]
        with open(filename, 'wb') as f:
            char8 = ""
            char = ""
            i=0
            while True:
                byte = list(self.map_over_bits(start=pos, end=pos+8))
                char = chr(int(''.join(byte), 2))
                if(char == '\0'):
                    print("break")
                    break
                if(i%8 == 0 and i!=0):
                    print(char8)
                    f.write(base64.urlsafe_b64decode(char8))
                    char8 = ''
                char8+=char
                
                pos = pos+8
                i+=1
        return byte
        

        


    def encode_text(text, bits_per_char=8, add_null=True):
        if(add_null):
            text+="\0"

        def convert_to_padded_binary(char):
            bin_value = bin(ord(char))[2:]
            return '0'*(bits_per_char-len(bin_value))+bin_value
        out = ''.join(map(convert_to_padded_binary, text))
        return out
        
    def decode_text(byte_array):
        def bin_to_char(byte_string):
            return chr(int(byte_string, 2))
            
        return ''.join(map(bin_to_char, byte_array))


    def decode_text_from_image(self):
        image = self.pil_image
        pixels = self.pixels
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
                    if(len(sequence) == self.bits_per_char):
                        last_char = chr(int(sequence, 2))
                        sequence = ''
                        if(last_char == '\0'):
                            kill = True
                            break
                        output+=last_char
        return output
                        

    def resize_image_to_data(self, data_size_bits, resize_method=img.ANTIALIAS):
        needed_pixels = math.ceil(data_size_bits+15/3) #fifteen bits from overhead
        width, height = self.pil_image.size
        scale = math.ceil(math.sqrt(needed_pixels/(width*height)))
        print("scale is ",scale)
        self.pil_image = self.pil_image.resize((width*scale, height*scale), resize_method)
        self.pixels = self.pil_image.load()
        self.width, self.height = self.pil_image.size
        return self

    def calculate_storage_size(self):
        return math.floor((self.pil_image.size[0]*self.pil_image.size[1]*3)/8)

    def save(self, filename):
        if(filename.endswith('.png')):
            pass
        else:
            filename+=".png"
        self.pil_image.save(filename, "PNG")
        return self
      
    def hide_text_in_image(self, text):
        def sub_last_bit_in_int(num, bit):
            num = list(bin(num)[2:])
            num[-1] = str(bit)
            return int(''.join(num), 2)    
        image = self.pil_image
        pixels = self.pixels
        bits = ''.join(data_img.encode_text(text))
        self.current_pos = len(bits)-1
        bit_length = len(bits)
        width, height = image.size
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
                    
        return self



if(__name__ == '__main__'):
    f = data_img("https://thenypost.files.wordpress.com/2018/05/180516-woman-mauled-by-angry-wiener-dogs-feature.jpg?quality=90&strip=all&w=618&h=410&crop=1")
    f.encode_binary_file("s.png").save("file.png")
    print('\n'*3)
    a = data_img("file.png").decode_binary_file()
    print(a)