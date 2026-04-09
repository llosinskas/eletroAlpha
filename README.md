# ⚡ Bancada Engenharia

Uma bancada profissional para FreeCAD dedicada a projetos elétricos, com foco em se tornar o padrão de projeto elétrico e escalar para projetos de quadros de comando.

## 🎯 Visão Geral

A Bancada Engenharia fornece um conjunto completo de ferramentas para:
- **Design 3D** de instalações elétricas residenciais e comerciais
- **Cálculos elétricos** (cabos, barramento, aterramento, fator de potência)
- **Gestão de componentes** (tomadas, lâmpadas, equipamentos)
- **Documentação técnica** (diagramas, relatórios, listas de materiais)
- **Projetos executivos** completos e profissionais

## ✨ Funcionalidades Principais

### 1. **Sistema de Componentes** ✅ (Implementado)
Insira componentes 3D diretamente do arquivo:
- 📦 Biblioteca de componentes (Tomadas, Lâmpadas, Equipamentos, etc.)
- 🎨 Preview/Thumbnail dos componentes
- 🖱️ Seleção fácil com diálogo intuitivo
- ⚙️ Configuração por callback (reutilizável)
- 🌙 **Suporte a Tema Dark** (Ícones com contorno branco, detectados automaticamente)

**Como usar:**
```
Menu Bancada → Componentes → Inserir Componente
ou
Toolbar "Componentes" → Botão "Inserir Componente"
```

### 2. **Cálculos Elétricos** ⏳ (Em Desenvolvimento)
- Cálculo de seção mínima de cabo
- Cálculo de queda de tensão
- Verificação de corrente
- Cálculos de barramento
- Cálculos de infraestrutura
- Aterramento

### 3. **Diagramas e Documentação** ⏳ (Planejado)
- Diagrama Unifilar automático
- Diagrama Multifilar
- Lista de Materiais
- Planilha de Circuitos
- Relatórios executivos

### 4. **Infraestrutura** ⏳ (Planejado)
- Traçado de Eletrodutos
- Geração automática de caminhos
- Eletrocalhas
- Leitos

---

## 🚀 Começar Rapidinho

### Prérequisitos
- FreeCAD 1.0.2+
- Python 3.7+
- PySide (incluído no FreeCAD)

### Instalação
Já está incluída! Apenas:
1. Abra FreeCAD
2. Selecione a bancada **"Engenharia"** na barra de seleção
3. Pronto! ✓

### Primeiro Uso
1. Crie um novo documento: `File → New`
2. Ative a bancada: Selecione **"Engenharia"** no dropdown
3. Clique em **"Inserir Componente"** (Toolbar ou Menu)
4. Selecione um componente (ex: Tomada)
5. Clique OK
6. Componente inserido no projeto! 🎉

---

## 📚 Documentação Detalhada

### Sistema de Componentes
Para documentação completa sobre seleção e inserção de componentes:
👉 [UI/dialogs/README.md](UI/dialogs/README.md)

### Arquitetura
Para entender a arquitetura interna:
👉 [UI/dialogs/ARCHITECTURE.md](UI/dialogs/ARCHITECTURE.md)

### Quick Start
Para começar em 5 minutos:
👉 [UI/dialogs/QUICKSTART.md](UI/dialogs/QUICKSTART.md)

### Exemplos de Integração
Para ver exemplos com cálculos:
👉 [UI/dialogs/examples_cable_calculation.py](UI/dialogs/examples_cable_calculation.py)

---

## 🗂️ Estrutura do Projeto

