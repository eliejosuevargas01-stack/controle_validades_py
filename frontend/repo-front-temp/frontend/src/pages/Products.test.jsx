import { describe, test } from 'vitest';

describe('Página Products', () => {
  test.todo('deve listar os produtos carregados da API mostrando Nome, Validade, Qtd, etc');
  test.todo('deve renderizar o formulário de criação com os campos esperados pelo ProductCreate');
  test.todo('deve impedir a submissão se a "quantidade" for menor que 0');
  test.todo('deve impedir a submissão se campos obrigatórios (nome, validade, ean, categoria) estiverem vazios');
  test.todo('deve validar se o payload enviado ao productService.create está no formato correto');
  test.todo('deve exibir botões de Editar e Deletar para cada item da lista e chamar a função correta ao clicar');
});
