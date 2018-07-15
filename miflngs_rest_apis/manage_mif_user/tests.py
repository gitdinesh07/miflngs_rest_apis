import base64


'''with open("E:/work_stress.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    print("img_data ",encoded_string)

#data = "this is dinesh".encode('utf-8')
#file = open("E:/profile_image.txt", "rb")
#encoded_string = file.read()
'''
string = "this is diensh".encode('utf-8')
en_str = base64.b64encode(string)
print("encode-",en_str)


userid= "tulsi"
#with open(""+userid+".png", "wb") as fh:
#    fh.write(base64.decodebytes(encoded_string))


