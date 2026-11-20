# Marca

Identidade visual do EstadiaFlow. Slogan: "Gerencie. Automatize. Encante."

## Símbolo

Uma casa em contorno aberto, atravessada por um check que nasce de um rastro em movimento. A casa é a hospedagem; o check, a operação concluída; o rastro, o fluxo da estadia passando pela casa. Não usa avião, mala nem outros símbolos de viagem aérea.

- Abaixo de ~40 px, use a **versão reduzida**: sem o rastro e com traço mais grosso.
- O desenho é definido em `scripts/build-brand.py` (constantes `ROOF`, `BASE`, `TAIL`, `CHECK`) e replicado em `apps/web/src/components/brand/Logo.tsx`.

## Cores

| Nome | Hex | Papel |
|---|---|---|
| Azul-marinho | `#0B1B4D` | Confiança. Nome, textos, menu lateral, fundos escuros. |
| Ciano | `#19C8F5` | Tecnologia. Check e detalhes. Não usar como fundo de texto branco nem como cor de texto: não tem contraste. |
| Azul elétrico | `#2563EB` | Modernidade. Botões, links, destaques e cor do tema do navegador. |
| Violeta | `#7C3AED` | Inteligência e automação. Fim do degradê. |

Degradês:

- **Da marca** (`--ho-logo-gradient`): ciano → azul elétrico → violeta. Para ícones de app, avatar do Instagram e áreas sem texto por cima.
- **Forte** (`--ho-gradient-strong`): marinho → azul elétrico → violeta. Para fundos com texto ou ícone branco por cima.

No nome, "Estadia" vai em marinho e "Flow" no degradê do azul elétrico ao violeta (em fundo escuro: branco e ciano).

Na interface, os tokens ficam em `apps/web/src/styles/variables.css`. Todas as combinações de texto foram conferidas para contraste mínimo de 4,5:1.

## Tipografia

- Nome: Sora 700, entreletras de −0,035 em.
- Slogan: Inter 500.

Nos arquivos SVG e PNG o texto está convertido em curvas, então eles não dependem de fonte instalada. No painel, Sora e Inter são servidas pelo próprio aplicativo (`@fontsource`), sem requisições a terceiros.

## Arquivos

### Para usar fora do sistema — `apps/web/public/brand/`

| Arquivo | Quando usar |
|---|---|
| `logo-horizontal.svg` | Assinatura padrão. |
| `logo-horizontal-tagline.svg` | Assinatura com slogan: apresentações, site, capa de documentos. |
| `logo-vertical.svg` | Espaços quadrados ou estreitos. |
| `symbol.svg` | Só o símbolo, a partir de 40 px. |
| `symbol-reduced.svg` | Só casa e check, abaixo de 40 px. |
| `app-icon.svg` | Ícone de aplicativo com fundo em degradê. |
| `png/` | As mesmas assinaturas em PNG com fundo transparente (1200 px de largura; vertical em 800 px) e o símbolo em 512 px. |

Cada SVG tem três versões: colorida (sem sufixo, para fundos claros), `-navy` (uma cor, para impressão em uma tinta) e `-white` (para fundos escuros: branco com o check em ciano).

### Usados pelo aplicativo web

| Arquivo | Função |
|---|---|
| `apps/web/src/app/icon.svg` | Favicon em navegadores atuais (versão reduzida). |
| `apps/web/src/app/favicon.ico` | Favicon em 16, 32 e 48 px. |
| `apps/web/src/app/apple-icon.png` | Ícone de 180 px para a tela inicial do iPhone e do iPad. |
| `apps/web/src/app/opengraph-image.png` | Imagem de 1200×630 exibida ao compartilhar o link. |
| `apps/web/src/app/manifest.ts` | Manifesto de instalação (nome, cores e ícones). |
| `apps/web/public/icons/icon-192.png`, `icon-512.png` | Ícones de instalação no Android e no computador. |
| `apps/web/public/icons/icon-maskable-192.png`, `icon-maskable-512.png` | Ícones com margem de segurança, que o Android recorta no formato do aparelho. |

O Next.js publica `icon.svg`, `favicon.ico`, `apple-icon.png`, `opengraph-image.png` e o manifesto automaticamente, pela convenção de nomes em `src/app`. A imagem de compartilhamento usa `WEB_URL` para montar o endereço absoluto; em produção, essa variável precisa estar definida no build do painel (o `docker-compose.yml` já repassa).

### No código

`apps/web/src/components/brand/Logo.tsx` exporta:

- `LogoMark`: só o símbolo. Propriedades: `size`, `variant` (`color` para fundo claro, `white` para fundo escuro, `navy` em uma cor) e `reduced`.
- `Logo`: símbolo e nome. Propriedades: `size`, `variant`, `layout` (`horizontal`, `vertical`) e `tagline`. Abaixo de 40 px, usa a versão reduzida do símbolo.

O menu lateral (versão `white`), a tela de login e a tela de carregamento usam esse componente.

## Regras de uso

- Deixe em volta do logo uma margem livre de pelo menos a largura do check.
- Tamanho mínimo: 24 px de altura para a assinatura horizontal; 16 px para o símbolo reduzido.
- Sobre foto ou fundo colorido, use a versão `-white`.
- Não distorça, não troque as cores do degradê e não redesenhe o símbolo à mão: gere de novo pelo script.

## Como regenerar

Todos os arquivos saem de `scripts/build-brand.py`, que é a fonte única do desenho.

```bash
pip install fonttools pillow            # e o pacote librsvg2-bin (rsvg-convert)
npm pack @fontsource/sora @fontsource/inter   # para obter os arquivos .woff
python3 scripts/build-brand.py \
  --sora-bold caminho/sora-latin-700-normal.woff \
  --inter-medium caminho/inter-latin-500-normal.woff
```

Se o desenho mudar no script, replique as mesmas curvas em `Logo.tsx` (as constantes `ROOF`, `BASE`, `TAIL` e `CHECK`, e as versões `_REDUCED`).

## Pendências

- Registro de marca: não foi feita busca de anterioridade. Antes de usar comercialmente, verifique no INPI se nome e símbolo estão livres.
- Foto de perfil do WhatsApp Business: use `png/symbol-512.png` sobre fundo branco ou `icons/icon-512.png`.
