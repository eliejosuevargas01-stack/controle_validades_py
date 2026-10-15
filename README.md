# Controle de Validades

Criei o Controle de Validades a partir de uma dificuldade que encontrei no trabalho em supermercado. Eu conseguia abastecer e manter corredores e gôndolas organizados, mas precisava de uma forma melhor de acompanhar os vencimentos. O sistema nasceu para organizar essa rotina e apoiar a retirada dos produtos no momento certo.

## Origem no n8n

A primeira versão foi construída com frontend próprio consumindo webhooks do n8n e persistência em PostgreSQL. O fluxo reúne:

- Cadastro de usuários e produtos, consulta e edição de validades.
- Registro de produtos vendidos e retirados.
- Consulta por produto/EAN e organização por data de vencimento.
- Rotina agendada para selecionar produtos com vencimento nos próximos sete dias.
- Preparação de avisos por WhatsApp ou e-mail e de arquivos com os produtos selecionados.

A leitura da API em 15/10/2026 identificou 50 nós nessa configuração n8n. O código neste repositório reúne a evolução em Python e os frontends legado e React.

## Organização do repositório

- `backend/`: API Python, serviços de produtos e usuários e testes.
- `frontend/legacy_app/`: frontend que preserva a integração com webhooks n8n.
- `frontend/react_app/`: interface React.
- [Relatório explicativo](relatorio_explicativo.md): contexto técnico adicional.

## Projeto relacionado: cartazes de validade e PVPS

Também criei uma automação para identificar os produtos na câmara de resfriados do açougue e facilitar o **PVPS — primeiro que vence, primeiro que sai**.

Informo nome do produto, validade e quantidade de cartazes. O fluxo de WhatsApp guarda os itens em n8n Data Tables e, ao finalizar, gera com JavaScript um PDF A4 em paisagem, com ajuste do tamanho do texto e uma página por cartaz, e prepara o envio do arquivo pelo WhatsApp.

O gerador é um fluxo relacionado no n8n; sua implementação não está incluída neste repositório Python.

## Tecnologias

n8n, JavaScript, webhooks, APIs REST, PostgreSQL, API de WhatsApp, Python e React. A experiência no varejo orientou o problema e as funcionalidades que escolhi construir.
