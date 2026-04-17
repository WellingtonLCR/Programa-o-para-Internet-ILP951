BEGIN;

CREATE TABLE IF NOT EXISTS categorias_materiais (
  id BIGSERIAL PRIMARY KEY,
  nome VARCHAR(80) UNIQUE NOT NULL,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS unidades_medida (
  id BIGSERIAL PRIMARY KEY,
  sigla VARCHAR(10) UNIQUE NOT NULL,
  descricao VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS materiais (
  id BIGSERIAL PRIMARY KEY,
  codigo VARCHAR(40) UNIQUE NOT NULL,
  descricao VARCHAR(180) NOT NULL,
  categoria_id BIGINT REFERENCES categorias_materiais(id),
  unidade_id BIGINT REFERENCES unidades_medida(id),
  estoque_minimo NUMERIC(14,3) NOT NULL DEFAULT 0,
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS fornecedores (
  id BIGSERIAL PRIMARY KEY,
  razao_social VARCHAR(180) NOT NULL,
  cnpj VARCHAR(20) UNIQUE,
  telefone VARCHAR(30),
  email VARCHAR(120),
  ativo BOOLEAN NOT NULL DEFAULT TRUE,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS estoque_saldos (
  material_id BIGINT PRIMARY KEY REFERENCES materiais(id) ON DELETE CASCADE,
  quantidade_atual NUMERIC(14,3) NOT NULL DEFAULT 0,
  atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS estoque_movimentacoes (
  id BIGSERIAL PRIMARY KEY,
  material_id BIGINT NOT NULL REFERENCES materiais(id),
  tipo VARCHAR(20) NOT NULL,
  quantidade NUMERIC(14,3) NOT NULL,
  custo_unitario NUMERIC(14,2),
  referencia_tipo VARCHAR(40),
  referencia_id BIGINT,
  observacao TEXT,
  usuario_id BIGINT REFERENCES usuarios(id),
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS requisicoes (
  id BIGSERIAL PRIMARY KEY,
  numero VARCHAR(30) UNIQUE NOT NULL,
  solicitante_id BIGINT REFERENCES usuarios(id),
  status VARCHAR(20) NOT NULL,
  observacao TEXT,
  criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
  aprovado_em TIMESTAMP
);

CREATE TABLE IF NOT EXISTS requisicao_itens (
  id BIGSERIAL PRIMARY KEY,
  requisicao_id BIGINT NOT NULL REFERENCES requisicoes(id) ON DELETE CASCADE,
  material_id BIGINT NOT NULL REFERENCES materiais(id),
  quantidade NUMERIC(14,3) NOT NULL,
  observacao TEXT
);

CREATE TABLE IF NOT EXISTS contas_pagar (
  id BIGSERIAL PRIMARY KEY,
  fornecedor_id BIGINT REFERENCES fornecedores(id),
  descricao VARCHAR(180) NOT NULL,
  valor NUMERIC(14,2) NOT NULL,
  vencimento DATE NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'ABERTO',
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pagamentos (
  id BIGSERIAL PRIMARY KEY,
  conta_pagar_id BIGINT NOT NULL REFERENCES contas_pagar(id) ON DELETE CASCADE,
  valor_pago NUMERIC(14,2) NOT NULL,
  pago_em DATE NOT NULL,
  forma_pagamento VARCHAR(30),
  observacao TEXT,
  registrado_por BIGINT REFERENCES usuarios(id),
  criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMIT;
