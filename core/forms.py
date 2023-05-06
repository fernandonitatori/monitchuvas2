from django import forms
from core.models import Acao, Locacao_Acao, TipoLocacao, Memorial,\
                        Compras_Locacao,\
                        Sede, Contrato_Locacao, Pagamento,\
                        Cronograma, Projeto, Aquisicao_Acao, Manutencao_Acao,\
                        Compras_Aquisicao, Compras_Manutencao, \
                        Sede_Aquisicao, Sede_Manutencao, Contrato_Aquisicao,\
                        Contrato_Manutencao, Pagamento_Aquisicao, \
                        Pagamento_Manutencao, Cronograma_Aquisicao,\
                        Cronograma_Manutencao


class LocacaoAcaoModelForm(forms.ModelForm):

    class Meta:
        model = Locacao_Acao
        fields = ['tipo_locacao', 'acao', 'memorial',
                  'prazo', 'data_cadastro', 'status', 'status_geral']


class AquisicaoAcaoModelForm(forms.ModelForm):

    class Meta:
        model = Aquisicao_Acao
        fields = ['memorial', 'prazo', 'data_cadastro',
                  'status', 'status_geral']


class ManutencaoAcaoModelForm(forms.ModelForm):

    class Meta:
        model = Manutencao_Acao
        fields = ['memorial', 'prazo', 'data_cadastro',
                  'status', 'status_geral']


class AcaoModelForm(forms.ModelForm):

    class Meta:
        model = Acao
        fields = ['nome', 'descricao', 'observacoes', 'data_base',
                  'projeto', 'linguagem', 'local']


class TipoLocacaoModelForm(forms.ModelForm):

    class Meta:
        model = TipoLocacao
        fields = ['descricao']


class ProjetoModelForm(forms.ModelForm):

    class Meta:
        model = Projeto
        fields = ['descricao']


class MemorialModelForm(forms.ModelForm):

    class Meta:
        model = Memorial
        fields = ['descricao', 'data_memorial']


class ComprasLocacaoModelForm(forms.ModelForm):

    class Meta:
        model = Compras_Locacao
        fields = ['descricao', 'numero', 'data', 'observacoes',
                  'locacao', 'trp', 'prazo', 'status', 'sede']


class ComprasAquisicaoModelForm(forms.ModelForm):

    class Meta:
        model = Compras_Aquisicao
        fields = ['descricao', 'numero', 'data', 'observacoes',
                  'aquisicao', 'trp', 'prazo', 'status', 'sede']


class ComprasManutencaoModelForm(forms.ModelForm):

    class Meta:
        model = Compras_Manutencao
        fields = ['descricao', 'numero', 'data', 'observacoes',
                  'manutencao', 'trp', 'prazo', 'status', 'sede']


class SedeModelForm(forms.ModelForm):

    class Meta:
        model = Sede
        fields = ['descricao', 'numero', 'dataminuta', 'datadca',
                  'anotacoes', 'licitacao', 'locacao', 'prazo', 'status']


class SedeAquisicaoModelForm(forms.ModelForm):

    class Meta:
        model = Sede_Aquisicao
        fields = ['descricao', 'numero', 'dataminuta', 'datadca',
                  'anotacoes', 'licitacao', 'aquisicao', 'prazo', 'status']


class SedeManutencaoModelForm(forms.ModelForm):

    class Meta:
        model = Sede_Manutencao
        fields = ['descricao', 'numero', 'dataminuta', 'datadca',
                  'anotacoes', 'licitacao', 'manutencao', 'prazo', 'status']


class ContratoLocacaoModelForm(forms.ModelForm):

    class Meta:
        model = Contrato_Locacao
        fields = ['descricao', 'processo', 'dataprocesso',
                  'instrcontratual', 'datacontrato', 'valorservico',
                  'valorlocacao', 'locacao', 'prazo', 'status']


class ContratoAquisicaoModelForm(forms.ModelForm):

    class Meta:
        model = Contrato_Aquisicao
        fields = ['descricao', 'processo', 'dataprocesso',
                  'instrcontratual', 'datacontrato', 'valorservico',
                  'valorlocacao', 'aquisicao', 'prazo', 'status']


class ContratoManutencaoModelForm(forms.ModelForm):

    class Meta:
        model = Contrato_Manutencao
        fields = ['descricao', 'processo', 'dataprocesso',
                  'instrcontratual', 'datacontrato', 'valorservico',
                  'valorlocacao', 'manutencao', 'prazo', 'status']


class PagamentoModelForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['descricao', 'tipo_pagto', 'atividade', 'parcela',
                  'qtde_parcelas', 'valor', 'dataprevnota',
                  'tiponota', 'numnota', 'dataemissnota', 'serienota', 'xml',
                  'anotacoes', 'locacao', 'prazo', 'status']


class PagamentoAquisicaoModelForm(forms.ModelForm):
    class Meta:
        model = Pagamento_Aquisicao
        fields = ['descricao', 'tipo_pagto', 'atividade', 'parcela',
                  'qtde_parcelas', 'valor', 'dataprevnota',
                  'tiponota', 'numnota', 'dataemissnota', 'serienota',
                  'xml', 'anotacoes', 'aquisicao', 'prazo', 'status']


class PagamentoManutencaoModelForm(forms.ModelForm):
    class Meta:
        model = Pagamento_Manutencao
        fields = ['descricao', 'tipo_pagto', 'atividade', 'parcela',
                  'qtde_parcelas', 'valor', 'dataprevnota',
                  'tiponota', 'numnota', 'dataemissnota', 'serienota', 'xml',
                  'anotacoes', 'manutencao', 'prazo', 'status']


class CronogramaModelForm(forms.ModelForm):

    class Meta:
        model = Cronograma
        fields = ['locacao', 'atividade', 'datainicio', 'datafim',
                  'anotacoes', 'prazo', 'status']


class CronogramaAquisicaoModelForm(forms.ModelForm):

    class Meta:
        model = Cronograma_Aquisicao
        fields = ['aquisicao', 'atividade', 'datainicio',
                  'datafim', 'anotacoes', 'prazo', 'status']


class CronogramaManutencaoModelForm(forms.ModelForm):

    class Meta:
        model = Cronograma_Manutencao
        fields = ['manutencao', 'atividade', 'datainicio',
                  'datafim', 'anotacoes', 'prazo', 'status']
