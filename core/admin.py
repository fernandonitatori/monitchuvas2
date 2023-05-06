from django.contrib import admin
from .models import Fornecedor, Parametro, Local, Linguagem, Projeto,\
                    TipoLocacao, Tipo_Status, Status, Memorial, \
                    Periodo, Acao, Locacao_Acao, TRP, CatFornecedor,\
                    EndFornecedor, ContFornecedor, Compras_Locacao, \
                    Orcamento, Licitacao, Aprovacao, Sede, Cronograma,\
                    TipoPagto, Pagamento, Contrato_Locacao, \
                    Aquisicao_Acao, Manutencao_Acao, Compras_Manutencao,\
                    Compras_Aquisicao


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'site', 'observacoes', ]


@admin.register(Parametro)
class ParametroAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'valor', 'observacoes', ]


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ['descricao', ]


@admin.register(Linguagem)
class LinguagemAdmin(admin.ModelAdmin):
    list_display = ['descricao', ]


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['descricao', ]


@admin.register(TipoLocacao)
class TipoLocacaoAdmin(admin.ModelAdmin):
    list_display = ['descricao', ]


@admin.register(Tipo_Status)
class Tipo_StatusAdmin(admin.ModelAdmin):
    list_display = ['descricao', ]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'tipo_status', ]


@admin.register(Memorial)
class MemorialAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'data_memorial', ]


@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ['etapa', 'data_inicio', 'data_termino', 'locacao_acao', ]


@admin.register(Acao)
class AcaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'observacoes', 'data_base',
                    'projeto', 'linguagem', 'local', ]


@admin.register(Locacao_Acao)
class Locacao_AcaoAdmin(admin.ModelAdmin):
    list_display = ['tipo_locacao', 'acao', 'memorial',
                    'status', 'status_geral', 'data_cadastro', ]


@admin.register(Aquisicao_Acao)
class Aquisicao_AcaoAdmin(admin.ModelAdmin):
    list_display = ['memorial', 'status', 'data_cadastro', 'status_geral', ]


@admin.register(Manutencao_Acao)
class Manutencao_AcaoAdmin(admin.ModelAdmin):
    list_display = ['memorial', 'status', 'status_geral', 'data_cadastro', ]


@admin.register(TRP)
class TRPAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', ]


@admin.register(CatFornecedor)
class CatFornecedorAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', ]


@admin.register(EndFornecedor)
class EndFornecedorAdmin(admin.ModelAdmin):
    list_display = ['id', 'logradouro', 'numero', ]


@admin.register(ContFornecedor)
class ContFornecedorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'telefone', 'email', ]


@admin.register(Compras_Locacao)
class Compras_LocacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'status', ]


@admin.register(Compras_Aquisicao)
class Compras_AquisicaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'status', ]


@admin.register(Compras_Manutencao)
class Compras_ManutencaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'status', ]


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'valor', ]


@admin.register(Licitacao)
class LicitacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'dataabertura', 'datapregao',
                    'dataassinatura', 'datahomologacao', 'vencedor', 'valor', ]


@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ['id', 'dataminuta', 'datadca', 'licitacao',
                    'locacao', 'status', ]


@admin.register(Aprovacao)
class AprovacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'setor', 'sede', ]


@admin.register(Cronograma)
class CronogramaAdmin(admin.ModelAdmin):
    list_display = ['id', 'locacao', 'datainicio', 'datafim',
                    'anotacoes', 'status', ]


@admin.register(TipoPagto)
class TipoPagtoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', ]


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_pagto', 'valor', 'anotacoes', ]


@admin.register(Contrato_Locacao)
class Contrato_LocacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'processo', 'dataprocesso', 'datacontrato',
                    'valorlocacao', 'status', ]
