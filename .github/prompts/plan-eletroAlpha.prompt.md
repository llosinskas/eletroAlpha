# 📋 PLANEJAMENTO ESTRATÉGICO - eletroAlpha Workbench
**Versão**: 1.0 | **Data**: 2026-04-07 | **Horizonte**: 6 meses | **Team**: 2-3 pessoas

---

## RESUMO EXECUTIVO (TL;DR)

Transformar eletroAlpha de um protótipo frágil (2.5/10 qualidade) em uma suite profissional (8/10+) através de:
1. **Fase 0**: Eliminar bugs críticos que travam inicialização
2. **Fase 1**: Refatoração arquitetural com abstração e padrões
3. **Fase 2**: Implementar 6 features principais solicitadas
4. **Fase 3**: Otimizações, testes e documentação

**Abordagem**: API-first, TDD (Test-Driven), documentação contínua

---

## FASE 0: STABILIZAÇÃO IMEDIATA (SEMANA 1-2)
**Objetivo**: Tornar a bancada usável + preparar base para refatoração

### 0.1 Corrigir Bugs Críticos 
**Impacto**: Bancada não carrega sem isso

- [ ] **InitGui.py**: Mover import WorkbenchBase para escopo global (FEITO)
- [ ] **WorkbenchBase.py**: Corrigir path resolution com try/except (FEITO)
- [ ] **Tools.py**: ReiniciarBancada sem usar reload() (FEITO)
- [ ] **calculo_cabo.py**: Corrigir `import numpy as pd` → `import numpy as np`
- [ ] **Eletro_libs.py**: Remover código comentado ou documentriar

### 0.2 Criar Estrutura de Logging
**Arquivo**: `config/logging_config.py`
```python
import logging
import logging.handlers
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger('eletroAlpha')
logger.setLevel(logging.DEBUG)

# Console + file handler
handler = logging.handlers.RotatingFileHandler(
    os.path.join(LOG_DIR, 'eletroAlpha.log'),
    maxBytes=10485760,  # 10MB
    backupCount=5
)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
```

**Benefício**: Depreca `App.Console.PrintError()` frágil

### 0.3 Centralizar Constantes
**Arquivo**: `config/constants.py`
```python
# Eletrônicos
CABLE_SECTIONS_MM2 = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240]
STANDARD_PHASES = [1, 3]
STANDARD_VOLTAGES = [127, 220, 380]  # V
MAX_VOLTAGE_DROP = 0.03  # 3% NBR5410

# UI
ICON_PATH_DEFAULT = "Resources/Icons"
DEFAULT_TIMEOUT = 5000  # ms

# Diretórios
COMPONENT_LIBRARY_PATH = "Componentes/Eletrica"
TEMPLATES_PATH = "templates"
DATABASE_PATH = "data/components.db"
```

### 0.4 Validação Rápida
**Teste**: Abrir FreeCAD e carregar bancada sem erros
- [ ] Inicializar eletroAlpha
- [ ] Clicar "Reiniciar Bancada" (não deve dar erro)
- [ ] Verificar `logs/eletroAlpha.log`

**Status**: ✅ PRONTO

---

## FASE 1: FUNDAÇÃO ARQUITETURAL (SEMANA 3-6)
**Objetivo**: Base sólida, testável e escalável | **Responsável**: Lead Dev

### 1.1 Criar Camada de Abstração FreeCAD
**Arquivo**: `adapters/freecad_adapter.py`

```python
class DocumentAdapter:
    """Abstração para App.Document"""
    def __init__(self, doc=None):
        self.doc = doc or App.ActiveDocument
    
    def add_group(self, name: str):
        return self.doc.addObject("App::DocumentObjectGroup", name)
    
    def get_object(self, label: str):
        return self.doc.getObject(label)
    
    def recompute(self):
        self.doc.recompute()

class GUIAdapter:
    """Abstração para FreeCADGui"""
    @staticmethod
    def add_command(cmd_id: str, command: object):
        Gui.addCommand(cmd_id, command)
    
    @staticmethod
    def activate_workbench(name: str):
        Gui.activateWorkbench(name)
```

