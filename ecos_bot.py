import os
import django
import requests
from django.core.files.base import ContentFile
from newsapi import NewsApiClient

# 1. SETUP
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from blog.models import Noticia

# 2. CHAVE
api_key = 'bb1fde67f93e4eed954d13c4df4c501b' # <--- COLOCAR SUA CHAVE NOVAMENTE
ecos = NewsApiClient(api_key=api_key)

print("🦅 Ecos: Iniciando curadoria com limpeza de texto...")

missoes = [
    {'tema': 'Inteligência Artificial', 'categoria': 'Tecnologia'},
    {'tema': 'Mercado Financeiro',      'categoria': 'Finanças'},
    {'tema': 'Saúde Mental',            'categoria': 'Saúde'},
    {'tema': 'Cultura Pop',             'categoria': 'Geral'}
]

for missao in missoes:
    tema = missao['tema']
    cat = missao['categoria']
    
    print(f"🔎 Buscando: {tema}...")

    dados = ecos.get_everything(
        q=tema,
        language='pt',
        sort_by='publishedAt',
        page_size=2
    )

    if dados['status'] == 'ok':
        for artigo in dados['articles']:
            titulo = artigo['title']
            
            if not titulo or Noticia.objects.filter(titulo=titulo).exists():
                continue

            # === CORREÇÃO 1: Subtítulo Inteligente ===
            # Tenta pegar a descrição. Se não tiver, usa o título.
            texto_desc = artigo['description'] or titulo
            # Corta em 195 caracteres
            sub_limpo = texto_desc[:195]
            # Se cortou no meio, volta até o último espaço e põe "..."
            if len(texto_desc) > 195:
                sub_limpo = sub_limpo.rsplit(' ', 1)[0] + "..."

            # === CORREÇÃO 2: Limpar o [+chars] do Conteúdo ===
            conteudo_cru = artigo['content'] or sub_limpo
            # Remove a parte feia do [+1234 chars]
            if '[+' in conteudo_cru:
                conteudo_cru = conteudo_cru.split('[+')[0] + "..."

            autor = artigo['source']['name'] or "Redação"
            link = artigo['url']
            img_url = artigo['urlToImage']
            
            # Monta o HTML final limpo
            conteudo_final = f"""
            <p>{conteudo_cru}</p>
            <br>
            <p><strong>Fonte:</strong> {autor}</p>
            <div style="margin-top: 15px;">
                <a href="{link}" target="_blank" style="background: #e63946; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; font-weight: bold;">
                    Ler matéria completa na íntegra &rarr;
                </a>
            </div>
            """

            nova_noticia = Noticia(
                titulo=titulo,
                subtitulo=sub_limpo, # Agora cortado bonitinho
                conteudo=conteudo_final,
                categoria=cat
            )

            if img_url:
                try:
                    resp = requests.get(img_url, timeout=10)
                    if resp.status_code == 200:
                        nome = f"img_{cat}_{titulo[:5].strip()}.jpg"
                        nova_noticia.imagem.save(nome, ContentFile(resp.content), save=False)
                except:
                    pass

            nova_noticia.save()
            print(f"   ✅ {titulo[:30]}...")

print("🦅 Ecos: Feito!")