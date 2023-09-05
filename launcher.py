from rembg import remove

input_path = 'test/art_0.png'
output_path = 'test/output.png'

with open(input_path, 'rb') as i:
    with open(output_path, 'wb') as o:
        input = i.read()
        output = remove(input)
        o.write(output)

