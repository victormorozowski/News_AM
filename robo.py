from datetime import datetime, timedelta
import json
from gnews import GNews

# Inicializa o buscador do Google News (focado no Brasil e em Português)
google_news = GNews(language='pt', country='BR', period='1d', max_results=5)

# Lista oficial com os 19 parâmetros solicitados
TEMAS_BUSCA = [
    "Superintendência da Polícia Federal no Amazonas",
    "Superintendente da Polícia Federal no Amazonas",
    "Delegada de Polícia Federal Danielle de Meneses Oliveira Mady",
    "Tráfico de drogas no Amazonas",
    "Apreensão de drogas no Amazonas",
    "Segurança Pública no Amazonas",
    "Desmatamento no Amazonas",
    "Queimadas no Amazonas",
    "Garimpo ilegal no Amazonas",
    "Extração de ouro no Amazonas",
    "Prisão no Amazonas",
    "Pirataria fluvial Amazonas",
    "Política no Amazonas fatos relevantes",
    "Polícia Civil do Amazonas",
    "Polícia Militar do Amazonas",
    "Polícia Federal do Amazonas",
    "Operações da Polícia Federal Amazonas",
    "Órgãos Federais atuantes no Amazonas",
]

def buscar_noticias():
  relatorio_geral = {}
  data_execucao = datetime.now().strftime('%d/%m/%Y %H:%M')

  print(f'Iniciando varredura de notícias - {data_execucao}\n' + '=' * 50)

  for tema in TEMAS_BUSCA:
    print(f'Pesquisando: {tema}...')
    try:
      artigos = google_news.get_news(tema)
      noticias_filtradas = []

      if artigos:
        for artigo in artigos:
          titulo = artigo.get('title', 'Sem Título')
          fonte = artigo.get('publisher', {}).get('title', 'Fonte Desconhecida')
          link = artigo.get('url', '#')
          data_pub = artigo.get('published date', 'Data não informada')
          descricao = artigo.get('description', '')
          resumo = descricao if descricao else f'Notícia referente a {tema}.'

          noticias_filtradas.append({
              'titulo': titulo,
              'resumo': resumo,
              'data': data_pub,
              'fonte': fonte,
              'link': link,
          })

      if not noticias_filtradas:
        relatorio_geral[tema] = 'Sem atualizações relevantes nas últimas 24h.'
      else:
        relatorio_geral[tema] = noticias_filtradas

    except Exception as e:
      print(f'Erro ao buscar o tema "{tema}": {e}')
      relatorio_geral[tema] = 'Sem atualizações relevantes nas últimas 24h.'

  with open('noticias_atualizadas.json', 'w', encoding='utf-8') as f:
    json.dump(relatorio_geral, f, ensure_ascii=False, indent=4)

  print('\nVarredura concluída! Dados salvos em notícias_atualizadas.json.')

if __name__ == '__main__':
  buscar_noticias()
