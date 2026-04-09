# Icon Manager - Gerenciador de Ícones para Tema Dark

## Visão Geral

O `IconManager` é um utilitário que detecta automaticamente o tema (light/dark) do FreeCAD e aprimora os ícones SVG com contorno branco para melhor visibilidade em modo dark.

## Características

✅ **Detecção automática de tema** - Detecta se FreeCAD está em modo dark ou light
✅ **Processamento em lote** - Modifica todos os ícones SVG de uma pasta
✅ **Filtros SVG avançados** - Adiciona drop-shadow branco para contraste
✅ **Sem modificação de origináis** - Estilos inline no SVG, sem arquivos separados
✅ **Integração automática** - Inicializa ao ativar a bancada

## Uso

### Automático (Recomendado)

Os ícones são aprimorados automaticamente quando a bancada é ativada:

```python
# Em InitGui.py, já configurado
def Activated(self):
    from utils.icon_manager import initialize_dark_theme_icons
    initialize_dark_theme_icons()
```

### Manual

Para processar ícones manualmente:

```bash
cd c:\Users\lucas\AppData\Roaming\FreeCAD\v1-1\Mod\eletroAlpha
python utils/icon_manager.py
```

### Programático

```python
from utils.icon_manager import IconManager

# Criar gerenciador
manager = IconManager()

# Aprimorar um ícone específico
manager.enhance_svg_for_dark_theme('Resources/Icons/logo.svg')

# Aprimorar todos os ícones
total, success = manager.add_white_stroke_to_all_icons()
print(f"Processados: {success}/{total}")

# Detectar tema atual
if manager.is_dark_theme:
    print("Tema dark detectado")
```

## Técnica de Aprimoramento

O gerenciador adiciona filtros CSS SVG que:

1. **Drop-shadow com 4 direções** - Cria um efeito de contorno branco
2. **Stroke-width aumentada** - Melhora a visibilidade de linhas finas
3. **Filter compound** - Combina múltiplos drop-shadows para contorno suave

Exemplo do estilo adicionado:

```xml
<style>
    path, circle, ellipse { 
        stroke-width: 1.2; 
        filter: drop-shadow(-0.5px -0.5px 0 white) 
                drop-shadow(0.5px -0.5px 0 white) 
                drop-shadow(-0.5px 0.5px 0 white) 
                drop-shadow(0.5px 0.5px 0 white);
    }
</style>
```

## Detecção de Tema

O gerenciador detecta o tema dark verificando a luminância da cor de fundo do FreeCAD:

```python
# Luminância = 0.299*R + 0.587*G + 0.114*B
# Se < 128 → Tema dark
# Se >= 128 → Tema light
```

## Ícones Processados

### Pasta: Resources/Icons (36 arquivos)
- Logo, componentes, conduite, fio, lampada, tomadas, etc.
- Todos aprimorados com contorno branco

### Pasta: Resources/Icons/simbologia (3 arquivos)  
- interruptor.svg
- tomada.svg
- tomadaespecial.svg

## Troubleshooting

### Ícones ainda aparecem escuros?

1. **Verifique se o FreeCAD está em modo dark:**
   ```python
   from utils.icon_manager import IconManager
   manager = IconManager()
   print(f"Dark theme: {manager.is_dark_theme}")
   ```

2. **Reprocesse os ícones:**
   ```bash
   python utils/icon_manager.py
   ```

3. **Reinicie a bancada:**
   - Desative e reactive a bancada no FreeCAD

### Erro ao importar?

Verifique se `utils/__init__.py` existe (deve estar vazio ou com imports).

## Futuras Melhorias

- [ ] Suporte a tons de cinza personalizados
- [ ] Integração com temas de cores do FreeCAD
- [ ] Cache de ícones processados
- [ ] Suporte a PNG e outros formatos
- [ ] Ajuste automático de brilho baseado em contraste

## Arquivos Relacionados

- **InitGui.py** - Chama `initialize_dark_theme_icons()` ao ativar
- **utils/icon_manager.py** - Código-fonte do gerenciador
- **Resources/Icons/** - Diretório de ícones

---

**Versão:** 0.1  
**Data:** 2026-04-08  
**Módulo:** utils.icon_manager
