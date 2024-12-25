from init import models
import time
time_start = time.time()  # 记录开始时间
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from PIL import Image
import numpy as np

def inpainting(path,text):
    init_image = Image.open(path)
    mask = np.ones((768, 768), dtype=np.float32)
    mask[:, :550] = 0
    images = models.generate_inpainting(
        text,
        init_image,
        mask,
        num_steps=150,
        batch_size=1,
        guidance_scale=5,
        h=768, w=768,
        sampler='p_sampler',
        prior_cf_scale=4,
        prior_steps="5"
    )
    return images[0]

def save_inpainting(text,repath,topath):
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    name=text+'_recover_'+str(round(time_sum))+'.png'
    inpainting(repath,text).save(os.path.join(topath,name))


if __name__ == '__main__':
    save_inpainting('证件照','./re.jpg','/home/whm/lhl/open/Kandinsky-2-main/new/rec')

