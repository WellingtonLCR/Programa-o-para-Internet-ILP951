BEGIN;

INSERT INTO perfis (nome, descricao)
VALUES
  ('ADMIN_MASTER', 'Acesso total do sistema e configuracoes globais'),
  ('ENCARREGADO', 'Responsavel por requisicoes e operacao de producao'),
  ('VENDEDOR', 'Gestao de pedidos e consulta operacional'),
  ('RH', 'Gestao de colaboradores e processos de RH'),
  ('PRODUCAO', 'Execucao de ordens e consumo de materiais')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO permissoes (modulo, acao, codigo, descricao)
VALUES
  ('ESTOQUE', 'VIEW', 'estoque.view', 'Visualizar estoque e saldos'),
  ('ESTOQUE', 'CREATE', 'estoque.create', 'Criar movimentacoes e materiais'),
  ('ESTOQUE', 'EDIT', 'estoque.edit', 'Editar materiais e ajustes'),
  ('ESTOQUE', 'APPROVE', 'estoque.approve', 'Aprovar ajustes relevantes'),

  ('REQUISICAO', 'VIEW', 'requisicao.view', 'Visualizar requisicoes'),
  ('REQUISICAO', 'CREATE', 'requisicao.create', 'Criar requisicoes internas'),
  ('REQUISICAO', 'APPROVE', 'requisicao.approve', 'Aprovar requisicoes'),

  ('FINANCEIRO', 'VIEW', 'financeiro.view', 'Visualizar contas a pagar'),
  ('FINANCEIRO', 'CREATE', 'financeiro.create', 'Criar contas e lancamentos'),
  ('FINANCEIRO', 'APPROVE', 'financeiro.approve', 'Aprovar pagamentos'),

  ('ADMIN', 'VIEW', 'admin.view', 'Visualizar administracao'),
  ('ADMIN', 'CREATE', 'admin.create', 'Criar usuarios/perfis'),
  ('ADMIN', 'EDIT', 'admin.edit', 'Editar configuracoes administrativas'),
  ('ADMIN', 'DELETE', 'admin.delete', 'Remover usuarios/perfis'),
  ('ADMIN', 'APPROVE', 'admin.approve', 'Aprovar alteracoes criticas')
ON CONFLICT (codigo) DO NOTHING;

WITH perfil_admin AS (
  SELECT id FROM perfis WHERE nome = 'ADMIN_MASTER'
), todas_permissoes AS (
  SELECT id FROM permissoes
)
INSERT INTO perfil_permissao (perfil_id, permissao_id)
SELECT perfil_admin.id, todas_permissoes.id
FROM perfil_admin, todas_permissoes
ON CONFLICT DO NOTHING;

WITH perfil_encarregado AS (
  SELECT id FROM perfis WHERE nome = 'ENCARREGADO'
), permissoes_encarregado AS (
  SELECT id FROM permissoes WHERE codigo IN (
    'estoque.view', 'estoque.create', 'estoque.edit',
    'requisicao.view', 'requisicao.create', 'requisicao.approve',
    'financeiro.view'
  )
)
INSERT INTO perfil_permissao (perfil_id, permissao_id)
SELECT perfil_encarregado.id, permissoes_encarregado.id
FROM perfil_encarregado, permissoes_encarregado
ON CONFLICT DO NOTHING;

WITH perfil_vendedor AS (
  SELECT id FROM perfis WHERE nome = 'VENDEDOR'
), permissoes_vendedor AS (
  SELECT id FROM permissoes WHERE codigo IN (
    'estoque.view',
    'requisicao.view', 'requisicao.create',
    'financeiro.view'
  )
)
INSERT INTO perfil_permissao (perfil_id, permissao_id)
SELECT perfil_vendedor.id, permissoes_vendedor.id
FROM perfil_vendedor, permissoes_vendedor
ON CONFLICT DO NOTHING;

WITH perfil_rh AS (
  SELECT id FROM perfis WHERE nome = 'RH'
), permissoes_rh AS (
  SELECT id FROM permissoes WHERE codigo IN ('admin.view')
)
INSERT INTO perfil_permissao (perfil_id, permissao_id)
SELECT perfil_rh.id, permissoes_rh.id
FROM perfil_rh, permissoes_rh
ON CONFLICT DO NOTHING;

WITH perfil_producao AS (
  SELECT id FROM perfis WHERE nome = 'PRODUCAO'
), permissoes_producao AS (
  SELECT id FROM permissoes WHERE codigo IN (
    'estoque.view', 'estoque.create',
    'requisicao.view', 'requisicao.create'
  )
)
INSERT INTO perfil_permissao (perfil_id, permissao_id)
SELECT perfil_producao.id, permissoes_producao.id
FROM perfil_producao, permissoes_producao
ON CONFLICT DO NOTHING;

COMMIT;