```
eletroAlpha/
├── InitGui.py                 # Inicialização da bancada
├── InsertComponent.py         # Comandos de inserção
├── Tools.py                   # Ferramentas diversas
├── NewProject.py              # Criar novo projeto
├── EletricProject.py          # Gerenciar projeto
├── Reports.py                 # Gerar relatórios
├── GerarUnifilar.py          # Gerar diagrama unifilar
├── importQEletrotech.py      # Importar QEletrotech
├── ProjetoQuadro.py          # Projetos de quadro
│
├── UI/
│   ├── dialogs/              # 🆕 Sistema de componentes
│   │   ├── ComponentSelectorDialog.py
│   │   ├── ComponentInserter.py
│   │   ├── README.md
│   │   ├── QUICKSTART.md
│   │   ├── ARCHITECTURE.md
│   │   └── examples_cable_calculation.py
│   ├── Cards.py
│   └── insert_circuit.py
│
├── core/
│   ├── functions/
│   │   ├── Cabo/             # Cálculos de cabo
│   │   │   ├── Cabo.py
│   │   │   ├── Correntes.py
│   │   │   ├── queda_tensao.py
│   │   │   └── ...
│   │   ├── Barramento.py
│   │   └── ...
│   └── eletromecanico/
│
├── Tables/
│   ├── NBR5410/              # Tabelas NBR 5410
│   └── NBR14039/             # Tabelas NBR 14039
│
├── Componentes/
│   └── Eletrica/             # Biblioteca de componentes
│       ├── Tomada.FCStd
│       ├── Lampada.FCStd
│       └── ...
│
├── config/
├── tests/
├── docs/                      # Documentação
└── Resources/
    └── Icons/                 # Ícones da bancada
```

---

## 📖 Menu da Bancada

Ao ativar a bancada "Eletro Alpha", você terá acesso a:

### Menu "Componentes"
- ✅ Inserir Componente
- ✅ Inserir Tomada
- ✅ Inserir Equipamento
- ⏳ Inserir Fiação
- ⏳ Inserir Eletroduto
- ⏳ Inserir Eletrocalha

### Menu "Novo Projeto"
- Criar novo projeto elétrico
- Adicionar spreadsheet
- Criar modelo

### Menu "Diagrama Unifilar"
- Gerar diagrama unifilar
- Gerar planilha de circuitos
- Adicionar circuito

### Menu "Quadro Elétrico"
- Criar novo quadro

### Menu "Relatórios"
- Gerar relatório

---

## 🔧 Configuração

### Pasta de Componentes
Os componentes estão em:
```
Componentes/Eletrica/
├── Tomada.FCStd
├── Lampada.FCStd
├── Tomadas.FCStd
└── ...
```

**Para adicionar novo componente:**
1. Crie arquivo 3D no FreeCAD: `File → Save As → component.FCStd`
2. Adicione um thumbnail (salva automaticamente no formato correto)
3. Coloque em `Componentes/Eletrica/`
4. Pronto! Aparecerá no seletor ao clicar no botão

---

## 💡 Exemplos de Uso

### Exemplo 1: Inserir uma Tomada
```
1. Menu → Componentes → Inserir Tomada
2. Diálogo abre com preview dos componentes
3. Clique em "Tomada"
4. Clique OK
5. Tomada inserida no projeto
```

### Exemplo 2: Integrar com Cálculo
```python
from UI.dialogs import ComponentInserter

def meu_callback(filepath, objeto):
    print(f"Componente inserido: {objeto.Label}")
    # Executar cálculo aqui

inserter = ComponentInserter(
    "Componentes/Eletrica",
    on_component_loaded=meu_callback
)
inserter.insert_component()
```

Ver arquivo `UI/dialogs/examples_cable_calculation.py` para 3 exemplos completos!

---

## 🗺️ Roadmap

### ✅ Concluído (v0.1)
- [x] Sistema de seleção e inserção de componentes
- [x] Preview com thumbnails
- [x] Integração com bancada
- [x] Documentação técnica

### ⏳ Próximo (v0.2)
- [ ] Modo posicionamento com mouse
- [ ] Cálculos de cabo básicos
- [ ] Filtros avançados de componentes
- [ ] Teste unitário

