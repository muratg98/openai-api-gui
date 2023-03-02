import tkinter.filedialog
from tkinter import *
import main
from tkinter import messagebox


window = Tk()
window.config(padx=5, pady=5)
window.title("OpenAI Fine-Tuned Model Creator")


# API_KEY Label
api_key_label = Label(window, text="API Key: ", font=("Arial", "11"))
api_key_label.grid(column=0, row=0, padx=5, pady=5)

# API_KEY USER ENTRY
api_key_entry = Entry(window, width=25, show='*')
api_key_entry.grid(column=1, row=0, padx=5, pady=5, sticky='w')


def show_api():
    if api_key_entry.cget('show') == '*':
        api_key_entry.config(show='')
    else:
        api_key_entry.config(show='*')


# API_KEY Check Click
api_key_check_button = Checkbutton(window, text="show key", command=show_api)
api_key_check_button.grid(column=2, row=0, padx=5, pady=5, sticky='w')

# Training/Validating File Menu
variable = StringVar(window)
variable.set("Train File")
training_file_menu = OptionMenu(window, variable, "Valid File", "Train File")
training_file_menu.grid(column=0, row=1, padx=5, pady=5)


def check_for_api():
    api_key = api_key_entry.get()
    if api_key == '' or api_key is None:
        tkinter.messagebox.showerror(title="No API", message="Please Make Sure To Include A Valid Api Key")
        return True


def open_my_files_window():
    if check_for_api():
        return
    my_filesWindow = Toplevel(window, pady=5, padx=5, width=100, height=100)
    my_filesWindow.title("My Files")
    # File ID Label
    file_id_label = Label(my_filesWindow, text="File ID", font=("Arial", "11"))
    file_id_label.grid(column=0, row=0, padx=10)
    # Creation Datetime Label
    creation_date_label = Label(my_filesWindow, text="Creation\nDatetime", font=("Arial", "11"))
    creation_date_label.grid(column=1, row=0)
    # Get List Of Files Uploaded
    api_key = api_key_entry.get()
    response = main.get_my_files(api_key)
    if response == 1:
        return
    file_ids = response[1]
    height = len(file_ids)
    file_ids_str = '\n'.join(file_ids)
    fids_text = Text(my_filesWindow, height=height, width=30)
    fids_text.insert(1.0, file_ids_str)
    fids_text.configure(bg=my_filesWindow.cget('bg'), relief="flat", state='disabled')
    fids_text.grid(column=0, row=1)
    file_dates = response[2]
    f_dates_str = '\n'.join(file_dates)
    f_dates_text = Text(my_filesWindow, height=height, width=20)
    f_dates_text.insert(1.0, f_dates_str)
    f_dates_text.configure(bg=my_filesWindow.cget('bg'), relief="flat", state='disabled')
    f_dates_text.grid(column=1, row=1)


# My Files Button
my_files = Button(window, text="My Files", command=open_my_files_window, width=15)
my_files.grid(column=2, row=1)


training_file_id_string = StringVar()
validation_file_id_string = StringVar()


def upload_file():
    if check_for_api():
        return
    file = tkinter.filedialog.askopenfilename(filetypes=[("JSONL files", '.jsonl'),
                                                         ('All types', '*.*')])
    if file:
        api_key = api_key_entry.get()
        file_loco = str(file)
        response = main.upload_files(file_loco, api_key)
        if response == 1:
            return
        if variable.get() == "Train File":
            training_file_id_string.set(response)
        elif variable.get() == "Valid File":
            validation_file_id_string.set(response)


# Upload File Button
upload_file_button = Button(window, text="Upload File", command=upload_file, width=20)
upload_file_button.grid(column=1, row=1, padx=5, pady=5, sticky='w')

# Training File Label Display
training_file_id = Label(window, text="Training File ID (necessary) ")
training_file_id.grid(column=0, row=2, sticky='e')

# Training File ID Uploaded Entry
training_file_id_entry = Entry(window, textvariable=training_file_id_string, width=25)
training_file_id_entry.grid(column=1, row=2, sticky='w')

# Validation File
validation_file_id = Label(window, text="Validation File ID (optional)")
validation_file_id.grid(column=0, row=3, sticky='e')