**Benefício**: Código testável sem FreeCAD rodando

### 1.2 Hierarquia de Classes Base
**Arquivo**: `base/commands.py`

```python
from abc import ABC, abstractmethod

class BaseCommand(ABC):
    """Classe base para todos os comandos"""
    
    @abstractmethod
    def Activated(self):
        pass
    
    @abstractmethod
    def GetResources(self) -> dict:
        pass
    
    def IsActive(self) -> bool:
        return True
    
    def get_icon(self, icon_name: str) -> str:
        from config.constants import ICON_PATH_DEFAULT
        return os.path.join(ICON_PATH_DEFAULT, icon_name)
```

### 1.3 Modelo de Dados com Validação
**Arquivo**: `models/circuit_model.py`

```python
from dataclasses import dataclass
from pydantic import BaseModel, Field, validator

class CircuitDTO(BaseModel):
    """Data Transfer Object para Circuito"""
    origin: str = Field(..., min_length=1)
    destiny: str = Field(..., min_length=1)
    power_kw: float = Field(..., gt=0)
    voltage_v: int = Field(..., ge=127)
    power_factor: float = Field(..., ge=0.5, le=1.0)
    cable_section_mm2: float = Field(..., gt=0)
    breaker_current_a: float = Field(..., gt=0)
    
    @validator('power_factor')
    def validate_pf(cls, v):
        if v < 0.8:
            raise ValueError("Fator de potência abaixo de 0.8 é incomum")
        return v

class CircuitRepository:
    """Persistência de circuitos na planilha"""
    
    def save(self, circuit: CircuitDTO):
        """Valida e salva na planilha"""
        # TODO: Implementar
        pass
    
    def load(self, circuit_id: str) -> CircuitDTO:
        """Carrega e valida do spreadsheet"""
        # TODO: Implementar
        pass
```

### 1.4 Inverter Dependências com Dependency Injection
**Arquivo**: `container.py`

```python
class DIContainer:
    """Injeção de dependência para desacoplamento"""
    
    def __init__(self):
        self._services = {}
    
    def register(self, name: str, service):
        self._services[name] = service
    
    def get(self, name: str):
        return self._services.get(name)

# Uso em comandos:
class NewCircuit(BaseCommand):
    def __init__(self, container: DIContainer):
        self.circuit_repo = container.get('circuit_repository')
        self.logger = container.get('logger')
```

### 1.5 Estrutura de Testes
**Arquivo**: `tests/test_circuit_model.py`

```python
import pytest
from models.circuit_model import CircuitDTO

def test_circuit_validation():
    # Válido
    circuit = CircuitDTO(
        origin="Q1", destiny="L1",
        power_kw=5.0, voltage_v=220,
        power_factor=0.95, cable_section_mm2=4.0,
        breaker_current_a=20.0
    )
    assert circuit.power_kw == 5.0
    
    # Inválido: potência negativa
    with pytest.raises(ValueError):
        CircuitDTO(
            origin="Q1", destiny="L1",
            power_kw=-1.0, ...  # ❌
        )
```

**Setup**: 
```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=core
```

### 1.6 Documentação Inicial
**Arquivo**: `docs/ARCHITECTURE.md`
```markdown
# Arquitetura eletroAlpha

## Camadas
1. **GUI** (PySide2): Diálogos e interações
2. **Commands**: Implementam Command Pattern
3. **Business Logic**: Cálculos (core/functions)
4. **Data**: Modelos e repositórios
5. **Adapters**: Abstração FreeCAD

## Fluxo
User → GUI Dialog → Command.Activated() → Repository → Model → FreeCAD.Document
```

**Status**: 🔧 Em progresso

---

