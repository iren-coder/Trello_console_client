import setuptools  
  
with open("README.md", "r") as fh:  
 long_description = fh.read()  
setuptools.setup(  
 name="trello_client-basics-api-iren_e", 
 version="0.0.1", 
 author="IRINA_E", 
 author_email="ira@gmail.com", 
 description="Консольный клиент для trello", 
 long_description=long_description, 
 long_description_content_type="text/markdown", 
 url="https://github.com/iren-coder/d1.9.trello_console_client", 
 packages=setuptools.find_packages(), 
 classifiers=[ "Programming Language :: Python :: >= 3.6.3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ], 
 python_requires='>=3.6',)  