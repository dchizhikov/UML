import os
os.system("pip install plantweb")
from IPython.display import display, Image, SVG

path = "/content/UML/orders_examples/"
file_name="config"
file_format="png" # ["svg", "png"]

def display_scheme(path, file_name, file_format="svg"):
  os.chdir(path)
  f_in=file_name+".puml"
  os.system(f"plantweb --format {file_format} --no-cache {f_in}") #!plantweb --no-cache $f_in
  #https://plantweb.readthedocs.io/#command-line-interface

  f_out=file_name+"."+file_format
  if file_format=="svg": scheme=SVG(filename=f_out)
  elif file_format=="png": scheme=Image(filename=f_out)
  display(scheme)