## FASE 2: FEATURES PRINCIPAIS (SEMANA 7-16)
**Objetivo**: Implementar 6 features solicitadas | **Responsável**: Dev + Colaboradores

### 2.1 Sistema de Validação e Checklist
**Timeline**: Semana 7-8

**Arquivos**:
- `features/validation/checklist_model.py` - DTO
- `features/validation/checklist_service.py` - Lógica
- `UI/validation_dialog.py` - Interface PySide

**Especificação**:
```python
class ProjectChecklist:
    """Checklist de projeto elétrico NBR5410"""
    checks = {
        "carga_conectada": {"status": False, "peso": 10},
        "circuitos_definidos": {"status": False, "peso": 15},
        "seções_validadas": {"status": False, "peso": 20},
        "eletrodutos_ok": {"status": False, "peso": 15},
        "proteções_ok": {"status": False, "peso": 20},
        "aterramento_ok": {"status": False, "peso": 10},
        "documentação_ok": {"status": False, "peso": 10},
    }
    
    def score(self) -> float:
        """Retorna % de conclusão"""
        return sum(v["peso"] for v in self.checks.values() if v["status"]) / 100
```

### 2.2 Gerador de Relatórios
**Timeline**: Semana 9-11

**Dependências**: 
```bash
pip install reportlab openpyxl
```

**Arquivos**:
- `features/reports/report_generator.py` - Engine
- `features/reports/templates/` - Modelos LaTeX/HTML
- `UI/report_dialog.py` - Dialog PySide

**Formatos Suportados**:
- PDF (ReportLab)
- Excel (openpyxl)
- HTML (Jinja2)

### 2.3 Integração com Banco de Dados
**Timeline**: Semana 12-13

**Tecnologia**: SQLite + SQLAlchemy (leve, sem server)

```python
# models/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(f'sqlite:///{DATABASE_PATH}')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class ComponentModel(Base):
    __tablename__ = 'components'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category = Column(String)  # "Cable", "Breaker", "Wire"
    properties = Column(JSON)  # {"section_mm2": 4.0, ...}
```

### 2.4 Cálculos de Demanda Avançados
**Timeline**: Semana 7-8 (paralelo com 2.1)

**Arquivo**: `core/functions/Demanda.py` (implementar)

```python
class DemandaCalculator:
    """NBR5410 - Métodos de cálculo de demanda"""
    
    def metodo_cv(self, potencias: List[float], simultaneidade=0.8) -> float:
        """Método da Curva de Vigência"""
        return sum(potencias) * simultaneidade
    
    def metodo_ppv(self, circuitos: List[CircuitDTO]) -> float:
        """Método das Potências de Projeto Verificadas"""
        # TODO: Implementar algoritmo
        pass
```

### 2.5 Sistema de Templates/Presets
**Timeline**: Semana 14

**Arquivo**: `features/templates/template_manager.py`

```python
class TemplateManager:
    """Gerencia templates predefinidos"""
    
    TEMPLATES = {
        "residencial_100a": {
            "circuitos": ["Iluminação", "Tomadas", "Chuveiro"],
            "demand_factor": 0.75,
            "voltage": 220
        },
        "comercial_200a": {
            "circuitos": ["Escritório", "HVAC", "Cargas"],
            "demand_factor": 0.85,
            "voltage": 380
        }
    }
    
    def apply_template(self, name: str):
        template = self.TEMPLATES.get(name)
        # TODO: Criar projeto baseado em template
```

### 2.6 Exportação para Softwares Comerciais
**Timeline**: Semana 15-16

**Formatos**:
- QEletrotech (`.qet` - XML)
- DWG/DXF (via `opendxf`)
- JSON (interoperabilidade)

**Arquivo**: `features/export/exporters.py`

```python
class QEtechExporter:
    """Exporta diagramas para QEletrotech"""
    def export(self, project, filepath: str):
        # TODO: Gerar XML conforme spec QEtech
        pass

class DXFExporter:
    """Exporta para AutoCAD DXF"""
    def export(self, project, filepath: str):
        # TODO: Usar ezdxf ou similar
        pass
```

