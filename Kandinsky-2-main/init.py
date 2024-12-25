import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


from kandinsky2 import get_kandinsky2

model = get_kandinsky2(
    'cuda',
    task_type='text2img',
    cache_dir='./download/kandinsky2',
    model_version='2.1',
    use_flash_attention=False
)

models = get_kandinsky2(
    'cuda',
    task_type='inpainting',
    model_version='2.1',
    use_flash_attention=False
)






