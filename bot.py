from openai import OpenAI
import os

# Ayarlar
HF_TOKEN = "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"
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

def makale_olustur(soru):
    print(f"Yazılıyor: {soru}...")
    
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": f"Write a professional SEO technical guide about '{soru}' in English. Use Markdown headers (##, ###) and a comparison table. Do not include any intro like 'Here is your article', just start with the content."
                }
            ],
            max_tokens=1500
        )

        text = completion.choices[0].message.content

        # Dosyayı oluştur (src/pages klasörüne)
        slug = soru.lower().replace(' ', '-').replace('?', '')
        dosya_adi = f"src/pages/{slug}.md"

        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.write(f"---\nlayout: ../layouts/MainLayout.astro\ntitle: '{soru}'\ndescription: 'Technical guide and review of {soru}.'\n---\n")
            f.write(text)
        
        print(f"Başarıyla oluşturuldu: {dosya_adi}")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# TEST
makale_olustur("What is Mythos AI")