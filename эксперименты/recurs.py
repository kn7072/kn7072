# -*- coding: utf-8 -*-
dict_ = {
    'q': {
          'r' :{'y' :5, 'z' :8 }, 't' :{'u' :7, 'b' :{'v':55}}
         },
    'w': {'i' : 6},
    'e': {'o' : 3}
  }
x = ''
dict_out = {}
dict_out_ = {}
def extract_(dict_in, dict_out, key_p = ''):
    for key, value in dict_in.items():
        if key_p == '':
            key_ = key
        else:
            key_ = key_p +"."+ key
        if isinstance(value, dict):
            global x
            dict_out, x = extract_(value, dict_out, key_)
        if key_ in x:  continue
        dict_out[key_p] = value
        print (key_p)
    return dict_out, key_p
# # # #  # # # # # # #  # # # #  # # # #  # # # #  # # # #  # # # # # # # # #  # # # #

def extract(dict_in, dict_out, key_p = ''):
    for key, value in dict_in.items():
        if isinstance(value, dict):
            if key_p == '':
                key_ = key
            else:
                key_ = key_p +"."+ key
            global x
            dict_out, x = extract(value, dict_out, key_)
        if key_p == '':
            key_x = key
        else:
            key_x = key_p +"."+ key
        if key_x in x:  continue
        dict_out[key_x] = value
        print (key_x)
    return dict_out, key_x
# # #  # # # # # # # #  # # #  # # #  # # # #  # # # # # #  # # # # #  # # # # # #

def extract_sergei(dict_in, dict_out):
    for key, value in dict_in.items():
        if isinstance(value, dict):
            extract_sergei(value, dict_out)
        dict_out[key] = value
    return dict_out



extract_(dict_, dict_out_)
pass