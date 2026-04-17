# ERP Interno — Marmoraria Carinhato (Plano V1)

## 1) Perfis de acesso e permissões (RBAC)

### Perfis base
- **ADMIN_MASTER (Patrões):** acesso total, gestão de usuários, permissões, parâmetros e auditoria.
- **ENCARREGADO:** gestão de requisições, ordens de produção e consumo de materiais.
- **VENDEDOR:** pedidos/vendas, consulta de estoque, acompanhamento de status de produção/entrega.
- **RH:** cadastro de colaboradores, documentos internos, permissões não financeiras.
- **PRODUCAO:** ordens de produção, apontamentos e baixa de consumo de materiais.

### Regra de permissão
Cada usuário terá permissões por módulo + ação:
- `VIEW` (visualizar)
- `CREATE` (criar)
- `EDIT` (editar)
- `DELETE` (excluir)
- `APPROVE` (aprovar)
- `EXPORT` (exportar)

Acesso final = união de permissões dos perfis + permissões extras diretas no usuário.

---

## 2) Mapa de telas (menu) por módulo

1. **Dashboard**
   - KPIs: estoque crítico, requisições pendentes, contas a pagar vencendo, ordens em atraso.
2. **Cadastros**
   - Materiais, categorias, unidades, fornecedores, clientes, colaboradores.
3. **Estoque**
   - Saldo atual, movimentações, inventário, ajustes, estoque mínimo.
4. **Compras/Requisições**
   - Requisição interna, aprovação, pedido de compra, recebimento.
5. **Notas Fiscais**
   - Entrada (compra) e saída (venda), anexos XML/PDF.
6. **Produção**
   - Ordens de produção, consumo de materiais, status (aberta, em produção, concluída).
7. **Financeiro**
   - Contas a pagar, contas a receber (opcional V1), baixa de pagamento, débitos.
8. **Administração**
   - Usuários, perfis, permissões, parâmetros, trilha de auditoria.

---

## 3) Modelo de dados (entidades principais)

### Núcleo de segurança
- `usuarios`
- `perfis`
- `permissoes`
- `perfil_permissao`
- `usuario_perfil`
- `usuario_permissao`
- `auditoria_logs`

### Núcleo operacional
- `materiais`, `categorias_materiais`, `unidades_medida`
- `estoque_saldos`, `estoque_movimentacoes`
- `fornecedores`, `clientes`
- `requisicoes`, `requisicao_itens`
- `pedidos_compra`, `pedido_compra_itens`
- `notas_fiscais`, `nota_itens`
- `ordens_producao`, `ordem_producao_itens`
- `contas_pagar`, `pagamentos`

---

## 4) Esquema SQL inicial (PostgreSQL)

