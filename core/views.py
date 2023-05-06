from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from datetime import date
from dateutil.relativedelta import relativedelta
from rest_framework import generics
from rest_framework import viewsets
from onesignal_sdk.client import Client
from .serializers import Locacao_AcaoSerializer,\
                         TipoLocacao_AcaoSerializer, FornecedorSerializer,\
                         Local_Serializer, Linguagem_Serializer, \
                         Projeto_Serializer, Acao_Serializer, \
                         Status_Serializer, Aquisicao_AcaoSerializer, \
                         Manutencao_AcaoSerializer

from .forms import TipoLocacaoModelForm, MemorialModelForm, \
                   ComprasLocacaoModelForm, LocacaoAcaoModelForm, \
                   SedeModelForm,  ContratoLocacaoModelForm, \
                   PagamentoModelForm, \
                   CronogramaModelForm, ProjetoModelForm,\
                   ComprasAquisicaoModelForm, ComprasManutencaoModelForm,  \
                   ManutencaoAcaoModelForm, SedeManutencaoModelForm,\
                   SedeAquisicaoModelForm, AquisicaoAcaoModelForm,\
                   ContratoAquisicaoModelForm, ContratoManutencaoModelForm, \
                   PagamentoAquisicaoModelForm, PagamentoManutencaoModelForm, \
                   CronogramaAquisicaoModelForm, CronogramaManutencaoModelForm

from .models import Locacao_Acao, Acao, TipoLocacao,\
                    Memorial, Compras_Locacao, \
                    TRP, Orcamento, Sede, Licitacao, \
                    Contrato_Locacao, Pagamento, \
                    Cronograma, Aprovacao,\
                    Fornecedor, CatFornecedor, EndFornecedor, \
                    ContFornecedor, Tipo_Status, Status,\
                    Local, Linguagem,\
                    Projeto, TipoPagto, Aquisicao_Acao, \
                    Manutencao_Acao, Compras_Aquisicao,\
                    Compras_Manutencao,\
                    Sede_Aquisicao, Sede_Manutencao, \
                    Contrato_Aquisicao, Contrato_Manutencao,\
                    Pagamento_Aquisicao, Pagamento_Manutencao, \
                    Cronograma_Aquisicao, Cronograma_Manutencao

from matplotlib import pyplot as plt

import matplotlib


# MatPlotLib
matplotlib.use('Agg')


# Pie Chart
def piechart(request):
    # Pie chart, where the slices will be ordered and plotted
    # counter-clockwise:
    labels = 'Locações', 'Aquisições', 'Manutenções'
    numlocacoes = Locacao_Acao.objects.count()
    numaquisicoes = Aquisicao_Acao.objects.count()
    nummanutencoes = Manutencao_Acao.objects.count()
    numsolicit = numlocacoes + numaquisicoes + nummanutencoes
    percentlocacoes = (numlocacoes/numsolicit) * 100
    percentaquisicoes = (numaquisicoes / numsolicit) * 100
    percentmanutencoes = (nummanutencoes / numsolicit) * 100
    sizes = [percentlocacoes, percentaquisicoes, percentmanutencoes]
    #  explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    plt.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.title('Solicitações por tipo')
    plt.savefig('static/img/grafico_solicitacoes.png', dpi=80)
    return render(request, 'piechart.html')


# APIViews da API V1
class LocacaoAPIView(generics.ListAPIView):
    queryset = Locacao_Acao.objects.all()
    serializer_class = Locacao_AcaoSerializer


class TipoLocacaoAPIView(generics.ListAPIView):
    queryset = TipoLocacao.objects.all()
    serializer_class = TipoLocacao_AcaoSerializer


class FornecedorAPIView(generics.ListAPIView):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer


# ViewSets da API V2
class LocacaoViewSet(viewsets.ModelViewSet):
    queryset = Locacao_Acao.objects.all().order_by('-data_cadastro')
    serializer_class = Locacao_AcaoSerializer


class AquisicaoViewSet(viewsets.ModelViewSet):
    queryset = Aquisicao_Acao.objects.all().order_by('-data_cadastro')
    serializer_class = Aquisicao_AcaoSerializer


class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao_Acao.objects.all().order_by('-data_cadastro')
    serializer_class = Manutencao_AcaoSerializer


class TipoLocacaoViewSet(viewsets.ModelViewSet):
    queryset = TipoLocacao.objects.all()
    serializer_class = TipoLocacao_AcaoSerializer


class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer


class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = Local_Serializer


class LinguagemViewSet(viewsets.ModelViewSet):
    queryset = Linguagem.objects.all()
    serializer_class = Linguagem_Serializer


class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = Projeto_Serializer


class AcaoViewSet(viewsets.ModelViewSet):
    queryset = Acao.objects.all()
    serializer_class = Acao_Serializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = Status_Serializer


# Listar Locações
class ListLocacaoAcaoView(ListView):
    model = Locacao_Acao
    template_name = 'locacao_acao_listview.html'
    queryset = Locacao_Acao.objects.all().order_by('-data_cadastro')
    context_object_name = 'locacoes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tiposlocacao'] = TipoLocacao.objects.all()
        context['acoes'] = Acao.objects.all()
        context['memoriais'] = Memorial.objects.all()
        context['statuses'] = Status.objects.all()
        return context


# Listar Aquisições
class ListAquisicaoAcaoView(ListView):
    model = Aquisicao_Acao
    template_name = 'aquisicao_acao_listview.html'
    queryset = Aquisicao_Acao.objects.all().order_by('-data_cadastro')
    context_object_name = 'aquisicoes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acoes'] = Acao.objects.all()
        context['memoriais'] = Memorial.objects.all()
        context['statuses'] = Status.objects.all()
        return context


# Listar Manutenções
class ListManutencaoAcaoView(ListView):
    model = Manutencao_Acao
    template_name = 'manutencao_acao_listview.html'
    queryset = Manutencao_Acao.objects.all().order_by('-data_cadastro')
    context_object_name = 'manutencoes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acoes'] = Acao.objects.all()
        context['memoriais'] = Memorial.objects.all()
        context['statuses'] = Status.objects.all()
        return context


# View do index
class IndexView(TemplateView):
    template_name = 'index.html'


# View da Central de Ajuda
class CentralAjudaView(TemplateView):
    template_name = 'central_de_ajuda.html'


# View das FAQs
class FaqsView(TemplateView):
    template_name = 'faqs_conteudo.html'


# View do Manual do Sistema
class ManualSistemaView(TemplateView):
    template_name = 'manual_conteudo.html'


# View da página inicial do sistema
class SistemaView(TemplateView):
    template_name = 'sistema.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        numlocacoes = Locacao_Acao.objects.count()
        numaquisicoes = Aquisicao_Acao.objects.count()
        nummanutencoes = Manutencao_Acao.objects.count()
        context['numsolicit'] = numlocacoes + numaquisicoes + nummanutencoes
        compras = Compras_Locacao.objects.all()
        countcompras = 0
        for compra in compras:
            if not str(compra.status) == 'Compras - Aprovado':
                countcompras += 1
                print(countcompras)

        sedes = Sede.objects.all()
        countsede = 0
        for sede in sedes:
            if not str(sede.status) == 'Sede - Aprovado':
                countsede += 1
                print(countsede)

        contratos = Contrato_Locacao.objects.all()
        countcontr = 0
        for contrato in contratos:
            if not str(contrato.status) == 'Contratação - Aprovado':
                countcontr += 1
                print(countcontr)

        pagtos = Pagamento.objects.all()
        countpagto = 0
        for pagto in pagtos:
            if not str(pagto.status) == 'Pagamento - Aprovado':
                countpagto += 1
                print(countpagto)

        cronos = Cronograma.objects.all()
        countcrono = 0
        for crono in cronos:
            if not str(crono.status) == 'Recebimento - Aprovado':
                countcrono += 1
                print(countcrono)

        countfin = 0
        locs = Locacao_Acao.objects.all()
        for loc in locs:
            if str(loc.status_geral) == 'Finalizado':
                countfin += 1

        context['numlocacoes'] = numlocacoes
        context['numaquisicoes'] = numaquisicoes
        context['nummanutencoes'] = nummanutencoes
        context['numcompras'] = countcompras
        context['numsede'] = countsede
        context['numcontr'] = countcontr
        context['numpagto'] = countpagto
        context['numrec'] = countcrono
        context['numfin'] = countfin

        return context


# View para criar solicitação de Locação
class CreateSolicitView(SuccessMessageMixin, CreateView):
    model = Locacao_Acao
    template_name = 'form_solicit_loc.html'
    fields = ['tipo_locacao', 'acao', 'memorial', 'prazo',
              'status', 'status_geral', 'data_cadastro', 'descricao']
    success_url = reverse_lazy('add_loc')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tiposlocacao'] = TipoLocacao.objects.all()
        context['acoes'] = Acao.objects.all()
        context['memoriais'] = Memorial.objects.all()
        context['statuses'] = Status.objects.all()
        context['projetos'] = Projeto.objects.all()
        context['linguagens'] = Linguagem.objects.all()
        context['locais'] = Local.objects.all()
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        client = Client(app_id='473c152c-7766-4691-9e44-9bbd0e67de05',
                        rest_api_key='OTEzYWU5ZTUtNGE5Mi00YWQ0L\
                        WJlOGEtMTZhNzhmYjc5MTE4')
        notification_body = {
            'contents': {'en': 'Nova Locação inserida no sistema \
                         - Veja detalhes no AcPro Mobile'},
            'included_segments': ['Subscribed Users'],
        }
        response = client.send_notification(notification_body)
        print(response.body)
        return "Solicitação cadastrada com sucesso!"


# View para Criar Solicitações de Aquisição
class CreateAquisicaoView(SuccessMessageMixin, CreateView):
    model = Aquisicao_Acao
    template_name = 'form_solicit_aquisicao.html'
    fields = ['memorial', 'prazo', 'status',
              'status_geral', 'descricao', 'data_cadastro']
    success_url = reverse_lazy('add_aquisicao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['tiposlocacao'] = TipoLocacao.objects.all()
        # context['acoes'] = Acao.objects.all()
        context['memoriais'] = Memorial.objects.all()
        context['statuses'] = Status.objects.all()
        context['projetos'] = Projeto.objects.all()
        context['linguagens'] = Linguagem.objects.all()
        context['locais'] = Local.objects.all()
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        client = Client(app_id='473c152c-7766-4691-9e44-9bbd0e67de05',
                        rest_api_key='OTEzYWU5ZTUtNGE5Mi00YWQ0LWJlOGE\
                        tMTZhNzhmYjc5MTE4')
        notification_body = {
            'contents': {'en': 'Nova Aquisição inserida no sistema \
                          - Veja detalhes no AcPro Mobile'},
            'included_segments': ['Subscribed Users'],
        }
        response = client.send_notification(notification_body)
        print(response.body)
        return "Solicitação cadastrada com sucesso!"


# View para Criar Solicitações de Manutenção
class CreateManutencaoView(SuccessMessageMixin, CreateView):
    model = Manutencao_Acao
    template_name = 'form_solicit_manut.html'
    fields = ['memorial', 'prazo', 'status',
              'status_geral', 'descricao', 'data_cadastro']
    success_url = reverse_lazy('add_manut')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['tiposlocacao'] = TipoLocacao.objects.all()
        # context['acoes'] = Acao.objects.all()
        context['memoriais'] = Memorial.objects.all()
        context['statuses'] = Status.objects.all()
        context['projetos'] = Projeto.objects.all()
        context['linguagens'] = Linguagem.objects.all()
        context['locais'] = Local.objects.all()
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        client = Client(app_id='473c152c-7766-4691-9e44-9bbd0e67de05',
                        rest_api_key='OTEzYWU5ZTUtNGE5Mi00YWQ0LWJlOGE\
                        tMTZhNzhmYjc5MTE4')
        notification_body = {
            'contents': {'en': 'Nova Manutenção inserida no sistema \
                        - Veja detalhes no AcPro Mobile'},
            'included_segments': ['Subscribed Users'],
        }
        response = client.send_notification(notification_body)
        print(response.body)
        return "Solicitação cadastrada com sucesso!"


# View para consulta de Locações
class ConsultaLocacaoAcaoView(UpdateView):
    model = Locacao_Acao
    template_name = 'locacao_acao_consulta.html'
    fields = ['tipo_locacao', 'acao', 'memorial', 'prazo',
              'descricao', 'status', 'status_geral']
    context_object_name = 'consulta'
    success_url = reverse_lazy('sistema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_chave_sol'] = 'Solicitação - Concluída'
        context['tiposlocacao'] = TipoLocacao.objects.all()
        context['acoes'] = Acao.objects.all()
        context['memoriais'] = Memorial.objects.all()
        context['statuses'] = Status.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = LocacaoAcaoModelForm(request.POST)
        if form.is_valid():
            loc = self.kwargs.get("pk")
            print(loc)
            super(ConsultaLocacaoAcaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Solicitação '
                                      'atualizado com sucesso')
            client = Client(app_id='473c152c-7766-4691-9e44-9bbd0e67de05',
                            rest_api_key='OTEzYWU5ZTUtNGE5Mi00YWQ0L\
                                    WJlOGEtMTZhNzhmYjc5MTE4')
            notification_body = {
                'contents': {'en': 'Locação {} atualizada no sistema \
                            - Veja detalhes no AcPro Mobile'.format(loc)},
                'included_segments': ['Subscribed Users'],
            }
            response = client.send_notification(notification_body)
            print(response.body)
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[loc]))
        return render(request, 'resultado.html', {'form': form})


# View para consulta e atualização de Aquisições
class ConsultaAquisicaoAcaoView(UpdateView):
    model = Aquisicao_Acao
    template_name = 'aquisicao_acao_consulta.html'
    fields = ['memorial', 'prazo', 'descricao',
              'status', 'status_geral']
    context_object_name = 'consulta_aquis'
    success_url = reverse_lazy('sistema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_chave_sol'] = 'Solicitação - Concluída'
        # context['acoes'] = Acao.objects.all()
        context['memoriais'] = Memorial.objects.all()
        context['statuses'] = Status.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = AquisicaoAcaoModelForm(request.POST)
        if form.is_valid():
            aquis = self.kwargs.get("pk")
            print(aquis)

            super(ConsultaAquisicaoAcaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Aquisição '
                                      'atualizado com sucesso')
            client = Client(app_id='473c152c-7766-4691-9e44-9bbd0e67de05',
                            rest_api_key='OTEzYWU5ZTUtNGE5Mi00YWQ0L\
                                                WJlOGEtMTZhNzhmYjc5MTE4')
            notification_body = {
                'contents': {'en': 'Aquisição {} atualizada no sistema \
                            - Veja detalhes no AcPro Mobile'.format(aquis)},
                'included_segments': ['Subscribed Users'],
            }
            response = client.send_notification(notification_body)
            print(response.body)

            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquis]))
        return render(request, 'resultado.html', {'form': form})


# View para consulta de Manutenções
class ConsultaManutencaoAcaoView(UpdateView):
    model = Manutencao_Acao
    template_name = 'manutencao_acao_consulta.html'
    fields = ['memorial', 'prazo', 'descricao',
              'status', 'status_geral']
    context_object_name = 'consulta'
    success_url = reverse_lazy('sistema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_chave_sol'] = 'Solicitação - Concluída'
        # context['tiposlocacao'] = TipoLocacao.objects.all()
        # context['acoes'] = Acao.objects.all()
        context['memoriais'] = Memorial.objects.all()
        context['statuses'] = Status.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = ManutencaoAcaoModelForm(request.POST)
        if form.is_valid():
            manut = self.kwargs.get("pk")
            print(manut)
            super(ConsultaManutencaoAcaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo de Aquisição em'
                                      ' Solicitação atualizado com sucesso')
            client = Client(app_id='473c152c-7766-4691-9e44-9bbd0e67de05',
                            rest_api_key='OTEzYWU5ZTUtNGE5Mi00YWQ0L\
                                                WJlOGEtMTZhNzhmYjc5MTE4')
            notification_body = {
                'contents': {'en': 'Manutenção {} atualizada no sistema \
                            - Veja detalhes no AcPro Mobile'.format(manut)},
                'included_segments': ['Subscribed Users'],
            }
            response = client.send_notification(notification_body)
            print(response.body)

            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manut]))
        return render(request, 'resultado.html', {'form': form})


# View para update de Locações
class ListUpdLocacaoAcaoView(ListView):
    model = Locacao_Acao
    template_name = 'locacao_acao_updlistview.html'
    queryset = Locacao_Acao.objects.all()
    context_object_name = 'updlocacoes'


# View para update de Aquisicao
class ListUpdAquisicaoAcaoView(ListView):
    model = Aquisicao_Acao
    template_name = 'aquisicao_acao_updlistview.html'
    queryset = Aquisicao_Acao.objects.all()
    context_object_name = 'updaquisicoes'


# View para update de Aquisicao
class ListUpdManutencaoAcaoView(ListView):
    model = Manutencao_Acao
    template_name = 'manutencao_acao_updlistview.html'
    queryset = Manutencao_Acao.objects.all()
    context_object_name = 'updmanutencoes'


# View para criar Ação
class CreateAcaoView(SuccessMessageMixin, CreateView):
    model = Acao
    template_name = 'form_create_acao.html'
    fields = ['nome', 'descricao', 'observacoes',
              'data_base', 'projeto', 'linguagem', 'local']
    success_url = reverse_lazy('add_acao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acoes'] = Acao.objects.all()
        context['projetos'] = Projeto.objects.all()
        context['linguagens'] = Linguagem.objects.all()
        context['locais'] = Local.objects.all()
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Ação cadastrada com sucesso!"


# View para criar tipo de locação
class CreateTipoLocView(CreateView):
    model = TipoLocacao
    template_name = 'form_create_tipoloc.html'
    fields = ['descricao']
    success_url = reverse_lazy('sistema')


# View para criar Memorial
class CreateMemorialView(CreateView):
    model = Memorial
    template_name = 'form_create_memorial.html'
    fields = ['descricao', 'data_memorial']
    success_url = reverse_lazy('add_memorial')

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Memorial cadastrado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memoriais'] = Memorial.objects.all().order_by('-id')
        return context


# View para criar etapa de Compras em Locações
class CreateComprasLocView(SuccessMessageMixin, CreateView):
    model = Compras_Locacao
    template_name = 'locacao_acao_consulta.html'
    fields = ['descricao', 'numero', 'data', 'observacoes',
              'locacao', 'trp', 'prazo', 'status', 'sede']
    success_url = reverse_lazy('list_loc')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trps'] = TRP.objects.all()
        context['statuses'] = Status.objects.all()
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Compras cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = ComprasLocacaoModelForm(request.POST)
        if form.is_valid():
            compra = form.save()
            print(compra.locacao)
            locacao = Locacao_Acao.objects.get(descricao=compra.locacao)
            locacao.status_geral = compra.status
            print(locacao)
            print(compra.status)
            locacao.save()
            compra.save()
            messages.success(request, 'Processo em compras'
                                      ' cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[locacao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar etapa de Compras em Aquisições
class CreateComprasAquisView(SuccessMessageMixin, CreateView):
    model = Compras_Aquisicao
    template_name = 'aquisicao_acao_consulta.html'
    fields = ['descricao', 'numero', 'data', 'observacoes',
              'aquisicao', 'trp', 'prazo', 'status', 'sede']
    success_url = reverse_lazy('list_aquis')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trps'] = TRP.objects.all()
        context['statuses'] = Status.objects.all()
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Compras cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = ComprasAquisicaoModelForm(request.POST)
        if form.is_valid():
            compra = form.save()
            print(compra.aquisicao)
            aquisicao = Aquisicao_Acao.objects.get(descricao=compra.aquisicao)
            aquisicao.status_geral = compra.status
            print(aquisicao)
            print(compra.status)
            aquisicao.save()
            compra.save()
            messages.success(request, 'Processo em compras '
                                      'cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquisicao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar etapa de Compras em Manutenções
class CreateComprasManutView(SuccessMessageMixin, CreateView):
    model = Compras_Manutencao
    template_name = 'manutencao_acao_consulta.html'
    fields = ['descricao', 'numero', 'data', 'observacoes', 'manutencao',
              'trp', 'prazo', 'status', 'sede']
    success_url = reverse_lazy('list_manut')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trps'] = TRP.objects.all()
        context['statuses'] = Status.objects.all()
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Compras cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = ComprasManutencaoModelForm(request.POST)
        if form.is_valid():
            compra = form.save()
            print(compra.manutencao)
            manutencao = Manutencao_Acao.objects.get(
                descricao=compra.manutencao)
            manutencao.status_geral = compra.status
            print(manutencao)
            print(compra.status)
            manutencao.save()
            compra.save()
            messages.success(request, 'Processo em compras '
                                      'cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manutencao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar TRP
class CreateTRPView(CreateView):
    model = TRP
    template_name = 'form_create_trp.html'
    fields = ['numeroTRP', 'descricao', 'data_fim_contrato',
              'data_fim_contrato_pror', 'observacoes']
    success_url = reverse_lazy('add_trp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trps'] = TRP.objects.all().order_by('-id')
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "TRP cadastrada com sucesso!"


# View para criar Orçamentos
class CreateOrcView(SuccessMessageMixin, CreateView):
    model = Orcamento
    template_name = 'form_create_orc.html'
    fields = ['compras_loc', 'fornecedor', 'valor', 'observacoes']
    success_url = reverse_lazy('add_orc')

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Orçamento cadastrado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['compras'] = Compras_Locacao.objects.all()
        context['fornecedores'] = Fornecedor.objects.all()
        context['orcamentos'] = Orcamento.objects.all().order_by('-id')
        return context


# View para criar etapa de Sede em Locações
class CreateSedeView(SuccessMessageMixin, CreateView):
    model = Sede
    template_name = 'locacao_acao_consulta.html'
    fields = ['descricao', 'numero', 'dataminuta', 'datadca',
              'anotacoes', 'licitacao', 'locacao', 'prazo',  'status']
    success_url = reverse_lazy('list_loc')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Sede cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = SedeModelForm(request.POST)
        if form.is_valid():
            sede = form.save()
            print(sede.locacao)
            locacao = Locacao_Acao.objects.get(descricao=sede.locacao)
            locacao.status_geral = sede.status
            print(locacao)
            print(sede.status)
            locacao.save()
            sede.save()
            messages.success(request, 'Processo em Sede '
                                      'cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[locacao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar etapa de Sede em Aquisições
class CreateSedeAquisicaoView(SuccessMessageMixin, CreateView):
    model = Sede_Aquisicao
    template_name = 'aquisicao_acao_consulta.html'
    fields = ['descricao', 'numero', 'dataminuta', 'datadca', 'anotacoes',
              'licitacao', 'aquisicao', 'prazo',  'status']
    success_url = reverse_lazy('list_aquis')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Sede cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = SedeAquisicaoModelForm(request.POST)
        if form.is_valid():
            sede = form.save()
            print(sede.aquisicao)
            aquisicao = Aquisicao_Acao.objects.get(descricao=sede.aquisicao)
            aquisicao.status_geral = sede.status
            print(aquisicao)
            print(sede.status)
            aquisicao.save()
            sede.save()
            messages.success(request, 'Processo em Sede '
                                      'cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquisicao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar etapa de Sede em Manutenções
class CreateSedeManutencaoView(SuccessMessageMixin, CreateView):
    model = Sede_Manutencao
    template_name = 'manutencao_acao_consulta.html'
    fields = ['descricao', 'numero', 'dataminuta', 'datadca', 'anotacoes',
              'licitacao', 'manutencao', 'prazo',  'status']
    success_url = reverse_lazy('list_manut')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Sede cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = SedeManutencaoModelForm(request.POST)
        if form.is_valid():
            sede = form.save()
            print(sede.manutencao)
            manutencao = Manutencao_Acao.objects.get(descricao=sede.manutencao)
            manutencao.status_geral = sede.status
            print(manutencao)
            print(sede.status)
            manutencao.save()
            sede.save()
            messages.success(request, 'Processo em Sede '
                                      'cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manutencao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar Licitação
class CreateLicView(SuccessMessageMixin, CreateView):
    model = Licitacao
    template_name = 'form_create_lic.html'
    fields = ['dataabertura', 'datapregao', 'dataassinatura',
              'datahomologacao', 'vencedor', 'valor']
    success_url = reverse_lazy('add_lic')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['licitacoes'] = Licitacao.objects.all().order_by('-id')
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Licitação cadastrado com sucesso!"


# View para criar Contratos de Locação
class CreateContrView(CreateView, SuccessMessageMixin):
    model = Contrato_Locacao
    template_name = 'locacao_acao_consulta.html'
    fields = ['descricao', 'processo', 'dataprocesso',
              'instrcontratual', 'datacontrato', 'valorservico',
              'valorlocacao', 'locacao', 'prazo', 'status']
    success_url = reverse_lazy('sistema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Contratação cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = ContratoLocacaoModelForm(request.POST)
        if form.is_valid():
            contrato = form.save()
            print(contrato.locacao)
            locacao = Locacao_Acao.objects.get(descricao=contrato.locacao)
            locacao.status_geral = contrato.status
            print(locacao)
            print(contrato.status)
            locacao.save()
            contrato.save()
            messages.success(request, 'Processo em Contratação '
                                      'cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[locacao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar Contratos de Aquisição
class CreateContrAquisicaoView(CreateView, SuccessMessageMixin):
    model = Contrato_Aquisicao
    template_name = 'aquisicao_acao_consulta.html'
    fields = ['descricao', 'processo', 'dataprocesso',
              'instrcontratual', 'datacontrato', 'valorservico',
              'valorlocacao', 'aquisicao', 'prazo', 'status']
    success_url = reverse_lazy('sistema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Contratação cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = ContratoAquisicaoModelForm(request.POST)
        if form.is_valid():
            contrato = form.save()
            print(contrato.aquisicao)
            aquisicao = Aquisicao_Acao.objects.get(
                descricao=contrato.aquisicao)
            aquisicao.status_geral = contrato.status
            print(aquisicao)
            print(contrato.status)
            aquisicao.save()
            contrato.save()
            messages.success(request, 'Processo em Contratação '
                                      'cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquisicao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar Contratos de Manutenção
class CreateContrManutencaoView(CreateView, SuccessMessageMixin):
    model = Contrato_Manutencao
    template_name = 'manutencao_acao_consulta.html'
    fields = ['descricao', 'processo', 'dataprocesso', 'instrcontratual',
              'datacontrato', 'valorservico',
              'valorlocacao', 'manutencao', 'prazo', 'status']
    success_url = reverse_lazy('sistema')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Contratação cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = ContratoManutencaoModelForm(request.POST)
        if form.is_valid():
            contrato = form.save()
            print(contrato.manutencao)
            manutencao = Manutencao_Acao.objects.get(
                descricao=contrato.manutencao)
            manutencao.status_geral = contrato.status
            print(manutencao)
            print(contrato.status)
            manutencao.save()
            contrato.save()
            messages.success(request, 'Processo em Contratação '
                                      'cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manutencao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar Pagamentos em Locações
class CreatePagtoView(CreateView, SuccessMessageMixin):
    model = Pagamento
    template_name = 'locacao_acao_consulta.html'
    fields = ['descricao', 'tipo_pagto', 'atividade', 'parcela',
              'qtde_parcelas', 'valor', 'dataprevnota',
              'tiponota', 'numnota', 'dataemissnota', 'serienota', 'xml',
              'anotacoes', 'locacao', 'prazo', 'status']
    success_url = reverse_lazy('list_loc')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Pagamento cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = PagamentoModelForm(request.POST)
        if form.is_valid():
            pagto = form.save()
            print(pagto.locacao)
            locacao = Locacao_Acao.objects.get(descricao=pagto.locacao)
            locacao.status_geral = pagto.status
            print(locacao)
            print(pagto.status)
            locacao.save()
            pagto.save()
            messages.success(request, 'Processo em Contratação'
                                      ' cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[locacao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar Pagamentos em Aquisições
class CreatePagtoAquisicaoView(CreateView, SuccessMessageMixin):
    model = Pagamento_Aquisicao
    template_name = 'aquisicao_acao_consulta.html'
    fields = ['descricao', 'tipo_pagto', 'atividade', 'parcela',
              'qtde_parcelas', 'valor', 'dataprevnota',
              'tiponota', 'numnota', 'dataemissnota', 'serienota', 'xml',
              'anotacoes', 'aquisicao', 'prazo', 'status']
    success_url = reverse_lazy('list_aquis')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Pagamento cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = PagamentoAquisicaoModelForm(request.POST)
        if form.is_valid():
            pagto = form.save()
            print(pagto.aquisicao)
            aquisicao = Aquisicao_Acao.objects.get(descricao=pagto.aquisicao)
            aquisicao.status_geral = pagto.status
            print(aquisicao)
            print(pagto.status)
            aquisicao.save()
            pagto.save()
            messages.success(request, 'Processo em Contratação'
                                      ' cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquisicao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar Pagamentos em Manutenções
class CreatePagtoManutencaoView(CreateView, SuccessMessageMixin):
    model = Pagamento_Manutencao
    template_name = 'manutencao_acao_consulta.html'
    fields = ['descricao', 'tipo_pagto', 'atividade', 'parcela',
              'qtde_parcelas', 'valor', 'dataprevnota',
              'tiponota', 'numnota', 'dataemissnota', 'serienota',
              'xml', 'anotacoes', 'manutencao', 'prazo', 'status']
    success_url = reverse_lazy('list_manut')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Pagamento cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = PagamentoManutencaoModelForm(request.POST)
        if form.is_valid():
            pagto = form.save()
            print(pagto.manutencao)
            manutencao = Manutencao_Acao.objects.get(
                descricao=pagto.manutencao)
            manutencao.status_geral = pagto.status
            print(manutencao)
            print(pagto.status)
            manutencao.save()
            pagto.save()
            messages.success(request, 'Processo em Contratação '
                                      'cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manutencao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar Cronograma para locações
class CreateCronoView(SuccessMessageMixin, CreateView):
    model = Cronograma
    template_name = 'locacao_acao_consulta.html'
    fields = ['locacao', 'atividade', 'datainicio', 'datafim',
              'anotacoes', 'prazo', 'status']
    success_url = reverse_lazy('list_loc')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Recebimento cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = CronogramaModelForm(request.POST)
        if form.is_valid():
            crono = form.save()
            print(crono.locacao)
            locacao = Locacao_Acao.objects.get(descricao=crono.locacao)
            locacao.status_geral = crono.status
            print(locacao)
            print(crono.status)
            locacao.save()
            crono.save()
            messages.success(request, 'Processo em Recebimento'
                                      ' cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[locacao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar Cronograma para Aquisições
class CreateCronoAquisicaoView(SuccessMessageMixin, CreateView):
    model = Cronograma_Aquisicao
    template_name = 'aquisicao_acao_consulta.html'
    fields = ['aquisicao', 'atividade', 'datainicio',
              'datafim', 'anotacoes', 'prazo', 'status']
    success_url = reverse_lazy('list_aquis')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Recebimento cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = CronogramaAquisicaoModelForm(request.POST)
        if form.is_valid():
            crono = form.save()
            print(crono.aquisicao)
            aquisicao = Aquisicao_Acao.objects.get(descricao=crono.aquisicao)
            aquisicao.status_geral = crono.status
            print(aquisicao)
            print(crono.status)
            aquisicao.save()
            crono.save()
            messages.success(request, 'Processo em Recebimento'
                                      ' cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquisicao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar Cronograma para Manutenções
class CreateCronoManutencaoView(SuccessMessageMixin, CreateView):
    model = Cronograma_Manutencao
    template_name = 'manutencao_acao_consulta.html'
    fields = ['manutencao', 'atividade', 'datainicio',
              'datafim', 'anotacoes', 'prazo', 'status']
    success_url = reverse_lazy('list_manut')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Recebimento cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = CronogramaManutencaoModelForm(request.POST)
        if form.is_valid():
            crono = form.save()
            print(crono.manutencao)
            manutencao = Manutencao_Acao.objects.get(
                descricao=crono.manutencao)
            manutencao.status_geral = crono.status
            print(manutencao)
            print(crono.status)
            manutencao.save()
            crono.save()
            messages.success(request, 'Processo em Recebimento '
                                      'cadastrado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manutencao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para criar Aprovação
class CreateAprovView(CreateView):
    model = Aprovacao
    template_name = 'form_create_aprov.html'
    fields = ['setor', 'data', 'dca']
    success_url = reverse_lazy('sistema')


# View para criar Fornecedor
class CreateFornecView(SuccessMessageMixin, CreateView):
    model = Fornecedor
    template_name = 'form_create_fornec.html'
    fields = ['nome', 'cnpj', 'site', 'observacoes']
    success_url = reverse_lazy('add_fornec')

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Fornecedor cadastrado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fornecedores'] = Fornecedor.objects.all().order_by('-id')
        return context


# View para criar Categorias de Fornecedores
class CreateCatFornecView(CreateView):
    model = CatFornecedor
    template_name = 'form_create_catfornec.html'
    fields = ['descricao', 'fornecedor']
    success_url = reverse_lazy('sistema')


# View para criar Endereços de Fornecedor
class CreateEndFornecView(CreateView):
    model = EndFornecedor
    template_name = 'form_create_endfornec.html'
    fields = ['logradouro', 'numero', 'complemento', 'CEP',
              'bairro', 'cidade', 'estado', 'pais', 'fornecedor']
    success_url = reverse_lazy('sistema')


# View para criar Contatos de Fornecedor
class CreateContFornecView(CreateView):
    model = ContFornecedor
    template_name = 'form_create_contfornec.html'
    fields = ['nome', 'telefone', 'email', 'observacoes', 'fornecedor']
    success_url = reverse_lazy('sistema')


# View para criar tipos de Status
class CreateTipoStatusView(CreateView):
    model = Tipo_Status
    template_name = 'form_create_tipostatus.html'
    fields = ['descricao']
    success_url = reverse_lazy('sistema')


# View para criar Status
class CreateStatusView(SuccessMessageMixin, CreateView):
    model = Status
    template_name = 'form_create_status.html'
    fields = ['tipo_status', 'descricao']
    success_url = reverse_lazy('add_status')

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Status cadastrado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tiposstatuses'] = Tipo_Status.objects.all()
        context['statuses'] = Status.objects.all()
        return context


# View para criar Local
class CreateLocalView(SuccessMessageMixin, CreateView):
    model = Local
    template_name = 'form_create_local.html'
    fields = ['descricao']
    success_url = reverse_lazy('add_local')

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Local cadastrado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locais'] = Local.objects.all().order_by('-id')
        return context


# View para criar Linguagem
class CreateLinguagemView(SuccessMessageMixin, CreateView):
    model = Linguagem
    template_name = 'form_create_ling.html'
    fields = ['descricao']
    success_url = reverse_lazy('add_linguagem')

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Linguagem cadastrado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['linguagens'] = Linguagem.objects.all().order_by('-id')
        return context


# View para criar Projeto
class CreateProjetoView(SuccessMessageMixin, CreateView):
    model = Projeto
    template_name = 'form_create_proj.html'
    fields = ['descricao']
    success_url = reverse_lazy('add_projeto')

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Projeto cadastrado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projetos'] = Projeto.objects.all().order_by('-id')
        return context


# View para criar Tipo de Pagamento
class CreateTipoPagtoView(CreateView):
    model = TipoPagto
    template_name = 'form_create_tipopagto.html'
    fields = ['descricao']
    success_url = reverse_lazy('sistema')


# Função para salvar Tipo de Locação - utilizada nos formulário Modal
def salvatipoloc(request):
    descricao = request.POST.get('descricao')
    if TipoLocacao.objects.filter(descricao=descricao).exists():
        messages.error(request, 'Tipo de locação já cadastrada',
                       extra_tags='tipoloc')
        return redirect('../add/')
    else:
        form = TipoLocacaoModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de locação incluída'
                                      ' com sucesso', extra_tags='tipoloc')
            return redirect('../add/')


# Função para salvar Memorial- utilizada nos formulário Modal
def salvamemorial(request):
    descricao = request.POST.get('descricao')
    if Memorial.objects.filter(descricao=descricao).exists():
        messages.error(request, "Memorial já cadastrado!")
        return redirect('../add/')
    else:
        form = MemorialModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Memorial Cadastrado com sucesso')
            return redirect('../add/')


# Função para salvar Tipo de Locação - utilizada nos formulário Modal
def salvaprojeto(request):
    descricao = request.POST.get('descricao')
    if Projeto.objects.filter(descricao=descricao).exists():
        messages.error(request, "Projeto já cadastrado!")
        return redirect('../add/')
    else:
        form = ProjetoModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto Cadastrado com sucesso')
            return redirect('../add/')


# Função para consultar locações
def consultalocacao(request):
    tipoloc = request.POST.get("tipo_locacao")
    acao = request.POST.get("acao")
    memorial = request.POST.get("memorial")
    status_geral = request.POST.get("status_geral")
    print(request.POST)

    criterio1 = False
    criterio2 = False
    criterio3 = False
    criterio4 = False

    if tipoloc != '':
        criterio1 = True
    if acao != '':
        criterio2 = True
    if memorial != '':
        criterio3 = True
    if status_geral != '':
        criterio4 = True

    if criterio1 is True and criterio2 is False and criterio3 is False:
        locacoes = Locacao_Acao.objects.filter(tipo_locacao=tipoloc)
    if criterio1 is False and criterio2 is True and criterio3 is False:
        locacoes = Locacao_Acao.objects.filter(acao=acao)
    if criterio1 is False and criterio2 is False and criterio3 is True:
        locacoes = Locacao_Acao.objects.filter(memorial=memorial)
    if criterio1 is True and criterio2 is True and criterio3 is False:
        locacoes = Locacao_Acao.objects.filter(tipo_locacao=tipoloc, acao=acao)
    if criterio1 is True and criterio2 is False and criterio3 is True:
        locacoes = Locacao_Acao.objects.filter(tipo_locacao=tipoloc,
                                               memorial=memorial)
    if criterio1 is False and criterio2 is True and criterio3 is True:
        locacoes = Locacao_Acao.objects.filter(acao=acao, memorial=memorial)
    if criterio1 is True and criterio2 is True and criterio3 is True:
        locacoes = Locacao_Acao.objects.filter(tipo_locacao=tipoloc,
                                               acao=acao, memorial=memorial)
    if criterio4 is True:
        locacoes = Locacao_Acao.objects.filter(status_geral=status_geral)
    if criterio1 is False and criterio2 is False and \
            criterio3 is False and criterio4 is False:
        locacoes = Locacao_Acao.objects.all()

    tiposlocacao = TipoLocacao.objects.all()
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()
    context = {'locacoes': locacoes.order_by('-data_cadastro'),
               'tiposlocacao': tiposlocacao,
               'acoes': acoes,
               'memoriais': memoriais,
               'statuses': statuses
               }
    return render(request, 'locacao_acao_listview.html', context)


# Função para consultar aquisições
def consultaaquisicao(request):
    acao = request.POST.get("acao")
    memorial = request.POST.get("memorial")
    status_geral = request.POST.get("status_geral")
    print(request.POST)

    criterio1 = False
    criterio2 = False
    criterio3 = False

    if acao != '':
        criterio1 = True
    if memorial != '':
        criterio2 = True
    if status_geral != '':
        criterio3 = True

    if criterio1 is False and criterio2 is False and criterio3 is False:
        aquisicoes = Aquisicao_Acao.objects.all()
    if criterio1 is True and criterio2 is False and criterio3 is False:
        aquisicoes = Aquisicao_Acao.objects.filter(acao=acao)
    if criterio1 is False and criterio2 is True and criterio3 is False:
        aquisicoes = Aquisicao_Acao.objects.filter(memorial=memorial)
    if criterio1 is False and criterio2 is False and criterio3 is True:
        aquisicoes = Aquisicao_Acao.objects.filter(status_geral=status_geral)
    if criterio1 is True and criterio2 is True and criterio3 is False:
        aquisicoes = Aquisicao_Acao.objects.filter(acao=acao,
                                                   memorial=memorial)
    if criterio1 is True and criterio2 is False and criterio3 is True:
        aquisicoes = Aquisicao_Acao.objects.filter(acao=acao,
                                                   status_geral=status_geral)
    if criterio1 is False and criterio2 is True and criterio3 is True:
        aquisicoes = Aquisicao_Acao.objects.filter(memorial=memorial,
                                                   status_geral=status_geral)

    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()
    context = {'aquisicoes': aquisicoes.order_by('-id'),
               'acoes': acoes,
               'memoriais': memoriais,
               'statuses': statuses
               }
    return render(request, 'aquisicao_acao_listview.html', context)


# Função para consultar manutenções
def consultamanutencao(request):
    acao = request.POST.get("acao")
    memorial = request.POST.get("memorial")
    status_geral = request.POST.get("status_geral")
    print(request.POST)

    criterio1 = False
    criterio2 = False
    criterio3 = False

    if acao != '':
        criterio1 = True
    if memorial != '':
        criterio2 = True
    if status_geral != '':
        criterio3 = True

    if criterio1 is False and criterio2 is False and criterio3 is False:
        manutencoes = Manutencao_Acao.objects.all()
    if criterio1 is True and criterio2 is False and criterio3 is False:
        manutencoes = Manutencao_Acao.objects.filter(acao=acao)
    if criterio1 is False and criterio2 is True and criterio3 is False:
        manutencoes = Manutencao_Acao.objects.filter(memorial=memorial)
    if criterio1 is False and criterio2 is False and criterio3 is True:
        manutencoes = Manutencao_Acao.objects.filter(status_geral=status_geral)
    if criterio1 is True and criterio2 is True and criterio3 is False:
        manutencoes = Manutencao_Acao.objects.filter(acao=acao,
                                                     memorial=memorial)
    if criterio1 is True and criterio2 is False and criterio3 is True:
        manutencoes = Manutencao_Acao.objects.filter(acao=acao,
                                                     status_geral=status_geral)
    if criterio1 is False and criterio2 is True and criterio3 is True:
        manutencoes = Manutencao_Acao.objects.filter(memorial=memorial,
                                                     status_geral=status_geral)

    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()
    context = {'manutencoes': manutencoes.order_by('-id'),
               'acoes': acoes,
               'memoriais': memoriais,
               'statuses': statuses
               }
    return render(request, 'manutencao_acao_listview.html', context)


# Função para consultar uma determinada locação
def consultaumalocacao(request, pk):

    idpassado = pk
    consulta = get_object_or_404(Locacao_Acao, id=pk)
    consultacompras = ''
    dataprazocompras = ''
    dataprazo1compras = ''
    dataprazo2compras = ''
    if Compras_Locacao.objects.filter(locacao=idpassado).exists():
        consultacompras = Compras_Locacao.objects.get(locacao=idpassado)
        dataprazocompras = consultacompras.criado + relativedelta(
            days=consultacompras.prazo)
        dataprazo1compras = consultacompras.criado + relativedelta(
            days=(consultacompras.prazo/3))
        dataprazo2compras = dataprazo1compras + relativedelta(
            days=(consultacompras.prazo/3))
        dataprazocompras = dataprazocompras.date()
        dataprazo1compras = dataprazo1compras.date()
        dataprazo2compras = dataprazo2compras.date()

    consultasede = ''
    dataprazosede = ''
    dataprazo1sede = ''
    dataprazo2sede = ''
    if Sede.objects.filter(locacao=idpassado).exists():
        consultasede = Sede.objects.get(locacao=idpassado)
        dataprazosede = consultasede.criado + relativedelta(
            days=consultasede.prazo)
        dataprazo1sede = consultasede.criado + relativedelta(
            days=(consultasede.prazo / 3))
        dataprazo2sede = dataprazo1sede + relativedelta(
            days=(consultasede.prazo / 3))
        dataprazosede = dataprazosede.date()
        dataprazo1sede = dataprazo1sede.date()
        dataprazo2sede = dataprazo2sede.date()

    consultacontrat = ''
    dataprazocontrat = ''
    dataprazo1contrat = ''
    dataprazo2contrat = ''

    if Contrato_Locacao.objects.filter(locacao=idpassado).exists():
        consultacontrat = Contrato_Locacao.objects.get(locacao=idpassado)
        dataprazocontrat = consultacontrat.criado + relativedelta(
            days=consultacontrat.prazo)
        dataprazo1contrat = consultacontrat.criado + relativedelta(
            days=(consultacontrat.prazo / 3))
        dataprazo2contrat = dataprazo1contrat + relativedelta(
            days=(consultacontrat.prazo / 3))
        dataprazocontrat = dataprazocontrat.date()
        dataprazo1contrat = dataprazo1contrat.date()
        dataprazo2contrat = dataprazo2contrat.date()

    consultapagto = ''
    dataprazopagto = ''
    dataprazo1pagto = ''
    dataprazo2pagto = ''
    if Pagamento.objects.filter(locacao=idpassado).exists():
        consultapagto = Pagamento.objects.get(locacao=idpassado)
        dataprazopagto = consultapagto.criado + relativedelta(
            days=consultapagto.prazo)
        dataprazo1pagto = consultapagto.criado + relativedelta(
            days=(consultapagto.prazo / 3))
        dataprazo2pagto = dataprazo1pagto + relativedelta(
            days=(consultapagto.prazo / 3))
        dataprazopagto = dataprazopagto.date()
        dataprazo1pagto = dataprazo1pagto.date()
        dataprazo2pagto = dataprazo2pagto.date()

    consultareceb = ''
    dataprazoreceb = ''
    dataprazo1receb = ''
    dataprazo2receb = ''
    if Cronograma.objects.filter(locacao=idpassado).exists():
        consultareceb = Cronograma.objects.get(locacao=idpassado)
        dataprazoreceb = consultareceb.criado + relativedelta(
            days=consultareceb.prazo)
        dataprazo1receb = consultareceb.criado + relativedelta(
            days=(consultareceb.prazo / 3))
        dataprazo2receb = dataprazo1receb + relativedelta(
            days=(consultareceb.prazo / 3))
        dataprazoreceb = dataprazoreceb.date()
        dataprazo1receb = dataprazo1receb.date()
        dataprazo2receb = dataprazo2receb.date()

    datahoje = date.today()
    statuses = Status.objects.all()
    tiposlocacao = TipoLocacao.objects.all()
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    trps = TRP.objects.all()
    licitacoes = Licitacao.objects.all()
    pagamentos = Pagamento.objects.all()
    tipospagto = TipoPagto.objects.all()
    context = {
            'consulta': consulta,
            'consultacompras': consultacompras,
            'consultasede': consultasede,
            'consultacontrat': consultacontrat,
            'consultapagto': consultapagto,
            'consultareceb': consultareceb,
            'status_chave_sol': 'Solicitação - Concluída',
            'status_chave_compras': 'Compras - Concluída',
            'status_chave_sede': 'Sede - Concluída',
            'status_chave_contrat': 'Contratação - Concluída',
            'status_chave_pagto': 'Pagamento - Concluída',
            'status_chave_receb': 'Recebimento - Concluída',
            'statuses': statuses,
            'trps': trps,
            'tiposlocacao': tiposlocacao,
            'acoes': acoes,
            'licitacoes': licitacoes,
            'pagamentos': pagamentos,
            'tipospagto': tipospagto,
            'memoriais': memoriais,
            'datahoje': datahoje,
            'dataprazocompras': dataprazocompras,
            'dataprazo1compras': dataprazo1compras,
            'dataprazo2compras': dataprazo2compras,
            'dataprazosede': dataprazosede,
            'dataprazo1sede': dataprazo1sede,
            'dataprazo2sede': dataprazo2sede,
            'dataprazocontrat': dataprazocontrat,
            'dataprazo1contrat': dataprazo1contrat,
            'dataprazo2contrat': dataprazo2contrat,
            'dataprazopagto': dataprazopagto,
            'dataprazo1pagto': dataprazo1pagto,
            'dataprazo2pagto': dataprazo2pagto,
            'dataprazoreceb': dataprazoreceb,
            'dataprazo1receb': dataprazo1receb,
            'dataprazo2receb': dataprazo2receb
    }
    return render(request, 'locacao_acao_consulta.html', context)


# Função que consulta uma determinada aquisição
def consultaumaaquisicao(request, pk):

    idpassado = pk
    consulta = get_object_or_404(Aquisicao_Acao, id=pk)
    consultacompras = ''
    dataprazocompras = ''
    dataprazo1compras = ''
    dataprazo2compras = ''
    if Compras_Aquisicao.objects.filter(aquisicao=idpassado).exists():
        consultacompras = Compras_Aquisicao.objects.get(aquisicao=idpassado)
        dataprazocompras = consultacompras.criado + relativedelta(
            days=consultacompras.prazo)
        dataprazo1compras = consultacompras.criado + relativedelta(
            days=(consultacompras.prazo/3))
        dataprazo2compras = dataprazo1compras + relativedelta(
            days=(consultacompras.prazo/3))
        dataprazocompras = dataprazocompras.date()
        dataprazo1compras = dataprazo1compras.date()
        dataprazo2compras = dataprazo2compras.date()

    consultasede = ''
    dataprazosede = ''
    dataprazo1sede = ''
    dataprazo2sede = ''
    if Sede_Aquisicao.objects.filter(aquisicao=idpassado).exists():
        consultasede = Sede_Aquisicao.objects.get(aquisicao=idpassado)
        dataprazosede = consultasede.criado + relativedelta(
            days=consultasede.prazo)
        dataprazo1sede = consultasede.criado + relativedelta(
            days=(consultasede.prazo / 3))
        dataprazo2sede = dataprazo1sede + relativedelta(
            days=(consultasede.prazo / 3))
        dataprazosede = dataprazosede.date()
        dataprazo1sede = dataprazo1sede.date()
        dataprazo2sede = dataprazo2sede.date()

    consultacontrat = ''
    dataprazocontrat = ''
    dataprazo1contrat = ''
    dataprazo2contrat = ''

    if Contrato_Aquisicao.objects.filter(aquisicao=idpassado).exists():
        consultacontrat = Contrato_Aquisicao.objects.get(aquisicao=idpassado)
        dataprazocontrat = consultacontrat.criado + relativedelta(
            days=consultacontrat.prazo)
        dataprazo1contrat = consultacontrat.criado + relativedelta(
            days=(consultacontrat.prazo / 3))
        dataprazo2contrat = dataprazo1contrat + relativedelta(
            days=(consultacontrat.prazo / 3))
        dataprazocontrat = dataprazocontrat.date()
        dataprazo1contrat = dataprazo1contrat.date()
        dataprazo2contrat = dataprazo2contrat.date()

    consultapagto = ''
    dataprazopagto = ''
    dataprazo1pagto = ''
    dataprazo2pagto = ''
    if Pagamento_Aquisicao.objects.filter(aquisicao=idpassado).exists():
        consultapagto = Pagamento_Aquisicao.objects.get(aquisicao=idpassado)
        dataprazopagto = consultapagto.criado + relativedelta(
            days=consultapagto.prazo)
        dataprazo1pagto = consultapagto.criado + relativedelta(
            days=(consultapagto.prazo / 3))
        dataprazo2pagto = dataprazo1pagto + relativedelta(
            days=(consultapagto.prazo / 3))
        dataprazopagto = dataprazopagto.date()
        dataprazo1pagto = dataprazo1pagto.date()
        dataprazo2pagto = dataprazo2pagto.date()

    consultareceb = ''
    dataprazoreceb = ''
    dataprazo1receb = ''
    dataprazo2receb = ''
    if Cronograma_Aquisicao.objects.filter(aquisicao=idpassado).exists():
        consultareceb = Cronograma_Aquisicao.objects.get(aquisicao=idpassado)
        dataprazoreceb = consultareceb.criado + relativedelta(
            days=consultareceb.prazo)
        dataprazo1receb = consultareceb.criado + relativedelta(
            days=(consultareceb.prazo / 3))
        dataprazo2receb = dataprazo1receb + relativedelta(
            days=(consultareceb.prazo / 3))
        dataprazoreceb = dataprazoreceb.date()
        dataprazo1receb = dataprazo1receb.date()
        dataprazo2receb = dataprazo2receb.date()

    datahoje = date.today()
    statuses = Status.objects.all()
    # acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    trps = TRP.objects.all()
    licitacoes = Licitacao.objects.all()
    pagamentos = Pagamento.objects.all()
    tipospagto = TipoPagto.objects.all()
    context = {
            'consulta': consulta,
            'consultacompras': consultacompras,
            'consultasede': consultasede,
            'consultacontrat': consultacontrat,
            'consultapagto': consultapagto,
            'consultareceb': consultareceb,
            'status_chave_sol': 'Solicitação - Concluída',
            'status_chave_compras': 'Compras - Concluída',
            'status_chave_sede': 'Sede - Concluída',
            'status_chave_contrat': 'Contratação - Concluída',
            'status_chave_pagto': 'Pagamento - Concluída',
            'status_chave_receb': 'Recebimento - Concluída',
            'statuses': statuses,
            'trps': trps,
            # 'acoes': acoes,
            'licitacoes': licitacoes,
            'pagamentos': pagamentos,
            'tipospagto': tipospagto,
            'memoriais': memoriais,
            'datahoje': datahoje,
            'dataprazocompras': dataprazocompras,
            'dataprazo1compras': dataprazo1compras,
            'dataprazo2compras': dataprazo2compras,
            'dataprazosede': dataprazosede,
            'dataprazo1sede': dataprazo1sede,
            'dataprazo2sede': dataprazo2sede,
            'dataprazocontrat': dataprazocontrat,
            'dataprazo1contrat': dataprazo1contrat,
            'dataprazo2contrat': dataprazo2contrat,
            'dataprazopagto': dataprazopagto,
            'dataprazo1pagto': dataprazo1pagto,
            'dataprazo2pagto': dataprazo2pagto,
            'dataprazoreceb': dataprazoreceb,
            'dataprazo1receb': dataprazo1receb,
            'dataprazo2receb': dataprazo2receb
    }
    return render(request, 'aquisicao_acao_consulta.html', context)


# Função que consulta uma determinada manutenção
def consultaumamanutencao(request, pk):

    idpassado = pk
    consulta = get_object_or_404(Manutencao_Acao, id=pk)
    consultacompras = ''
    dataprazocompras = ''
    dataprazo1compras = ''
    dataprazo2compras = ''
    if Compras_Manutencao.objects.filter(manutencao=idpassado).exists():
        consultacompras = Compras_Manutencao.objects.get(manutencao=idpassado)
        dataprazocompras = consultacompras.criado + relativedelta(
            days=consultacompras.prazo)
        dataprazo1compras = consultacompras.criado + relativedelta(
            days=(consultacompras.prazo/3))
        dataprazo2compras = dataprazo1compras + relativedelta(
            days=(consultacompras.prazo/3))
        dataprazocompras = dataprazocompras.date()
        dataprazo1compras = dataprazo1compras.date()
        dataprazo2compras = dataprazo2compras.date()

    consultasede = ''
    dataprazosede = ''
    dataprazo1sede = ''
    dataprazo2sede = ''
    if Sede_Manutencao.objects.filter(manutencao=idpassado).exists():
        consultasede = Sede_Manutencao.objects.get(manutencao=idpassado)
        dataprazosede = consultasede.criado + relativedelta(
            days=consultasede.prazo)
        dataprazo1sede = consultasede.criado + relativedelta(
            days=(consultasede.prazo / 3))
        dataprazo2sede = dataprazo1sede + relativedelta(
            days=(consultasede.prazo / 3))
        dataprazosede = dataprazosede.date()
        dataprazo1sede = dataprazo1sede.date()
        dataprazo2sede = dataprazo2sede.date()

    consultacontrat = ''
    dataprazocontrat = ''
    dataprazo1contrat = ''
    dataprazo2contrat = ''

    if Contrato_Manutencao.objects.filter(manutencao=idpassado).exists():
        consultacontrat = Contrato_Manutencao.objects.get(manutencao=idpassado)
        dataprazocontrat = consultacontrat.criado + relativedelta(
            days=consultacontrat.prazo)
        dataprazo1contrat = consultacontrat.criado + relativedelta(
            days=(consultacontrat.prazo / 3))
        dataprazo2contrat = dataprazo1contrat + relativedelta(
            days=(consultacontrat.prazo / 3))
        dataprazocontrat = dataprazocontrat.date()
        dataprazo1contrat = dataprazo1contrat.date()
        dataprazo2contrat = dataprazo2contrat.date()

    consultapagto = ''
    dataprazopagto = ''
    dataprazo1pagto = ''
    dataprazo2pagto = ''
    if Pagamento_Manutencao.objects.filter(manutencao=idpassado).exists():
        consultapagto = Pagamento_Manutencao.objects.get(manutencao=idpassado)
        dataprazopagto = consultapagto.criado + relativedelta(
            days=consultapagto.prazo)
        dataprazo1pagto = consultapagto.criado + relativedelta(
            days=(consultapagto.prazo / 3))
        dataprazo2pagto = dataprazo1pagto + relativedelta(
            days=(consultapagto.prazo / 3))
        dataprazopagto = dataprazopagto.date()
        dataprazo1pagto = dataprazo1pagto.date()
        dataprazo2pagto = dataprazo2pagto.date()

    consultareceb = ''
    dataprazoreceb = ''
    dataprazo1receb = ''
    dataprazo2receb = ''
    if Cronograma_Manutencao.objects.filter(manutencao=idpassado).exists():
        consultareceb = Cronograma_Manutencao.objects.get(manutencao=idpassado)
        dataprazoreceb = consultareceb.criado + relativedelta(
            days=consultareceb.prazo)
        dataprazo1receb = consultareceb.criado + relativedelta(
            days=(consultareceb.prazo / 3))
        dataprazo2receb = dataprazo1receb + relativedelta(
            days=(consultareceb.prazo / 3))
        dataprazoreceb = dataprazoreceb.date()
        dataprazo1receb = dataprazo1receb.date()
        dataprazo2receb = dataprazo2receb.date()

    datahoje = date.today()
    statuses = Status.objects.all()
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    trps = TRP.objects.all()
    licitacoes = Licitacao.objects.all()
    pagamentos = Pagamento.objects.all()
    tipospagto = TipoPagto.objects.all()
    context = {
            'consulta': consulta,
            'consultacompras': consultacompras,
            'consultasede': consultasede,
            'consultacontrat': consultacontrat,
            'consultapagto': consultapagto,
            'consultareceb': consultareceb,
            'status_chave_sol': 'Solicitação - Concluída',
            'status_chave_compras': 'Compras - Concluída',
            'status_chave_sede': 'Sede - Concluída',
            'status_chave_contrat': 'Contratação - Concluída',
            'status_chave_pagto': 'Pagamento - Concluída',
            'status_chave_receb': 'Recebimento - Concluída',
            'statuses': statuses,
            'trps': trps,
            'acoes': acoes,
            'licitacoes': licitacoes,
            'pagamentos': pagamentos,
            'tipospagto': tipospagto,
            'memoriais': memoriais,
            'datahoje': datahoje,
            'dataprazocompras': dataprazocompras,
            'dataprazo1compras': dataprazo1compras,
            'dataprazo2compras': dataprazo2compras,
            'dataprazosede': dataprazosede,
            'dataprazo1sede': dataprazo1sede,
            'dataprazo2sede': dataprazo2sede,
            'dataprazocontrat': dataprazocontrat,
            'dataprazo1contrat': dataprazo1contrat,
            'dataprazo2contrat': dataprazo2contrat,
            'dataprazopagto': dataprazopagto,
            'dataprazo1pagto': dataprazo1pagto,
            'dataprazo2pagto': dataprazo2pagto,
            'dataprazoreceb': dataprazoreceb,
            'dataprazo1receb': dataprazo1receb,
            'dataprazo2receb': dataprazo2receb
    }
    return render(request, 'manutencao_acao_consulta.html', context)


# Função para finalizar o processo de Locação
def finalizarlocacao(request, pk):
    idpassado = pk
    consulta = Locacao_Acao.objects.get(id=idpassado)
    statusfinal = Status.objects.get(descricao='Finalizado')
    print(statusfinal)
    consulta.status_geral = statusfinal
    consulta.save()
    messages.success(request, 'Processo  de locação finalizado com sucesso!')
    return redirect('consultaumalocacao', pk=idpassado)


# Função para finalizar o processo de Aquisicao
def finalizaraquisicao(request, pk):
    idpassado = pk
    consulta = Aquisicao_Acao.objects.get(id=idpassado)
    statusfinal = Status.objects.get(descricao='Finalizado')
    print(statusfinal)
    consulta.status_geral = statusfinal
    consulta.save()
    messages.success(request, 'Processo  de Aquisição finalizado com sucesso!')
    return redirect('consultaumaaquisicao', pk=idpassado)


# Função para finalizar o processo de Aquisicao
def finalizarmanutencao(request, pk):
    idpassado = pk
    consulta = Manutencao_Acao.objects.get(id=idpassado)
    statusfinal = Status.objects.get(descricao='Finalizado')
    print(statusfinal)
    consulta.status_geral = statusfinal
    consulta.save()
    messages.success(request, 'Processo  de Manutenção finalizado'
                              ' com sucesso!')
    return redirect('consultaumamanutencao', pk=idpassado)


# Função para listar locações em Compras
def listloc_compras(request):
    locacoes_compras = Locacao_Acao.objects.filter(
        status_geral__descricao__startswith='Compras')
    tiposlocacao = TipoLocacao.objects.all()
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'locacoes': locacoes_compras,
        'tiposlocacao': tiposlocacao,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'locacao_acao_listview.html', context)


# Função para listas aquisições em Compras
def listaquis_compras(request):
    aquisicao_compras = Aquisicao_Acao.objects.filter(
        status_geral__descricao__startswith='Compras')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'aquisicoes': aquisicao_compras,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'aquisicao_acao_listview.html', context)


# Função para listar aquisições em Compras
def listmanut_compras(request):
    manutencoes_compras = Manutencao_Acao.objects.filter(
        status_geral__descricao__startswith='Compras')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'manutencoes': manutencoes_compras,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'manutencao_acao_listview.html', context)


# Lista locações em Sede
def listloc_sede(request):
    locacoes_sede = Locacao_Acao.objects.filter(
        status_geral__descricao__startswith='Sede')
    tiposlocacao = TipoLocacao.objects.all()
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'locacoes': locacoes_sede,
        'tiposlocacao': tiposlocacao,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'locacao_acao_listview.html', context)


# Lista aquisições em Sede
def listaquis_sede(request):
    aquisicoes_sede = Aquisicao_Acao.objects.filter(
        status_geral__descricao__startswith='Sede')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'aquisicoes': aquisicoes_sede,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'aquisicao_acao_listview.html', context)


# Lista aquisições em Sede
def listmanut_sede(request):
    manutencoes_sede = Manutencao_Acao.objects.filter(
        status_geral__descricao__startswith='Sede')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'manutencoes': manutencoes_sede,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'manutencao_acao_listview.html', context)


# Lista locações em Contrato
def listloc_contr(request):
    locacoes_contr = Locacao_Acao.objects.filter(
        status_geral__descricao__startswith='Contratação')
    tiposlocacao = TipoLocacao.objects.all()
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'locacoes': locacoes_contr,
        'tiposlocacao': tiposlocacao,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'locacao_acao_listview.html', context)


# Lista aquisições em Contrato
def listaquis_contr(request):
    aquisicoes_contr = Aquisicao_Acao.objects.filter(
        status_geral__descricao__startswith='Contratação')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'aquisicoes': aquisicoes_contr,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'aquisicao_acao_listview.html', context)


# Lista manutenções em Contrato
def listmanut_contr(request):
    manutencoes_contr = Manutencao_Acao.objects.filter(
        status_geral__descricao__startswith='Contratação')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'manutencoes': manutencoes_contr,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'manutencao_acao_listview.html', context)


# Lista locações em Pagamento
def listloc_pagto(request):
    locacoes_pagto = Locacao_Acao.objects.filter(
        status_geral__descricao__startswith='Pagamento')
    tiposlocacao = TipoLocacao.objects.all()
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'locacoes': locacoes_pagto,
        'tiposlocacao': tiposlocacao,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'locacao_acao_listview.html', context)


# Lista aquisições em Pagamento
def listaquis_pagto(request):
    aquisicoes_pagto = Aquisicao_Acao.objects.filter(
        status_geral__descricao__startswith='Pagamento')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'aquisicoes': aquisicoes_pagto,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'aquisicao_acao_listview.html', context)


# Lista manutenções em Pagamento
def listmanut_pagto(request):
    manutencoes_pagto = Manutencao_Acao.objects.filter(
        status_geral__descricao__startswith='Pagamento')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'manutencoes': manutencoes_pagto,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'manutencao_acao_listview.html', context)


# Lista locações em Cronograma
def listloc_crono(request):
    locacoes_crono = Locacao_Acao.objects.filter(
        status_geral__descricao__startswith='Recebimento')
    tiposlocacao = TipoLocacao.objects.all()
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'locacoes': locacoes_crono,
        'tiposlocacao': tiposlocacao,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'locacao_acao_listview.html', context)


# Lista aquisicoes em Cronograma
def listaquis_crono(request):
    aquisicoes_crono = Aquisicao_Acao.objects.filter(
        status_geral__descricao__startswith='Recebimento')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'aquisicoes': aquisicoes_crono,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'aquisicao_acao_listview.html', context)


# Lista manutencoes em Cronograma
def listmanut_crono(request):
    manutencoes_crono = Manutencao_Acao.objects.filter(
        status_geral__descricao__startswith='Recebimento')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'manutencoes': manutencoes_crono,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'manutencao_acao_listview.html', context)


# Lista locações em Finalizados
def listloc_fin(request):
    locacoes_fin = Locacao_Acao.objects.filter(
        status_geral__descricao__startswith='Finalizado')
    tiposlocacao = TipoLocacao.objects.all()
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'locacoes': locacoes_fin,
        'tiposlocacao': tiposlocacao,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'locacao_acao_listview.html', context)


# Lista aquisições em Finalizados
def listaquis_fin(request):
    aquisicoes_fin = Aquisicao_Acao.objects.filter(
        status_geral__descricao__startswith='Finalizado')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'aquisicoes': aquisicoes_fin,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'aquisicao_acao_listview.html', context)


# Lista manutencoes em Finalizados
def listmanut_fin(request):
    manutencoes_fin = Manutencao_Acao.objects.filter(
        status_geral__descricao__startswith='Finalizado')
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {
        'manutencoes': manutencoes_fin,
        'acoes': acoes,
        'memoriais': memoriais,
        'statuses': statuses
    }
    return render(request, 'manutencao_acao_listview.html', context)


def defcomprasupdumalocacao(request, pk):
    idpassado = pk
    consultacompras = Compras_Locacao.objects.get(locacao=idpassado)
    context = {
        'consultacompras': consultacompras,
    }
    return render(request, 'form_upd_compras.html', context)


def defcomprasupdumaaquisicao(request, pk):
    idpassado = pk
    consultacompras = Compras_Aquisicao.objects.get(aquisicao=idpassado)
    context = {
        'consultacompras': consultacompras,
    }
    return render(request, 'form_upd_compras_aquisicao.html', context)


def defcomprasupdumamanutencao(request, pk):
    idpassado = pk
    consultacompras = Compras_Manutencao.objects.get(manutencao=idpassado)
    context = {
        'consultacompras': consultacompras,
    }
    return render(request, 'form_upd_compras_manutencao.html', context)


# View para atualizar Compras Locacao
class UpdComprasLocacaoView(UpdateView):
    model = Compras_Locacao
    template_name = 'locacao_acao_consulta.html'
    fields = ['descricao', 'numero', 'data', 'observacoes',
              'locacao', 'trp', 'status', 'sede']
    context_object_name = 'consultacompras'
    success_url = reverse_lazy('list_loc')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_chave_sol'] = 'Solicitação - Concluída'
        context['status_compras_emaprov'] = 'Compras - Em Aprovação'
        context['status_compras_emorc'] = 'Compras - Aguardando orçamento'
        context['status_compras_orc'] = 'Compras - Orçado'
        return context

    def post(self, request, *args, **kwargs):
        form = ComprasLocacaoModelForm(request.POST)
        if form.is_valid():
            loc = form.cleaned_data['locacao']
            print(loc)
            locacao = Locacao_Acao.objects.get(descricao=loc)
            locacao.status_geral = form.cleaned_data['status']
            locacao.save()
            super(UpdComprasLocacaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em compras'
                                      ' atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[locacao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Compras Aquisição
class UpdComprasAquisicaoView(UpdateView):
    model = Compras_Aquisicao
    template_name = 'aquisicao_acao_consulta.html'
    fields = ['descricao', 'numero', 'data', 'observacoes',
              'aquisicao', 'trp', 'status', 'sede']
    context_object_name = 'consultacompras'
    success_url = reverse_lazy('list_aquis')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_chave_sol'] = 'Solicitação - Concluída'
        context['status_compras_emaprov'] = 'Compras - Em Aprovação'
        context['status_compras_emorc'] = 'Compras - Aguardando orçamento'
        context['status_compras_orc'] = 'Compras - Orçado'
        return context

    def post(self, request, *args, **kwargs):
        form = ComprasAquisicaoModelForm(request.POST)
        if form.is_valid():
            aquis = form.cleaned_data['aquisicao']
            print(aquis)
            aquisicao = Aquisicao_Acao.objects.get(descricao=aquis)
            aquisicao.status_geral = form.cleaned_data['status']
            aquisicao.save()
            super(UpdComprasAquisicaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo de aquisição em compras'
                                      ' atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquisicao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Compras em Manutenção
class UpdComprasManutencaoView(UpdateView):
    model = Compras_Manutencao
    template_name = 'manutencao_acao_consulta.html'
    fields = ['descricao', 'numero', 'data', 'observacoes',
              'manutencao', 'trp', 'status', 'sede']
    context_object_name = 'consultacompras'
    success_url = reverse_lazy('list_manut')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_chave_sol'] = 'Solicitação - Concluída'
        context['status_compras_emaprov'] = 'Compras - Em Aprovação'
        context['status_compras_emorc'] = 'Compras - Aguardando orçamento'
        context['status_compras_orc'] = 'Compras - Orçado'
        return context

    def post(self, request, *args, **kwargs):
        form = ComprasManutencaoModelForm(request.POST)
        if form.is_valid():
            manut = form.cleaned_data['manutencao']
            print(manut)
            manutencao = Manutencao_Acao.objects.get(descricao=manut)
            manutencao.status_geral = form.cleaned_data['status']
            manutencao.save()
            super(UpdComprasManutencaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo de aquisição em compras'
                                      ' atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manutencao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Sede em Locações
class UpdSedeView(UpdateView):
    model = Sede
    template_name = 'locacao_acao_consulta.html'
    fields = ['descricao', 'numero', 'dataminuta', 'datadca',
              'anotacoes', 'licitacao', 'locacao', 'status']
    success_url = reverse_lazy('list_loc')
    context_object_name = 'consultasede'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Sede cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = SedeModelForm(request.POST)
        if form.is_valid():
            loc = form.cleaned_data['locacao']
            print(loc)
            locacao = Locacao_Acao.objects.get(descricao=loc)
            locacao.status_geral = form.cleaned_data['status']
            locacao.save()
            super(UpdSedeView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Sede '
                                      'atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[locacao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Sede em Aquisições
class UpdSedeAquisicaoView(UpdateView):
    model = Sede_Aquisicao
    template_name = 'aquisicao_acao_consulta.html'
    fields = ['descricao', 'numero', 'dataminuta', 'datadca',
              'anotacoes', 'licitacao', 'aquisicao', 'status']
    success_url = reverse_lazy('list_aquis')
    context_object_name = 'consultasede'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Sede cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = SedeAquisicaoModelForm(request.POST)
        if form.is_valid():
            aquis = form.cleaned_data['aquisicao']
            print(aquis)
            aquisicao = Aquisicao_Acao.objects.get(descricao=aquis)
            aquisicao.status_geral = form.cleaned_data['status']
            aquisicao.save()
            super(UpdSedeAquisicaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Sede '
                                      'atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquisicao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Sede em Manutenções
class UpdSedeManutencaoView(UpdateView):
    model = Sede_Manutencao
    template_name = 'manutencao_acao_consulta.html'
    fields = ['descricao', 'numero', 'dataminuta', 'datadca',
              'anotacoes', 'licitacao', 'manutencao', 'status']
    success_url = reverse_lazy('list_manut')
    context_object_name = 'consultasede'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Sede cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = SedeManutencaoModelForm(request.POST)
        if form.is_valid():
            manut = form.cleaned_data['manutencao']
            print(manut)
            manutencao = Aquisicao_Acao.objects.get(descricao=manut)
            manutencao.status_geral = form.cleaned_data['status']
            manutencao.save()
            super(UpdSedeManutencaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Sede '
                                      'atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manutencao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Contratos em Locações
class UpdContratView(UpdateView):
    model = Contrato_Locacao
    template_name = 'locacao_acao_consulta.html'
    fields = ['descricao', 'processo', 'dataprocesso',
              'instrcontratual',
              'datacontrato', 'valorservico',
              'valorlocacao', 'locacao', 'status']
    success_url = reverse_lazy('list_loc')
    context_object_name = 'consultacontrat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Contratação cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = ContratoLocacaoModelForm(request.POST)
        if form.is_valid():
            loc = form.cleaned_data['locacao']
            print(loc)
            locacao = Locacao_Acao.objects.get(descricao=loc)
            locacao.status_geral = form.cleaned_data['status']
            locacao.save()
            super(UpdContratView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Contratação '
                                      'atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[locacao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Contratos em Aquisições
class UpdContratAquisicaoView(UpdateView):
    model = Contrato_Aquisicao
    template_name = 'aquisicao_acao_consulta.html'
    fields = ['descricao', 'processo', 'dataprocesso', 'instrcontratual',
              'datacontrato', 'valorservico',
              'valorlocacao', 'aquisicao', 'status']
    success_url = reverse_lazy('list_aquis')
    context_object_name = 'consultacontrat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Contratação cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = ContratoAquisicaoModelForm(request.POST)
        if form.is_valid():
            aquis = form.cleaned_data['aquisicao']
            print(aquis)
            aquisicao = Aquisicao_Acao.objects.get(descricao=aquis)
            aquisicao.status_geral = form.cleaned_data['status']
            aquisicao.save()
            super(UpdContratAquisicaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Contratação'
                                      ' atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquisicao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Contratos em Manutenções
class UpdContratManutencaoView(UpdateView):
    model = Contrato_Manutencao
    template_name = 'manutencao_acao_consulta.html'
    fields = ['descricao', 'processo', 'dataprocesso', 'instrcontratual',
              'datacontrato', 'valorservico',
              'valorlocacao', 'manutencao', 'status']
    success_url = reverse_lazy('list_manut')
    context_object_name = 'consultacontrat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Contratação cadastrado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = ContratoManutencaoModelForm(request.POST)
        if form.is_valid():
            manut = form.cleaned_data['manutencao']
            print(manut)
            manutencao = Manutencao_Acao.objects.get(descricao=manut)
            manutencao.status_geral = form.cleaned_data['status']
            manutencao.save()
            super(UpdContratManutencaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Contratação '
                                      'atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manutencao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Pagamentos em Locações
class UpdPagtoView(UpdateView):
    model = Pagamento
    template_name = 'locacao_acao_consulta.html'
    fields = ['descricao', 'tipo_pagto', 'atividade', 'parcela',
              'qtde_parcelas', 'valor', 'dataprevnota',
              'tiponota', 'numnota', 'dataemissnota', 'serienota',
              'xml', 'anotacoes', 'locacao', 'status']
    success_url = reverse_lazy('list_loc')
    context_object_name = 'consultapagto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Pagamento atualizado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = PagamentoModelForm(request.POST)
        if form.is_valid():
            loc = form.cleaned_data['locacao']
            print(loc)
            locacao = Locacao_Acao.objects.get(descricao=loc)
            locacao.status_geral = form.cleaned_data['status']
            locacao.save()
            super(UpdPagtoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Pagamento '
                                      'atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[locacao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Pagamentos em Locações
class UpdPagtoAquisicaoView(UpdateView):
    model = Pagamento_Aquisicao
    template_name = 'aquisicao_acao_consulta.html'
    fields = ['descricao', 'tipo_pagto', 'atividade', 'parcela',
              'qtde_parcelas', 'valor', 'dataprevnota',
              'tiponota', 'numnota', 'dataemissnota', 'serienota',
              'xml', 'anotacoes', 'aquisicao', 'status']
    success_url = reverse_lazy('list_aquis')
    context_object_name = 'consultapagto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Pagamento atualizado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = PagamentoAquisicaoModelForm(request.POST)
        if form.is_valid():
            aquis = form.cleaned_data['aquisicao']
            print(aquis)
            aquisicao = Aquisicao_Acao.objects.get(descricao=aquis)
            aquisicao.status_geral = form.cleaned_data['status']
            aquisicao.save()
            super(UpdPagtoAquisicaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Pagamento '
                                      'atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquisicao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Pagamentos em Manutenções
class UpdPagtoManutencaoView(UpdateView):
    model = Pagamento_Manutencao
    template_name = 'manutencao_acao_consulta.html'
    fields = ['descricao', 'tipo_pagto', 'atividade', 'parcela',
              'qtde_parcelas', 'valor', 'dataprevnota',
              'tiponota', 'numnota', 'dataemissnota', 'serienota',
              'xml', 'anotacoes', 'manutencao', 'status']
    success_url = reverse_lazy('list_manut')
    context_object_name = 'consultapagto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Pagamento atualizado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = PagamentoManutencaoModelForm(request.POST)
        if form.is_valid():
            manut = form.cleaned_data['manutencao']
            print(manut)
            manutencao = Manutencao_Acao.objects.get(descricao=manut)
            manutencao.status_geral = form.cleaned_data['status']
            manutencao.save()
            super(UpdPagtoManutencaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Pagamento'
                                      ' atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manutencao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Cronograma em Locações
class UpdCronoView(UpdateView):
    model = Cronograma
    fields = ['locacao', 'atividade', 'datainicio',
              'datafim', 'anotacoes', 'status']
    template_name = 'locacao_acao_consulta.html'
    success_url = reverse_lazy('list_loc')
    context_object_name = 'consultareceb'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Recebimento atualizado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = CronogramaModelForm(request.POST)
        if form.is_valid():
            loc = form.cleaned_data['locacao']
            print(loc)
            locacao = Locacao_Acao.objects.get(descricao=loc)
            locacao.status_geral = form.cleaned_data['status']
            locacao.save()
            super(UpdCronoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Recebimento'
                                      ' atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumalocacao',
                                                     args=[locacao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Cronograma em Aquisições
class UpdCronoAquisicaoView(UpdateView):
    model = Cronograma_Aquisicao
    fields = ['aquisicao', 'atividade', 'datainicio',
              'datafim', 'anotacoes', 'status']
    template_name = 'aquisicao_acao_consulta.html'
    success_url = reverse_lazy('list_aquis')
    context_object_name = 'consultareceb'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Recebimento atualizado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = CronogramaAquisicaoModelForm(request.POST)
        if form.is_valid():
            aquis = form.cleaned_data['aquisicao']
            print(aquis)
            aquisicao = Locacao_Acao.objects.get(descricao=aquis)
            aquisicao.status_geral = form.cleaned_data['status']
            aquisicao.save()
            super(UpdCronoAquisicaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Recebimento '
                                      'atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumaaquisicao',
                                                     args=[aquisicao.id]))
        return render(request, 'resultado.html', {'form': form})


# View para atualizar Cronograma em Manutenções
class UpdCronoManutencaoView(UpdateView):
    model = Cronograma_Manutencao
    fields = ['manutencao', 'atividade', 'datainicio',
              'datafim', 'anotacoes', 'status']
    template_name = 'manutencao_acao_consulta.html'
    success_url = reverse_lazy('list_manut')
    context_object_name = 'consultareceb'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Processo em Recebimento atualizado com sucesso!"

    def post(self, request, *args, **kwargs):
        form = CronogramaManutencaoModelForm(request.POST)
        if form.is_valid():
            manut = form.cleaned_data['manutencao']
            print(manut)
            manutencao = Manutencao_Acao.objects.get(descricao=manut)
            manutencao.status_geral = form.cleaned_data['status']
            manutencao.save()
            super(UpdCronoManutencaoView, self).post(request, **kwargs)
            messages.success(request, 'Processo em Recebimento '
                                      'atualizado com sucesso')
            return HttpResponseRedirect(reverse_lazy('consultaumamanutencao',
                                                     args=[manutencao.id]))
        return render(request, 'resultado.html', {'form': form})


def resultloc(request, id):
    idpassado = id
    context = {
        'id': idpassado,
    }
    return render(request, 'resultado.html', context)


def resultaquis(request, id):
    idpassado = id
    context = {
        'id': idpassado,
    }
    return render(request, 'resultado.html', context)


def resultmanut(request, id):
    idpassado = id
    context = {
        'id': idpassado,
    }
    return render(request, 'resultado.html', context)


# Insere solicitação de Aquisição
def add_aquisicao(request):
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {'acoes': acoes,
               'memoriais': memoriais,
               'statuses': statuses
               }

    return render(request, 'form_solicit_aquisicao.html', context)


# Insere solicitação de Manutenção
def add_manut(request):
    acoes = Acao.objects.all()
    memoriais = Memorial.objects.all()
    statuses = Status.objects.all()

    context = {'acoes': acoes,
               'memoriais': memoriais,
               'statuses': statuses
               }

    return render(request, 'form_solicit_manut.html', context)
