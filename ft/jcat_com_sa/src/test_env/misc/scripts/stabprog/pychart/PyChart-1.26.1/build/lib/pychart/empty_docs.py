
def generate_doc(name, suffix="", append = 0):
    if append:
        fp = open(name + "_doc.py", "a+")
    else:
        fp = open(name + "_doc.py", "w")
        fp.write("# automatically generated by generate_docs.py.\n")
    fp.write("doc" + suffix + "=\" \"\n")
    fp.close()
    
generate_doc( "area")
generate_doc( "arrow")
generate_doc( "axis", "_x")
generate_doc( "axis", "_y", 1)
generate_doc( "bar_plot")
generate_doc( "color")
generate_doc( "error_bar","_1")
generate_doc( "error_bar", "_2", 1)
generate_doc( "error_bar", "_3", 1)
generate_doc( "error_bar", "_4", 1)
generate_doc( "error_bar", "_5", 1)
generate_doc( "fill_style")
generate_doc("line_plot")
generate_doc("pie_plot")
generate_doc("text_box")
generate_doc("range_plot")
generate_doc("legend")
generate_doc("legend", "_entry", 1)
generate_doc("line_style")
generate_doc("tick_mark")
