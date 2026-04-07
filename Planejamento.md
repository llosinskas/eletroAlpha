# Planejamento da bancada do Freecad de elétrica

A bancada é uma ferramenta para o apoio para projetos elétricos onde pretendemos substituir softwares comerciais para projetos eletricos e escalar para projetos de quadros de comando
## Ideias de melhorias
1. Definir uma arquitetura para o projeto 
1. Refatorar o código para ser mais fácil para manutenção do código 
    1. Templates reutilizados para cards calculos
1. Adicionar funcionalidade:
    1. Gerar um caixa de diálogo onde liste todos os componentes dentro de uma pasta e insira no projeto principal EX: Tomadas, Lâmpadas, chuveiros etc. 
    Esses elementos vai ter duas pastas 1 a modelagem 3D e 2 o desenho 2D
    1. Botão para criar caminho do eletrodutos
    1. Botão para gerar eletrodutos do caminho já colocado.
    1. Botão para criar lista de materiais
    1. Botão para criar um diagrama multifilar 
    1. Botão criar planilhas de quadro e rebalancear fase
    1. Botão para gerar relatórios como memoriais, lista de materiais, diagramas
    1. Botão para gerar diagramas unifilares a partir dos circuitos definidos na lista de materiais
    1. Botão para criar projeto executivo

1. Estrutura para os calculos elétricos 
    1. Cálculos de cabos
    1. Cálculos de barramento
    1. Cálculos de infraestrutura
    1. Cálculos de aterramento
    1. Fator de Potência
    1. Capacitores

1. Problemas para pensar
    1. Conexão entre eletroduto do teto com eletroduto no solo ou tomadas 

1. Necessidades
    1. é precisso de um banco de dados sql?