```sql
-- PERFIS E USUÁRIOS
CREATE TABLE perfis (
  id BIGSERIAL PRIMARY KEY,
  nome VARCHAR(60) UNIQUE NOT NULL,
  descricao TEXT,
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE usuarios (
  id BIGSERIAL PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  senha_hash TEXT NOT NULL,
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  ultimo_login_em TIMESTAMP,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE permissoes (
  id BIGSERIAL PRIMARY KEY,
  modulo VARCHAR(60) NOT NULL,
  acao VARCHAR(20) NOT NULL,
  codigo VARCHAR(120) UNIQUE NOT NULL,
  descricao TEXT,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE usuario_perfil (
  usuario_id BIGINT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  perfil_id BIGINT NOT NULL REFERENCES perfis(id) ON DELETE CASCADE,
  PRIMARY KEY (usuario_id, perfil_id)
);

CREATE TABLE perfil_permissao (
  perfil_id BIGINT NOT NULL REFERENCES perfis(id) ON DELETE CASCADE,
  permissao_id BIGINT NOT NULL REFERENCES permissoes(id) ON DELETE CASCADE,
  PRIMARY KEY (perfil_id, permissao_id)
);

CREATE TABLE usuario_permissao (
  usuario_id BIGINT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  permissao_id BIGINT NOT NULL REFERENCES permissoes(id) ON DELETE CASCADE,
  permitido BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (usuario_id, permissao_id)
);

-- CADASTROS
CREATE TABLE categorias_materiais (
  id BIGSERIAL PRIMARY KEY,
  nome VARCHAR(80) UNIQUE NOT NULL,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE unidades_medida (
  id BIGSERIAL PRIMARY KEY,
  sigla VARCHAR(10) UNIQUE NOT NULL,
  descricao VARCHAR(60) NOT NULL
);

CREATE TABLE materiais (
  id BIGSERIAL PRIMARY KEY,
  codigo VARCHAR(40) UNIQUE NOT NULL,
  descricao VARCHAR(180) NOT NULL,
  categoria_id BIGINT REFERENCES categorias_materiais(id),
  unidade_id BIGINT REFERENCES unidades_medida(id),
  estoque_minimo NUMERIC(14,3) NOT NULL DEFAULT 0,
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE fornecedores (
  id BIGSERIAL PRIMARY KEY,
  razao_social VARCHAR(180) NOT NULL,
  cnpj VARCHAR(20) UNIQUE,
  telefone VARCHAR(30),
  email VARCHAR(120),
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE clientes (
  id BIGSERIAL PRIMARY KEY,
  nome VARCHAR(180) NOT NULL,
  documento VARCHAR(20),
  telefone VARCHAR(30),
  email VARCHAR(120),
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ESTOQUE
CREATE TABLE estoque_saldos (
  material_id BIGINT PRIMARY KEY REFERENCES materiais(id) ON DELETE CASCADE,
  quantidade_atual NUMERIC(14,3) NOT NULL DEFAULT 0,
  atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE estoque_movimentacoes (
  id BIGSERIAL PRIMARY KEY,
  material_id BIGINT NOT NULL REFERENCES materiais(id),
  tipo VARCHAR(20) NOT NULL, -- ENTRADA, SAIDA, AJUSTE
  quantidade NUMERIC(14,3) NOT NULL,
  custo_unitario NUMERIC(14,2),
  referencia_tipo VARCHAR(40), -- NOTA, REQUISICAO, PRODUCAO, AJUSTE
  referencia_id BIGINT,
  observacao TEXT,
  usuario_id BIGINT REFERENCES usuarios(id),
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

-- REQUISIÇÕES E COMPRAS
CREATE TABLE requisicoes (
  id BIGSERIAL PRIMARY KEY,
  numero VARCHAR(30) UNIQUE NOT NULL,
  solicitante_id BIGINT REFERENCES usuarios(id),
  status VARCHAR(20) NOT NULL, -- ABERTA, APROVADA, REJEITADA, ATENDIDA
  observacao TEXT,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
  aprovado_em TIMESTAMP
);

CREATE TABLE requisicao_itens (
  id BIGSERIAL PRIMARY KEY,
  requisicao_id BIGINT NOT NULL REFERENCES requisicoes(id) ON DELETE CASCADE,
  material_id BIGINT NOT NULL REFERENCES materiais(id),
  quantidade NUMERIC(14,3) NOT NULL,
  observacao TEXT
);

CREATE TABLE pedidos_compra (
  id BIGSERIAL PRIMARY KEY,
  numero VARCHAR(30) UNIQUE NOT NULL,
  fornecedor_id BIGINT NOT NULL REFERENCES fornecedores(id),
  requisicao_id BIGINT REFERENCES requisicoes(id),
  status VARCHAR(20) NOT NULL, -- ABERTO, PARCIAL, RECEBIDO, CANCELADO
  valor_total NUMERIC(14,2) NOT NULL DEFAULT 0,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE pedido_compra_itens (
  id BIGSERIAL PRIMARY KEY,
  pedido_id BIGINT NOT NULL REFERENCES pedidos_compra(id) ON DELETE CASCADE,
  material_id BIGINT NOT NULL REFERENCES materiais(id),
  quantidade NUMERIC(14,3) NOT NULL,
  valor_unitario NUMERIC(14,2) NOT NULL,
  quantidade_recebida NUMERIC(14,3) NOT NULL DEFAULT 0
);

-- NOTAS FISCAIS
CREATE TABLE notas_fiscais (
  id BIGSERIAL PRIMARY KEY,
  tipo VARCHAR(10) NOT NULL, -- ENTRADA, SAIDA
  numero VARCHAR(50) NOT NULL,
  serie VARCHAR(20),
  emissao_em DATE,
  fornecedor_id BIGINT REFERENCES fornecedores(id),
  cliente_id BIGINT REFERENCES clientes(id),
  valor_total NUMERIC(14,2) NOT NULL DEFAULT 0,
  xml_url TEXT,
  pdf_url TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'LANCADA',
  criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
  UNIQUE (tipo, numero, serie)
);

CREATE TABLE nota_itens (
  id BIGSERIAL PRIMARY KEY,
  nota_id BIGINT NOT NULL REFERENCES notas_fiscais(id) ON DELETE CASCADE,
  material_id BIGINT REFERENCES materiais(id),
  descricao_item VARCHAR(180),
  quantidade NUMERIC(14,3) NOT NULL,
  valor_unitario NUMERIC(14,2) NOT NULL
);

-- PRODUÇÃO
CREATE TABLE ordens_producao (
  id BIGSERIAL PRIMARY KEY,
  codigo VARCHAR(40) UNIQUE NOT NULL,
  cliente_id BIGINT REFERENCES clientes(id),
  vendedor_id BIGINT REFERENCES usuarios(id),
  responsavel_id BIGINT REFERENCES usuarios(id),
  status VARCHAR(20) NOT NULL, -- ABERTA, EM_PRODUCAO, CONCLUIDA, ENTREGUE
  previsao_entrega DATE,
  observacao TEXT,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE ordem_producao_itens (
  id BIGSERIAL PRIMARY KEY,
  ordem_id BIGINT NOT NULL REFERENCES ordens_producao(id) ON DELETE CASCADE,
  material_id BIGINT REFERENCES materiais(id),
  descricao VARCHAR(180) NOT NULL,
  quantidade_prevista NUMERIC(14,3),
  quantidade_consumida NUMERIC(14,3) NOT NULL DEFAULT 0
);

-- FINANCEIRO
CREATE TABLE contas_pagar (
  id BIGSERIAL PRIMARY KEY,
  fornecedor_id BIGINT REFERENCES fornecedores(id),
  nota_id BIGINT REFERENCES notas_fiscais(id),
  descricao VARCHAR(180) NOT NULL,
  valor NUMERIC(14,2) NOT NULL,
  vencimento DATE NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'ABERTO', -- ABERTO, PAGO, VENCIDO
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE pagamentos (
  id BIGSERIAL PRIMARY KEY,
  conta_pagar_id BIGINT NOT NULL REFERENCES contas_pagar(id) ON DELETE CASCADE,
  valor_pago NUMERIC(14,2) NOT NULL,
  pago_em DATE NOT NULL,
  forma_pagamento VARCHAR(30),
  observacao TEXT,
  registrado_por BIGINT REFERENCES usuarios(id),
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

-- AUDITORIA
CREATE TABLE auditoria_logs (
  id BIGSERIAL PRIMARY KEY,
  usuario_id BIGINT REFERENCES usuarios(id),
  modulo VARCHAR(60) NOT NULL,
  acao VARCHAR(30) NOT NULL,
  entidade VARCHAR(80) NOT NULL,
  entidade_id BIGINT,
  payload JSONB,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## 5) Matriz de permissão inicial (resumo)

| Módulo | Admin Master | Encarregado | Vendedor | RH | Produção |
|---|---|---|---|---|---|
| Dashboard | VIEW | VIEW | VIEW | VIEW | VIEW |
| Cadastros | CRUD+APPROVE | VIEW/EDIT limitado | VIEW clientes | RH colaboradores | VIEW materiais |
| Estoque | CRUD+APPROVE | VIEW/CREATE/EDIT | VIEW | VIEW | VIEW/CREATE (consumo) |
| Requisições/Compras | CRUD+APPROVE | CREATE/APPROVE | VIEW | VIEW | CREATE |
| Notas | CRUD+APPROVE | VIEW | VIEW saída | VIEW | VIEW |
| Produção | CRUD+APPROVE | CRUD+APPROVE | VIEW | VIEW | CREATE/EDIT |
| Financeiro | CRUD+APPROVE | VIEW | VIEW limitado | sem acesso | sem acesso |
| Administração | TOTAL | sem acesso | sem acesso | sem acesso | sem acesso |

> Observação: no sistema real, o ADMIN_MASTER poderá ajustar cada permissão por usuário.

---

## 6) Backlog V1 (ordem de execução)

1. **Sprint 1 — Fundação**
   - Autenticação, usuários, perfis, permissões, layout base, auditoria.
2. **Sprint 2 — Cadastros + Estoque**
   - Materiais, fornecedores, saldos, movimentações e alertas de mínimo.
3. **Sprint 3 — Requisições + Compras**
   - Fluxo de solicitação, aprovação e pedidos de compra.
4. **Sprint 4 — Notas + Financeiro (Contas a pagar)**
   - Entrada de nota, vínculo com pedido, geração de contas a pagar e baixa.
5. **Sprint 5 — Produção + Dashboard executivo**
   - Ordem de produção, consumo e painéis de gestão.

---

## 7) Critérios de sucesso do MVP

- Permissões por cargo e por usuário funcionando.
- Rastreabilidade completa de movimentações de estoque.
- Fluxo de requisição -> compra -> nota -> pagamento fechado.
- Visão de pendências e indicadores principais em dashboard.
- Histórico de auditoria para ações críticas.

