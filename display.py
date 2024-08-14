#!pip3 install plantweb
from IPython.display import display, Image, SVG

path = "/content/UML/orders_examples/"
os.chdir(path)
file_name="config"
f_in=file_name+".puml"

file_format="png" # ["svg", "png"]

os.system(f"plantweb --format {file_format} --no-cache {f_in}") #!plantweb --no-cache $f_in
#https://plantweb.readthedocs.io/#command-line-interface

f_out=file_name+"."+file_format
if file_format=="svg": display(SVG(filename=f_out))
elif file_format=="png": display(Image(filename=f_out))
