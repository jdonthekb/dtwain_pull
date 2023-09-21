import datetime

# Define your conditions
USE_UNICODE = True
USE_64_BIT = False

# Conditional imports based on the conditions
if USE_UNICODE:
    if USE_64_BIT:
        from dtwain_x64_unicode import dtwain
        dtwain_dll = "./dtwain_x64_unicode/dtwain64u.dll"
    else:
        from dtwain_x86_unicode import dtwain
        dtwain_dll = "./dtwain_x86_unicode/dtwain86u.dll"
else:
    if USE_64_BIT:
        from dtwain_x64 import dtwain
        dtwain_dll = "./dtwain_x64/dtwain64.dll"
    else:
        from dtwain_x86 import dtwain
        dtwain_dll = "./dtwain_x86/dtwain64.dll"

# Now, you can use the dtwain module in your code, and it will refer to the correct version
# dtwain.some_function()

def get_formatted_datetime():
    now = datetime.datetime.now()
    formatted_date = now.strftime("%m%d%Y-%H%M%S-")
    return formatted_date

def generate_filename(app):
    name = app.Entry2.get() # get our name from the input field
    print("Name: " + name) # display to console
    current_time = get_formatted_datetime() # get current time | to stamp filename
    file_name = current_time + name + ".jpg"
    print("Filename: " + file_name)
    return file_name

# This function will be responsible for acquiring the image from the twain device
def acquire_image(app):
    print("Attempting to Acquire the image...")
    pass