# Validation File ID Uploaded Label
validation_file_id_entry = Entry(window, textvariable=validation_file_id_string, width=25)
validation_file_id_entry.grid(column=1, row=3, sticky='w')

################
# Create Fine-Tuned Model Label
create_fine_tuned_model_label = Label(window, text="Create Fine-Tuned Model ", font=("Arial", "11"))
create_fine_tuned_model_label.grid(column=0, row=4, pady=15)

# Model Status
model_status_label = Label(window, text="No Model Detected", fg="red")
model_status_label.grid(column=2, row=4, sticky='w')


def custom_model_new_window():
    if check_for_api():
        return
    customWindow = Toplevel(window, pady=5, padx=5)
    customWindow.title("Customize Your Model")
    # Select Parameters Label
    parameters_label = Label(customWindow, text="Select Parameters", font=("Arial", "11"))
    parameters_label.grid(column=0, row=0, padx=5, pady=5)
    # Model Type Label
    model_type_label = Label(customWindow, text="Base Model ")
    model_type_label.grid(column=0, row=1)
    # Models Menu
    model_variable = StringVar(customWindow)
    model_variable.set("davinci")
    api_key = api_key_entry.get()
    available_models = main.get_list_of_available_ft(api_key)
    if available_models == 1:
        return
    models_menu = OptionMenu(customWindow, model_variable, *available_models)
    models_menu.grid(column=1, row=1)
    # Model Name Label
    model_name_label = Label(customWindow, text="Name: ")
    model_name_label.grid(column=0, row=2)
    # Model Name Entry
    model_name_entry = Entry(customWindow, width=15)
    model_name_entry.grid(column=1, row=2)
    # Optional Parameters Label
    optional_parameters_label = Label(customWindow, text="Optional Parameters", font=("Arial", "11"))
    optional_parameters_label.grid(column=0, row=3)
    # Values Name Label
    parameters_label = Label(customWindow, text="Values", font=("Arial", "11"))
    parameters_label.grid(column=1, row=3, padx=5, pady=5)
    # COMING SOON LABEL
    coming_soon_label = Label(customWindow, text="COMING SOON", font=("Arial", "20"))
    coming_soon_label.grid(column=0, row=4, columnspan=2)

    # Function to make model
    def make_fine_tuned_model():
        t_file_id = training_file_id_string.get()
        model_name = model_name_entry.get()
        chosen_model = model_variable.get()
        v_file_id = None
        if validation_file_id_entry.get() != '':
            v_file_id = validation_file_id_entry.get()
        response = main.create_fine_tune(t_file=t_file_id, v_file=v_file_id, name=model_name, model=chosen_model, api_key=api_key)
        if response == 1:
            return
        model_id = response['id']
        event_response = main.list_fine_tune_events(fine_tune_id=model_id, api_key=api_key)
        if event_response == 1:
            return
        response_message = event_response['data']
        for message in response_message:
            model_status_label.config(text=message['message'])

    # Create Model Button
    make_model_button = Button(customWindow, text="Create Fine-Tuned Model", width=30, command=make_fine_tuned_model)
    make_model_button.grid(row=11, column=0, columnspan=2)


# Customize Model Button
customize_model_button = Button(window, text="Customize Model", command=custom_model_new_window, width=20)
customize_model_button.grid(column=1, row=4, sticky='w')


def show_my_models():
    if check_for_api():
        return
    show_models_window = Toplevel(window, pady=5, padx=5, width=100, height=100)
    show_models_window.title("My Models")
    # Model Name Label
    model_name_label = Label(show_models_window, text="Model Name", font=("Arial", "11"))
    model_name_label.grid(column=0, row=0, padx=10)
    # Model ID Label
    model_id_label = Label(show_models_window, text="Model ID", font=("Arial", "11"))
    model_id_label.grid(column=1, row=0, padx=10)
    # Model Status
    status_label = Label(show_models_window, text="Status", font=("Arial", "11"))
    status_label.grid(column=2, row=0, padx=10)
    # Get model data
    api_key = api_key_entry.get()
    response = main.get_list_of_fine_tunes(api_key)
    if response == 1:
        return
    model_names = response[0]
    model_ids = response[1]
    model_status = response[2]
    height = len(model_names)
    model_names_str = '\n'.join(model_names)
    model_names_text = Text(show_models_window, height=height, width=60)
    model_names_text.insert(1.0, model_names_str)
    model_names_text.configure(bg=show_models_window.cget('bg'), relief="flat", state='disabled')
    model_names_text.grid(column=0, row=1)
    model_ids_str = '\n'.join(model_ids)
    model_ids_text = Text(show_models_window, height=height, width=30)
    model_ids_text.insert(1.0, model_ids_str)
    model_ids_text.configure(bg=show_models_window.cget('bg'), relief="flat", state='disabled')
    model_ids_text.grid(column=1, row=1)
    model_status_str = '\n'.join(model_status)
    model_status_text = Text(show_models_window, height=height, width=10)
    model_status_text.insert(1.0, model_status_str)
    model_status_text.configure(bg=show_models_window.cget('bg'), relief="flat", state='disabled')
    model_status_text.grid(column=2, row=1)


