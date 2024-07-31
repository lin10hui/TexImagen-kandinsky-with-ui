from T2I import t2i
from init import model
import time
time_start = time.time()  # 记录开始时间
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

def mix(text1,text2):
    image_mixed = model.mix_images(
        [t2i(text1), t2i(text2)], [0.5, 0.5],
        num_steps=20,
        batch_size=1,
        guidance_scale=4,
        h=768,
        w=768,
        sampler='p_sampler',
        prior_cf_scale=4,
        prior_steps="5",
    )
    return image_mixed[0]

def save_mix(text1,text2,path):
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    name=text1+'  with  '+text2+'+'+str(round(time_sum))+'.png'
    mix(text1,text2).save(os.path.join(path,name))





if __name__ == '__main__':
    save_mix('sad man','lion','/home/whm/lhl/open/Kandinsky-2-main/new/mix')