---

## FASE 3: OTIMIZAÇÕES E POLISH (SEMANA 17-24)
**Objetivo**: Produto pronto para produção

### 3.1 Testes Completos (TDD)
```bash
# Target: >80% cobertura
pytest tests/ --cov=core --cov=features --cov-report=html
```

### 3.2 Documentação
- [ ] API reference (Sphinx)
- [ ] Tutorial de uso (12 páginas PDF)
- [ ] Guia de desenvolvimento (para colaboradores)

### 3.3 Performance
- [ ] Profile com `cProfile` em operações pesadas
- [ ] Cache de cálculos (CircuitCalculator)
- [ ] Lazy loading de componentes

### 3.4 Assistência de IA
- [ ] Verificação de code style com `black`
- [ ] Análise estática com `pylint`
- [ ] Type hints (`mypy`)

---

## ESTRUTURA DE PASTAS PROPOSTA

```
eletroAlpha/
├── 📁 base/                    # Abstrações base
│   ├── commands.py            # BaseCommand
│   ├── models.py              # BaseModel
│   └── __init__.py
│
├── 📁 config/                 # Configurações
│   ├── constants.py           # Constantes globais
│   ├── logging_config.py      # Setup logging
│   └── settings.py            # Variáveis ambiente
│
├── 📁 adapters/               # Abstrações FreeCAD
│   ├── freecad_adapter.py
│   ├── gui_adapter.py
│   └── __init__.py
│
├── 📁 models/                 # Dados e ORM
│   ├── circuit_model.py       # CircuitDTO
│   ├── component_model.py     # ComponentDTO
│   ├── database.py            # SQLAlchemy setup
│   └── __init__.py
│
├── 📁 repositories/          # Persistência
│   ├── circuit_repository.py
│   ├── component_repository.py
│   └── __init__.py
│
├── 📁 features/              # Features principais
│   ├── validation/
│   ├── reports/
│   ├── templates/
│   ├── export/
│   └── __init__.py
│
├── 📁 core/                  # Lógica de negócio
│   ├── functions/
│   ├── simulation/
│   ├── projectsbim/
│   └── __init__.py
│
├── 📁 UI/                    # Interface PySide
│   ├── dialogs/
│   ├── widgets/
│   ├── forms/
│   └── __init__.py
│
├── 📁 tests/                 # Testes
│   ├── unit/
│   ├── integration/
│   ├── conftest.py
│   └── __init__.py
│
├── 📁 docs/                  # Documentação
│   ├── ARCHITECTURE.md
│   ├── CONTRIBUTING.md
│   ├── QUICKSTART.md
│   └── API.md
│
├── 📁 logs/                  # Logs (gitignored)
│
├── 📄 container.py           # Dependency Injection
├── 📄 InitGui.py             # Entry point FreeCAD
├── 📄 WorkbenchBase.py
├── 📄 requirements.txt
├── 📄 pytest.ini
├── 📄 .gitignore
├── 📄 README.md
└── 📄 CHANGELOG.md
```

---

## MELHORES PRÁTICAS DE CODIFICAÇÃO

### ✅ Convenções de Código

**1. Nomenclatura**
```python
# Variables
circuit_id = "Q1"  # snake_case
CABLE_SECTIONS = [...]  # CONSTANTS_ARE_UPPER
class CircuitValidator:  # PascalCase
    def calculate_demand(self):  # method_snake_case
```

**2. Type Hints OBRIGATÓRIOS**
```python
# ❌ Ruim
def calculate(power, voltage):
    return power / voltage

# ✅ Bom
def calculate(power: float, voltage: float) -> float:
    """Calcula corrente (A) a partir de potência (kW) e tensão (V)"""
    return (power * 1000) / voltage
```