# My Fine-Tuned Models
my_models_button = Button(window, text="My Fine-Tuned\nModels", command=show_my_models)
my_models_button.grid(column=0, row=5)


def delete_file_cmd():
    if check_for_api():
        return
    delete_file_window = Toplevel(window, pady=5, padx=5, width=100, height=100)
    delete_file_window.title("Delete File")
    delete_file_label = Label(delete_file_window, text="Delete A File", font=("Arial", "11"))
    delete_file_label.grid(column=0, row=0, padx=10, columnspan=3)
    # Enter File ID Label
    enter_file_id_label = Label(delete_file_window, text="Enter File ID ")
    enter_file_id_label.grid(column=0, row=1, padx=10)
    # Entry Box For File ID
    file_id_entry = Entry(delete_file_window, width=40)
    file_id_entry.grid(column=1, row=1, columnspan=2, padx=5, pady=10)
    # Confirm Del Label
    confirm_del = StringVar()
    confirm_del_label = Label(delete_file_window, textvariable=confirm_del, fg='red')
    confirm_del_label.grid(column=2, row=2)

    # Script to execute deletion
    def file_deletion():
        file_id = file_id_entry.get()
        if file_id == '' or file_id is None:
            tkinter.messagebox.showerror(title="No File ID", message="Please Enter The File ID For Deletion")
        api_key = api_key_entry.get()
        delete_file = main.delete_file(file_id, api_key)
        if delete_file == 1:
            return
        if delete_file['deleted']:
            confirm_del.set("File Deleted")
    # Button To Execute Deletion
    del_file_button = Button(delete_file_window, text="Delete", width=15, command=file_deletion)
    del_file_button.grid(column=1, row=2)


# Delete File Button Popup
delete_file_button = Button(window, text="Delete File", width=15, command=delete_file_cmd)
delete_file_button.grid(column=2, row=2)


# Delete FineTuned Model
def delete_ft_model():
    if check_for_api():
        return
    delete_ft_window = Toplevel(window, pady=5, padx=5, width=100, height=100)
    delete_ft_window.title("Delete FT Model")
    delete_ft_label = Label(delete_ft_window, text="Delete A FT Model", font=("Arial", "11"))
    delete_ft_label.grid(column=0, row=0, padx=10, columnspan=3)
    # Enter FT Model Name Label
    enter_ft_name_label = Label(delete_ft_window, text="Enter FT Model Name ")
    enter_ft_name_label.grid(column=0, row=1, padx=10)
    # Entry Box For File ID
    ft_name_entry = Entry(delete_ft_window, width=40)
    ft_name_entry.grid(column=1, row=1, columnspan=2, padx=5, pady=10)
    # Confirm Del Label
    confirm_del = StringVar()
    confirm_del_label = Label(delete_ft_window, textvariable=confirm_del, fg='red')
    confirm_del_label.grid(column=2, row=2)

    def ft_deletion():
        ft_name = ft_name_entry.get()
        api_key = api_key_entry.get()
        delete_file = main.delete_file(ft_name, api_key)
        if delete_file == 1:
            return
        if delete_file['deleted']:
            confirm_del.set("File Deleted")
    # Button To Execute Deletion
    del_file_button = Button(delete_ft_window, text="Delete", width=15, command=ft_deletion)
    del_file_button.grid(column=1, row=2)


delete_ft = Button(window, text="Delete a\nFT Model", width=15, command=delete_ft_model)
delete_ft.grid(column=1, row=5)

window.mainloop()
