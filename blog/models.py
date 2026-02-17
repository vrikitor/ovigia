from django.db import models

class Noticia(models.Model):
    CATEGORIAS = [
        ('SAUDE', 'Saúde'),
        ('FINANCAS', 'Finanças'),
        ('RECEITAS', 'Receitas'),
        ('MUNDO', 'Mundo'),
        ('GERAL', 'Geral'),
    ]

    titulo = models.CharField(max_length=200)
    
    # NOVO CAMPO: Subtítulo (Texto de apoio que fica abaixo do título)
    subtitulo = models.CharField(max_length=300, blank=True, null=True, help_text="Opcional: Uma frase curta que complementa o título")
    
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='GERAL')
    conteudo = models.TextField()
    
    imagem = models.ImageField(upload_to='noticias/', blank=True, null=True)
    
    # NOVO CAMPO: Legenda da Imagem (Créditos ou descrição)
    legenda_imagem = models.CharField(max_length=150, blank=True, null=True, help_text="Opcional: Créditos da foto ou descrição curta")
    
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo