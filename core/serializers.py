from rest_framework import serializers

from .models import Locacao_Acao, TipoLocacao, Fornecedor, Local,\
                    Linguagem, Projeto, Acao, Status, \
                    Aquisicao_Acao, Manutencao_Acao


class Aquisicao_AcaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aquisicao_Acao
        fields = ('id', 'memorial', 'status',
                  'status_geral', 'descricao', 'data_cadastro',
                  'prazo', 'criado', 'modificado', 'ativo')
        depth = 1


class Manutencao_AcaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manutencao_Acao
        fields = ('id', 'memorial', 'status',
                  'status_geral', 'descricao', 'data_cadastro',
                  'prazo', 'criado', 'modificado', 'ativo')
        depth = 1


class TipoLocacao_AcaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoLocacao
        fields = ('id', 'descricao', 'criado', 'modificado', 'ativo')


class FornecedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fornecedor
        fields = ('id', 'nome', 'cnpj', 'observacoes', 'ativo')


class Local_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Local
        fields = ('id', 'descricao')


class Linguagem_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Linguagem
        fields = ('id', 'descricao')


class Projeto_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Projeto
        fields = ('id', 'descricao')


class AcaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Acao
        fields = ('id', 'nome', 'descricao', 'observacoes',
                  'data_base', 'projeto', 'linguagem', 'local')


class Acao_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Acao
        fields = ('id', 'nome', 'descricao', 'observacoes',
                  'data_base', 'projeto', 'linguagem',
                  'local')


class Status_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('id', 'tipo_status', 'descricao')


class Locacao_AcaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Locacao_Acao
        fields = ('id', 'tipo_locacao', 'acao', 'memorial', 'status',
                  'status_geral', 'descricao', 'data_cadastro',
                  'prazo', 'criado', 'modificado', 'ativo')
        depth = 1
