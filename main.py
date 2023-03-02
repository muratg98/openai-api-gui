import datetime as dt
import openai
import os
import tkinter
from tkinter import messagebox


def Error_Handler(func):
    def Inner_Function(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            return resp
        except openai.error.APIError as e:
            tkinter.messagebox.showerror(title="Error", message=f"OpenAI API returned an API Error: {e}")
            return 1
        except openai.error.APIConnectionError as e:
            tkinter.messagebox.showerror(title="Error", message=f"Failed to connect to OpenAI API: {e}")
            return 1
        except openai.error.RateLimitError as e:
            tkinter.messagebox.showerror(title="Error", message=f"OpenAI API request exceeded rate limit: {e}")
            return 1
        except openai.error.InvalidRequestError as e:
            tkinter.messagebox.showerror(title="Error", message=f"OpenAI API request invalid error: {e}")
            return 1
        except openai.error.AuthenticationError as e:
            tkinter.messagebox.showerror(title="Error", message=f"OpenAI API key or token was invalid, expired, or revoked.\nError Displayed: {e}")
            return 1
        except openai.error.InvalidAPIType as e:
            tkinter.messagebox.showerror(title="Error", message=f"OpenAI API request error: {e}")
            return 1
        except openai.error.PermissionError as e:
            tkinter.messagebox.showerror(title="Error", message=f"OpenAI API request Permission Error: {e}")
            return 1
        except openai.error.ServiceUnavailableError as e:
            tkinter.messagebox.showerror(title="Error", message=f"There is currently an issue with our servers.\n Error: {e}")
            return 1
        except openai.error.SignatureVerificationError as e:
            tkinter.messagebox.showerror(title="Error", message=f"OpenAI API request error with signature verification: {e}")
            return 1
        except openai.error.Timeout as e:
            tkinter.messagebox.showerror(title="Error", message=f"OpenAI API request took too long to create.\n Error: {e}")
            return 1
        except openai.error.TryAgain as e:
            tkinter.messagebox.showerror(title="Error", message=f"OpenAI API request error.\n Error: {e}")
            return 1
    return Inner_Function


@Error_Handler
def upload_files(file_loco, api_key):
    openai.api_key = api_key
    response = openai.File.create(file=open(file_loco, "rb"), purpose='fine-tune')
    return response['id']


@Error_Handler
def get_my_files(api_key):
    openai.api_key = api_key
    response = openai.File.list()
    data = response['data']
    f_names = []
    f_ids = []
    f_dates = []
    for info in data:
        ts = dt.datetime.fromtimestamp(info['created_at']).strftime('%Y-%m-%d %H:%M:%S')
        f_names.append(info['filename'])
        f_ids.append(info['id'])
        f_dates.append(ts)
    return [f_names, f_ids, f_dates]


@Error_Handler
def delete_file(file_id, api_key):
    openai.api_key = api_key
    response = openai.File.delete(file_id)
    return response


@Error_Handler
def create_fine_tune(t_file, v_file, name, model, api_key, **kwargs):
    openai.api_key = api_key
    response = openai.FineTune.create(training_file=t_file, validation_file=v_file, suffix=name, model=model, **kwargs)
    return response


@Error_Handler
def list_fine_tune_events(fine_tune_id, api_key):
    openai.api_key = api_key
    response = openai.FineTune.list_events(id=fine_tune_id)
    return response


@Error_Handler
def get_list_of_fine_tunes(api_key):
    openai.api_key = api_key
    response = openai.FineTune.list()
    data = response['data']
    model_id = []
    model_name = []
    model_status = []
    for model in data:
        model_id.append(model['id'])
        if model['fine_tuned_model'] is None:
            model_name.append('Model Name In Process of Creation')
            model_status.append(model['status'])
            continue
        model_name.append(model['fine_tuned_model'])
        model_status.append(model['status'])
    return [model_name, model_id, model_status]


@Error_Handler
def get_list_of_models(api_key):
    openai.api_key = api_key
    response = openai.Model.list()
    return response


@Error_Handler
def get_list_of_available_ft(api_key):
    all_models = get_list_of_models(api_key)
    data = all_models['data']
    available_ft = ["davinci", "curie", "babbage", "ada"]
    for i in data:
        if i['permission'][0]['allow_fine_tuning'] is True and "ft" in i['id']:
            available_ft.append(i['id'])
    return available_ft


@Error_Handler
def delete_fine_tuned_model(model_name):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.Model.delete(model_name)


@Error_Handler
def delete_all_models(list_of_model_names):
    for name in list_of_model_names:
        delete_fine_tuned_model(name)
