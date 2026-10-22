from datetime import datetime
import json
import os
from gnews import GNews

# Inicializa o buscador do Google News (focado no Brasil e em Português)
google_news = GNews(language='pt', country='BR', period='1d', max_results=8)

# Lista oficial com os 18 parâmetros solicitados
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
  data_hoje = datetime.now().strftime('%Y-%m-%d')

  print(f'Iniciando varredura de notícias - {data_execucao}\n' + '=' * 50)

  links_processados = set()

  for tema in TEMAS_BUSCA:
    print(f'Pesquisando: {tema}...')
    try:
      artigos = google_news.get_news(tema)
      noticias_filtradas = []

      if artigos:
        for artigo in artigos:
          link = artigo.get('url', '#')

          # Evita duplicatas globais (se a mesma notícia aparecer em temas diferentes)
          if link in links_processados:
            continue
          links_processados.add(link)

          titulo = artigo.get('title', 'Sem Título')
          fonte = artigo.get('publisher', {}).get('title', 'Fonte Desconhecida')
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

  # 1. Salva o arquivo padrão do dia (usado pelo painel principal)
  with open('noticias_atualizadas.json', 'w', encoding='utf-8') as f:
    json.dump(relatorio_geral, f, ensure_ascii=False, indent=4)

  # 2. Atualiza o banco de dados histórico (historico_geral.json)
  historico = {}
  if os.path.exists('historico_geral.json'):
    try:
      with open('historico_geral.json', 'r', encoding='utf-8') as f:
        historico = json.load(f)
    except:
      historico = {}

  # Adiciona ou substitui o dia de hoje no histórico geral
  historico[data_hoje] = relatorio_geral

  with open('historico_geral.json', 'w', encoding='utf-8') as f:
    json.dump(historico, f, ensure_ascii=False, indent=4)

  print(
      '\nVarredura concluída! Dados salvos em notícias_atualizadas.json e'
      ' historico_geral.json.'
  )


if __name__ == '__main__':
  buscar_noticias()
