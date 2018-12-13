import data_img



def This_should_make_a_png_file_of_a_dog_named_file_in_this_directory():
	#encode
	cat = data_img.data_img("https://thumbs.dreamstime.com/b/cat-dragon-li-tabby-cat-small-to-medium-sized-cats-102707061.jpg") #file can be local or a uri
	cat.encode_file("https://www.publicdomainpictures.net/pictures/40000/nahled/dog-cartoon.jpg") #s/a
	cat.save("file.png")

	#decode
	seceret_img = data_img.data_img("file.png")
	seceret_img.decode_file() #this creates the file in the current directory

def this_should_encode_hello_world_into_the_created_image():
	test = data_img.data_img("file.png") 
	test.hide_text("hello world")
	test.save("test.png")
def this_should_return_the_encoded_text_from_the_created_image():
	test1 = data_img.data_img("test.png")
	return test1.retreve_text()

if __name__ == '__main__':
	This_should_make_a_png_file_of_a_dog_named_file_in_this_directory() #works on my machine o_o
	this_should_encode_hello_world_into_the_created_image() #s/a
	assert this_should_return_the_encoded_text_from_the_created_image() == "hello world" #These are really bad tests :(
	print()
	print("all tests done")