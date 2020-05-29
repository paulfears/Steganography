# Steganography
a simple bit of Steganography written in python allows for hiding data inside images
<hr>
<h2>description:</h2>
 allows you to hide any file in any image. even if the file is bigger than the image
 uses lsb stegangraphy to encode the file into the last bit of pixel constituant currently allowing 3 its per px
 larger files are encoded into smaller images by resizing the image based on the size of the bigger file
<hr>
<h2>requirements</h2>
  <ul>
  <li>python3</li>
  <li>PIL</li>
  </ul>
<hr>
<h2>useage:</h2>
  simple text encode and retrival
  
```python
    
import data_img #data_imag.py must be in local directory

src = "https://img.wikinut.com/img/_dw4ymezru3_rwsr/jpeg/0/Vincent-van-Gogh-Public-domain-Wikimedia-Commons.jpeg"

#how to encode text into image
    
encoded_image = data_img.data_img(src) #can be local file, data:image, or data_url
encoded_image.hide_text("seceret text") #hides text in image 
encoded_image.save("new_file.png") #must be saved as a .png otherwise .png will be appended


#how retreve text from image
    
img = data_img.data_img("new_file.png")
text = img.retreve_text() #returns seceret text
print(text)
    
```

simple file encode and retrival

```python
import data_img

src = "https://img.wikinut.com/img/_dw4ymezru3_rwsr/jpeg/0/Vincent-van-Gogh-Public-domain-Wikimedia-Commons.jpeg"

#how to encode text into image
img = data_img.data_img(src) #can be local filename as string, data:image as string, or data_url

img.encode_file("https://www.mynutritionclinic.com.au/wp-content/uploads/2017/01/Secret-Public-Domain.jpg")
#encode_file method can accept any file not just images, local or otherwise
img.save("hidden_file.png")


#how to retreve file from image
img = data_img.data_img("hidden_file.png")
img.decode_file() #creates file with identical filename to the one encoded in local directory

```

<hr>
<h2>Other infomation</h2>
<ul>
<li>when using url files a website may turn the request down</li>
<li>larger files can be encoded into smaller ones, but the resulting file will be larger than the original</li>
<ul>
