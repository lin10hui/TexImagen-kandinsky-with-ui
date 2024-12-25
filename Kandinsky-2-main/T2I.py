import time
time_start = time.time()  # 记录开始时间
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from init import model

def t2i(text):
    images = model.generate_text2img(
        text,
        num_steps=20,
        batch_size=1,
        guidance_scale=4,
        h=768,
        w=768,
        sampler='p_sampler',
        prior_cf_scale=4,
        prior_steps="5"
    )
    return images[0]


def save_t2i(text,path):
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    name=text+'+'+str(round(time_sum))+'.png'
    t2i(text).save(os.path.join(path,name))


if __name__ == '__main__':
    # display(images[0])
    save_t2i('laugh man','/home/whm/lhl/open/Kandinsky-2-main/new/t2i')




