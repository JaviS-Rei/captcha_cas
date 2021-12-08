'''
    input:   original captcha image in CAS 
    output:  answer in type string
    usage:   
        from captcha_recognizer_cas import captha_recognize
        res = captcha_recognize(path)
    
    performance: 1500 captchas per sec
    
    Note:
        1. this program can only recognize captcha image in CAS.
        2. performance optimizing causes little UNREADABLE code.
    
'''

from PIL import Image
import numpy as np
from pathlib import Path

x0_list = [6, 19, 32, 45]
x1_list = [16, 29, 42, 55]
threshold = 125

# set label path
label_dir = r".\label\%d.jpg"
label_set = []
for i in range(10):
    label_set.append((np.array(Image.open(label_dir % i).convert('L'))) < threshold)

def char_cmp(img, label):
    diff = []
    for i in range(10):
        diff.append(np.sum(img ^ label[i]))
    return diff.index(min(diff))

def captcha_recognize(path):
    img = np.array(Image.open(path).convert('L')) < threshold
    res = ""
    for i in range(4):
        x0_ = x0_list[i]
        x1_ = x1_list[i]
        res += str(char_cmp(img[:,x0_:x1_], label_set))
    return res

def performance_test(testdir):
    res = []
    for file in Path(testdir).iterdir():
        res.append(captcha_recognize(file))
        
if __name__ == "__main__":
    performance_test(r"./two_value_125")