# Documentação do Projeto "Sistema de E-commerce com Django"

## Introdução

O "Sistema de E-commerce com Django" é uma aplicação desenvolvida utilizando Python com o framework Django, HTML, CSS e JavaScript. É um e-commerce simples, ate o momento foi abstraido a forma de pagamento, mas futuramente sera adicionada. O objetivo deste sistema é criar uma plataforma de comércio eletrônico que permite aos usuários visualizar, pesquisar, adicionar ao carrinho, pagar e gerenciar produtos. O projeto está estruturado em apps individuais, cada um focado em funcionalidades específicas.

## Estrutura do Projeto

### Apps do Projeto

**1. Perfil:**

+ Responsável pelo gerenciamento de perfis de usuários, incluindo informações pessoais e endereço.
+ Models: Perfil
+ Views: BasePerfil, Criar, Atualizar, Login, Logout
+ Forms: PerfilForm, UserForm

**2. Produto:**

+ Gerencia informações sobre os produtos disponíveis para venda.
+ Models: Produto, Variacao
+ Views: ListaProdutos, Busca, DetalheProduto, AdicionarCarrinho, RemoverCarrinho, Carrinho, ResumoDaCompra

**3. Pedido:**

+ Lida com a criação, pagamento e visualização detalhada dos pedidos.
+ Models: Pedido, ItemPedido
+ Views: DispatchLoginRequiredMixin, Pagar, SalvarPedido, Detalhe, Lista

### Funcionalidades Gerais

**1. Autenticação de Usuário:**

+ Os usuários podem se autenticar, criar contas e atualizar perfis.

**2. Visualização de Produtos:**

+ Exibição de lista de produtos, pesquisa por termo, visualização detalhada de produtos.

**3. Carrinho de Compras:**

+ Adição, remoção e visualização de itens no carrinho de compras.

**4. Pedido e Pagamento:**

+ Criação de pedidos, processamento de pagamentos e visualização detalhada dos pedidos.

**5. Dashboard Principal:**

Exibição de informações cruciais, como últimas compras, pedidos pendentes e promoções.
### Apps Individuais

**Perfil:**

+ Gerencia informações pessoais e endereço dos usuários.

**Produto:**

+ Gerencia informações sobre os produtos disponíveis, incluindo nome, descrição, preço, promoções e variações.

**Pedido:**

+ Lida com a criação, pagamento e detalhes dos pedidos realizados pelos usuários.
## Considerações Finais

O sistema de e-commerce proporciona uma experiência completa aos usuários (abstraindo sistema de pagamento), permitindo que eles naveguem pela loja, adicionem produtos ao carrinho, efetuem pagamentos e gerenciem seus pedidos. A estrutura modular do projeto facilita a expansão e a adição de novas funcionalidades no futuro. Contribuições são bem-vindas, e o projeto está aberto para melhorias e correções de bugs.

Autor: Flauziino - Desenvolvedor

Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir um pull request ou relatar problemas abrindo uma issue.