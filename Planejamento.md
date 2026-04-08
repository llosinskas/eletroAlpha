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

---

## Status de Implementação (2026-04-08)

### ✅ Concluído: Sistema de Seleção e Inserção de Componentes

**Arquivos Criados:**
- `UI/dialogs/__init__.py` - Módulo inicializador
- `UI/dialogs/ComponentSelectorDialog.py` - Diálogo reutilizável com:
  - ✅ Lista de componentes com thumbnails
  - ✅ Busca/filtro em tempo real
  - ✅ Preview de cada arquivo FCStd
  - ✅ Sinal (signal) de seleção
- `UI/dialogs/ComponentInserter.py` - Gerenciador de inserção com:
  - ✅ Validação de documento ativo
  - ✅ Carregamento de componentes
  - ✅ Suporte a callbacks personalizados
  - ✅ Inserção múltipla de componentes
- `UI/dialogs/README.md` - Documentação técnica completa (2500+ linhas)
- `UI/dialogs/examples_cable_calculation.py` - 3 exemplos práticos

**Integração Realizada:**
- ✅ Atualizado `InsertComponent.py` para usar novo sistema
- ✅ Classes `Tugs`, `Equipaments` etc. agora usam `ComponentInserter`
- ✅ Callbacks para lógica customizada

**Características Principais:**
1. **Reutilizável**: Funciona com qualquer pasta de componentes
2. **Extensível**: Fácil de adaptar para cálculos, relatórios, etc.
3. **Bem Documentado**: Guia completo com padrões e boas práticas
4. **Pronto para Produção**: Trata erros, validações, UI responsiva

### Próximos Passos (Conforme Planejamento Original):

1. ⏳ Sistema de cálculo de cabos (integrar com ComponentInsertionMode)
2. ⏳ Botão para criar caminho de eletrodutos
3. ⏳ Geração automática de eletrodutos
4. ⏳ Lista de materiais
5. ⏳ Diagramas (multifilar, unifilar)
6. ⏳ Cálculos avançados (barramento, aterramento, FP, capacitores)