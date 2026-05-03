from openai import OpenAI
import os

HF_TOKEN = "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"
client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=HF_TOKEN)

def makale_olustur(soru):
    print(f"Sıradaki: {soru}...")
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages=[{"role": "user", "content": f"Write a long, professional SEO technical guide about '{soru}' in English. Use Markdown headers and a comparison table. No intro."}],
            max_tokens=1500
        )
        text = completion.choices[0].message.content
        slug = soru.lower().replace(' ', '-').replace('?', '').strip()
        
        with open(f"src/pages/{slug}.md", "w", encoding="utf-8") as f:
            f.write(f"---\nlayout: ../layouts/MainLayout.astro\ntitle: '{soru}'\ndescription: 'Guide about {soru}.'\n---\n")
            f.write(text)
        print(f"Başarılı: {slug}")
    except Exception as e:
        print(f"Hata: {e}")

# KEYWORDS.TXT DOSYASINI OKU VE HEPSİNİ YAZ
if __name__ == "__main__":
    if os.path.exists("keywords.txt"):
        with open("keywords.txt", "r", encoding="utf-8") as f:
            liste = f.read().splitlines()
        
        for satir in liste:
            if satir.strip():
                makale_olustur(satir.strip())
    else:
        print("Lütfen keywords.txt dosyasını oluşturun!")