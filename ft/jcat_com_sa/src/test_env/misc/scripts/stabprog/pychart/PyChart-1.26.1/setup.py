from distutils.core import setup


setup (name = "PyChart",
       version = "1.26.1",
       description = "Python Chart Generator",
       author = "Yasushi Saito",
       author_email = "ysaito@hpl.hp.com",
       url = "http://www.hpl.hp.com/personal/Yasushi_Saito/pychart",
       license = "GPL",
       long_description = """
Pychart is a Python library for creating high-quality
charts in Postscript, PDF, and PNG. 
It produces line plots, bar plots, range-fill plots, and pie
charts.""",
       packages = ['pychart', 'pychart.afm']
      )