**3. Docstrings**
```python
def create_project(name: str, voltage: int = 220) -> bool:
    """
    Cria um novo projeto elétrico.
    
    Args:
        name: Nome do projeto (ex: "Residência_Rua_A_123")
        voltage: Tensão nominal em volts. Padrão: 220V
    
    Returns:
        True se criado com sucesso, False caso contrário
    
    Raises:
        ValueError: Se name está vazio
        
    Examples:
        >>> create_project("Casa_Nova")
        True
    """
```

**4. Logging em vez de Print**
```python
# ❌ Ruim
print("Circuito adicionado!")
App.Console.PrintError("Erro!")

# ✅ Bom
logger.info("Circuito adicionado: %s", circuit_id)
logger.error("Erro ao carregar componente", exc_info=True)
```

**5. Tratamento de Exceções**
```python
# ❌ Ruim
try:
    calculate()
except:
    pass

# ✅ Bom
try:
    result = calculate(power, voltage)
except ValueError as e:
    logger.error("Valor inválido: %s", str(e), exc_info=True)
    raise
except Exception as e:
    logger.critical("Erro inesperado", exc_info=True)
    raise
```

### ✅ Organização do Projeto

**1. Um arquivo = uma responsabilidade**
```
✅ circuit_model.py (só modelos)
✅ circuit_repository.py (só persistência)
❌ circuit.py (tudo junto)
```

**2. Imports organizados**
```python
# Stdlib
import os
import json
from typing import List, Optional

# Third-party
import numpy as np
from pydantic import BaseModel

# Local
from config.constants import CABLE_SECTIONS
from base.commands import BaseCommand
```

**3. Tamanho de funções**
- Ideal: <30 linhas
- Máximo: <50 linhas
- Muito complexo? Quebrar em subfunções

### ✅ Versionamento para Colaboração

**Git Workflow**:
```bash
# Branch por feature
git checkout -b feature/validation-checklist

# Commits descritivos
git commit -m "feat: implementar checklist de projeto NBR5410"

# Tags para releases
git tag -a v0.2.0 -m "Release com validação"
```

### ✅ Code Review Checklist

Antes de fazer merge:
- [ ] Testes passando (`pytest -v`)
- [ ] Type hints completos (`mypy .`)
- [ ] Sem warnings (`pylint models/`)
- [ ] Documentação atualizada
- [ ] Exemplo de uso na docstring

---

## ROADMAP VISUAL (Timeline)

```
📅 SEMANA
1-2     [████████] FASE 0: Bugs críticos + Logging
3-6     [████████████] FASE 1: Arquitetura base
        └─ 3-4: Abstrações
        └─ 4-5: Modelos + Testes
        └─ 5-6: DI + Documentação

7-8     [████] Validação + Demanda
9-11    [██████] Relatórios
12-13   [████] Banco de dados
14      [██] Templates
15-16   [████] Exportação

17-20   [█████████] Testes + Qualidade
21-24   [████████] Documentação + Polish
```

---

## MÉTRICAS DE SUCESSO

| Métrica | Baseline | Target | Método |
|---------|----------|--------|--------|
| **Qualidade do Código** | 2.5/10 | 8/10 | SonarQube |
| **Cobertura de Testes** | 0% | >80% | pytest --cov |
| **Type Hints** | 10% | 100% | mypy strict |
| **Documentação** | 5% | 100% | sphinx index |
| **Features Funcionando** | 40% | 100% | Checklist |
| **Time Produtividade** | - | +200% | Git velocity |

---

## PRÓXIMOS PASSOS

1. ✅ **IMEDIATO (hoje)**: Aprovação do plano
2. 🔧 **SEMANA 1**: Iniciar Fase 0 com code review desta análise
3. 📋 **SEMANA 3**: Briefs de desenvolvimento para cada feature
4. 👥 **ONBOARDING**: Documentar para colaboradores

---

**Responsável planejamento**: GitHub Copilot
**Última atualização**: 2026-04-07 13:45
**Status**: 🟢 Pronto para aprovação
