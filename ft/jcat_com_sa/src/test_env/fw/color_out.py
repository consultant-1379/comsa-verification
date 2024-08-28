import java.io.PrintStream as PrintStream
import java.lang.Appendable as Appendable
import java.io.Closeable as Closeable
import java.lang.System as System
import java.lang.Thread as Thread
import traceback
import array
import sys
import re


##########################
#                        #
# written by Daniel Oman  #
# eomadan(at)ericsson.se #
#                        #
##########################


class color_out(PrintStream, Closeable, Appendable):
    """
            
    """
    #more info http://www.gilesorr.com/bashprompt/howto/c333.html
    reset = "\033[0m"
    
    #foreground
    fg_black = "\033[30m"
    fg_red = "\033[31m"
    fg_green = "\033[32m"
    fg_yellow = "\033[33m"
    fg_blue = "\033[34m"
    fg_magenta = "\033[35m"
    fg_cyan = "\033[36m"
    fg_white = "\033[37m"    
    
    #background
    bg_black = "\033[40m"
    bg_red = "\033[41m"
    bg_green = "\033[42m"
    bg_yellow = "\033[43m"
    bg_blue = "\033[44m"
    bg_magenta = "\033[45m"
    bg_cyan = "\033[46m"
    bg_white = "\033[47m"
    
    #other
    other_bold_on = "\033[1m"#not correct
    other_revers_on = "\033[2m"#not tested
    other_italics_on = "\033[3m"#not tested
    other_underline_on = "\033[4m"
    other_blink_on = "\033[5m"#not tested
    other_reverse_on = "\033[7m"#not tested
    other_concealed_on = "\033[8m"#not tested
    
    
    #Create a printout stream instance to replace Java and Python output.
    def __init__(self, filter=None,
                 default_color=reset,
                 replace=None):  
        
        if(filter == None):
            c_file = traceback.extract_stack()[-2][0].split("/")[-1]
            c_funk = traceback.extract_stack()[-2][2]
            filter = [(c_file, c_funk, """self\.logger\.""", color_out.fg_green)]
        if(replace == None):
            replace = System.out
        
        PrintStream.__init__(self, replace)
        
        self._filter = filter
        self._default_color = default_color
        self._replace = replace
        
        self._restPrintOut = "" #This one is used to preserve the background color.
    
    
    #Filter out the text from a Java or Python printout before sending to _write.
    def write(self, *arg):
        
        #We don't want the test case to fail because of a faulty printout.
        try:
            #a Python printout
            if(len(arg) == 1):
                self._write(arg[0])
            
            #a Java printout
            if(len(arg) == 3):
                byte_aray = arg[0]
                start = arg[1]
                stop = arg[2]
                
                #recover the string
                byte_aray = byte_aray[start:stop]
                text = byte_aray.tostring()     
                
                self._write(text)
        except:
            ############
            # Something has gone really badly. Let's try to save what we can.
            ############
            
            #Try to set the default color.
            try:
                 self._replace.write(self._default_color)
            except:
                pass
            
            #Try to print the text.
            try:
                 self._replace.write(*arg)
            except:
                pass
             
    #adds a color tag before writing
    def _write(self, str): 
        
        #Get what color it should be.
        color = self._get_color_code()
        
        #Tag all text after this with the right color tag.
        self._replace.write(color)
        
        #Replace HTML tags with normal text.
        str = self._html2Text(str, color)
               
        ##This code is to preserve the background color.
        #Print the last new line.... This is to prevent coloring from the background on this row.
        self._replace.write(self._restPrintOut)
        
        self._restPrintOut = ""
        if(str.endswith("\n")):
            str = str[:-len("\n")]#It might be longer than 1 char in some architectures.
            self._restPrintOut = "\n"
        ##This code is to preserve the background color.
        
        #Print the actual message.
        self._replace.write(str)
        
        #Go back to the default color tag.
        self._replace.write(self._default_color)
        
        
        
        #Then perform a flush just in case.
        self._replace.flush()
    
    #Look through the filter and get the appropriate color for the caller.
    def _get_color_code(self):
        p_stack = traceback.extract_stack()       
        j_stack = Thread.currentThread().getStackTrace();
        
        
        #####################
        # Go through the filter.
        #####################
        for (file, func, command, color) in self._filter:

            #####################
            # Go through the Python p_stack.
            #####################
            for (c_file, _, c_func, c_command) in p_stack :
                if(c_file == None):
                    c_file = "None"
                if(c_func == None):
                    c_func = "None"
                if(c_command == None):
                    c_command = "None"
                    
                c_file = c_file.split("/")[-1]
                 
                
                #Compare with the filter.
                if(re.match(file, c_file)):
                    if(re.match(func, c_func)):
                        if(re.match(command, c_command)):               
                            return color
                            
            
            #We only go through the java stack if the command line can be anything.
            if(command == "."):
                
                #####################
                # Go through the java stack.
                #####################
                for i in j_stack:
                    c_file = i.getFileName()
                    c_func = i.getMethodName()
                    
                    if (c_func == None):
                        c_func = "None"                
                    if (c_file == None):
                        c_file = "None"
                        
                    #Fix the filename to be a filename and not a file path.
                    c_file = c_file.split("/")[-1]           
                    
                    #Compare with the filter.
                    if(re.match(file, c_file)):
                        if(re.match(func, c_func)):
                           return color
        
        #If it doesn't match any filter entry we return the default color.
        return self._default_color
    
    def _html2Text(self, text, color):
            
        ##known problems 
        #
        # Having nested tags will not work in this version.
        # <b> This should be bold, and will be. <i> This should be italics and bold, and will be. </i> This should be bold.... but it wont be.</b>
        #     
        
        ###########                     
        # fixes line breaks
        ###########
        regexNL = "<\s*br\s*/?\s*>"
        text = re.sub(regexNL, "\n", text)
        
        ###########                     
        # fixes bold
        ###########
        regexBoldStart = "<\s*b\s*>"
        regexBoldEnd = "<\s*/\s*b\s*>"
        text = re.sub(regexBoldStart, color_out.other_bold_on, text)
        text = re.sub(regexBoldEnd, color_out.reset + color, text)
        
        ###########                     
        # fixes italics
        ###########
        regexItalicsStart = "<\s*i\s*>"
        regexItalicsEnd = "<\s*/\s*i\s*>"
        text = re.sub(regexItalicsStart, color_out.other_italics_on, text)
        text = re.sub(regexItalicsEnd, color_out.reset + color, text)
        
        ###########                     
        # fixes underline
        ###########
        regexUnderlineStart = "<\s*u\s*>"
        regexUnderlineEnd = "<\s*/\s*u\s*>"
        text = re.sub(regexItalicsStart, color_out.other_underline_on, text)
        text = re.sub(regexItalicsEnd, color_out.reset + color, text)
        
        ##########
        # fixes spaces
        ##########
        text = text.replace("&#160", " ")
             
        return text
    
    
