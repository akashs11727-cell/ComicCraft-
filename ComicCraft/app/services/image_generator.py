from pathlib import Path
from PIL import Image,ImageDraw
from app.config import get_settings
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'static'/'panels'; OUT.mkdir(parents=True,exist_ok=True)
def generate_image(prompt,panel_number):
    s=get_settings(); path=OUT/f'panel_{panel_number}.png'; provider=s.image_provider.lower()
    if s.demo_mode or provider=='demo':
        im=Image.new('RGB',(1024,640),'white'); d=ImageDraw.Draw(im); d.rectangle((20,20,1004,620),outline='black',width=6); d.text((50,70),'COMICCRAFT',fill='black'); d.text((50,160),prompt[:180],fill='black'); d.text((50,540),'Demo image - enable Hugging Face or Diffusers for AI art.',fill='black'); im.save(path); return f'/static/panels/panel_{panel_number}.png'
    if provider=='huggingface':
        from huggingface_hub import InferenceClient
        if not s.hf_api_key: raise RuntimeError('HF_API_KEY is required')
        img=InferenceClient(provider='hf-inference',api_key=s.hf_api_key).text_to_image(prompt,model=s.image_model); img.save(path); return f'/static/panels/panel_{panel_number}.png'
    if provider=='diffusers':
        import torch
        from diffusers import StableDiffusionPipeline
        dev='cuda' if torch.cuda.is_available() else 'cpu'; dtype=torch.float16 if dev=='cuda' else torch.float32
        pipe=StableDiffusionPipeline.from_pretrained(s.image_model,torch_dtype=dtype).to(dev); pipe(prompt,num_inference_steps=20).images[0].save(path); return f'/static/panels/panel_{panel_number}.png'
    raise ValueError('Unsupported IMAGE_PROVIDER')