### 🚀 Futuro (v0.3+)
- [ ] Traçado automático de eletrodutos
- [ ] Geração de diagrama unifilar
- [ ] Cálculos completos (barramento, aterramento, FP)
- [ ] Relatórios automáticos
- [ ] Exportação (DWG, PDF)
- [ ] Integração com QEletrotech

---

## 🐛 Troubleshooting

### "Sistema de Componentes não aparece"
- Verifique pasta `Componentes/Eletrica/`
- Arquivos devem ser `.FCStd` (não `.FCBak`)
- Recrie a pasta se necessário

### "Thumbnails vazios"
- Isso é normal, usa fallback de ícone genérico
- Para adicionar thumbnail: abra `.FCStd` no FreeCAD e re-salve

### "Erro ao inserir componente"
- Verifique se um documento está aberto
- Tente recarregar a bancada (Menu → Ferramentas → Reiniciar Bancada)

### "Bancada não aparece"
- Reinicie FreeCAD
- Verifique pasta `Mod/eletroAlpha/`

### "Ícones muito escuros em tema dark"
- Os ícones são aprimorados automaticamente ao ativar a bancada
- Se não funcionar, execute manualmente:
  ```bash
  cd c:\Users\lucas\AppData\Roaming\FreeCAD\v1-1\Mod\eletroAlpha
  python utils/icon_manager.py
  ```
- Reinicie a bancada para aplicar as mudanças
- Ver: [utils/ICON_MANAGER.md](utils/ICON_MANAGER.md) para mais detalhes

---

## 📝 Notas de Versão

### v0.2 (2026-04-08)
- ✅ **Suporte completo a tema dark**
  - Detecção automática de tema (light/dark)
  - Aprimoramento de ícones com contorno branco (drop-shadow SVG)
  - 39 ícones processados (36 principais + 3 símbolos)
  - Inicialização automática ao ativar bancada
- ✅ Novo módulo `utils/icon_manager.py`
- ✅ Documentação em `utils/ICON_MANAGER.md`

### v0.1 (2026-04-08)
- ✅ Implementação do sistema de componentes
- ✅ Diálogo com busca em tempo real
- ✅ Preview de thumbnails
- ✅ Integração com bancada FreeCAD
- ✅ Documentação técnica completa
- ✅ 3 exemplos de integração

---

## 👨‍💻 Desenvolvimento e Contribuição

### Para Desenvolvedores
A bancada foi estruturada para ser fácil de estender:

**Adicionar novo tipo de componente:**
1. Crie pasta em `Componentes/` (ex: `Componentes/Cabos/`)
2. Adicione arquivos `.FCStd`
3. Use `ComponentSelectorDialog` apontando para essa pasta

**Integrar com cálculos:**
```python
from UI.dialogs import ComponentInserter

inserter = ComponentInserter(
    "sua/pasta/componentes",
    on_component_loaded=seus_calculos
)
```

Ver `UI/dialogs/README.md` para API completa!

---

## 📞 Suporte

- Versão do FreeCAD: 0.19+
- Python: 3.7+
- Sistema: Windows, Linux, macOS
- Licença: (Defina sua licença)

---

## 🎓 Aprender Mais

- [Documentação técnica de Componentes](UI/dialogs/README.md)
- [Arquitetura interna](UI/dialogs/ARCHITECTURE.md)
- [Quick Start em 5 minutos](UI/dialogs/QUICKSTART.md)
- [Exemplos com cálculos](UI/dialogs/examples_cable_calculation.py)
- [Gerenciador de Ícones (Tema Dark)](utils/ICON_MANAGER.md)
- [Resumo de Atualização Dark Theme](DARK_THEME_UPDATE.md)

---

## 📅 Histórico

| Versão | Data | Alterações |
|--------|------|-----------|
| 0.1 | 2026-04-08 | Sistema de componentes implementado |
| 0.0 | 2026-03 | Inicial |

---

**Desenvolvido com ❤️ para ElectroAlpha**

*Última atualização: 2026-04-08*