def tag_prints(filter=None,
               default_color=color_out.reset,
               replace=None): 

    #By default create a default filter.
    if(filter == None):
                
        filter = []#Create an empty filter to append rules to.
        
        ###########                     
        # test step, cyan with green background
        ###########
        #filter.append((".", ".", """\s*self\.setTestStep\(.*\)""", color_out.fg_magenta + color_out.bg_green))
        
        
        ###########                     
        # FATAL red, underlined
        ###########
        filter.append(("Category.java", "fatal", "." , color_out.fg_red + color_out.other_bold_on))        
        
        ###########                     
        # ERROR red
        ###########
        filter.append(("Category.java", "error", "." , color_out.fg_red))
               
        ###########                     
        # WARNING yellow
        ###########
        filter.append(("Category.java", "warn", "." , color_out.fg_yellow))
        
        ###########                     
        # INFO green
        ###########
        filter.append(("Category.java", "info", "." , color_out.fg_green))
        
        ###########                     
        # DEBUG cyan
        ###########
        filter.append(("Category.java", "debug", ".", color_out.fg_cyan))
               
        
    #By default replace Java's standard output stream.
    if(replace == None):
        replace = System.out
        #Remove any previous color_out.
        while color_out().__class__ == replace.__class__:
            replace = replace._replace
    
    new_out = color_out(filter, default_color, replace) 
    System.setOut(new_out)#Change the Java output stream.
    sys.stdout = new_out#Change the Python output stream.
