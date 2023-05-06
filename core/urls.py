from django.urls import path

import core.views
from .views import IndexView, SistemaView, \
                   ConsultaLocacaoAcaoView, \
                   CreateSedeView, CreateLicView, \
                   CreateContrView, CreateCronoView,\
                   CreateAcaoView, CreateTipoLocView,\
                   CreateMemorialView, CreateTRPView, \
                   CreateOrcView, CreatePagtoView,\
                   CreateAprovView, CreateFornecView, CreateCatFornecView, \
                   CreateEndFornecView, CreateContFornecView,\
                   CreateStatusView, CreateTipoStatusView, CreateLocalView,\
                   CreateProjetoView, CreateLinguagemView,\
                   CreateTipoPagtoView, \
                   LocacaoAPIView,\
                   TipoLocacaoAPIView, LocacaoViewSet,\
                   LocalViewSet, LinguagemViewSet, ProjetoViewSet, \
                   AcaoViewSet, StatusViewSet, \
                   TipoLocacaoViewSet, ConsultaAquisicaoAcaoView,\
                   ConsultaManutencaoAcaoView, \
                   FornecedorAPIView, FornecedorViewSet, \
                   CreateSedeAquisicaoView, CreateSedeManutencaoView, \
                   CreateContrAquisicaoView, CreateContrManutencaoView,\
                   CreatePagtoAquisicaoView, CreatePagtoManutencaoView,\
                   CreateCronoAquisicaoView, CreateCronoManutencaoView, \
                   CentralAjudaView, FaqsView, ManualSistemaView,\
                   AquisicaoViewSet, \
                   ManutencaoViewSet


from rest_framework.routers import SimpleRouter

from . import views
from django.conf import settings
from django.conf.urls.static import static

router = SimpleRouter()
router.register('locacoes', LocacaoViewSet)
router.register('aquisicoes', AquisicaoViewSet)
router.register('manutencoes', ManutencaoViewSet)
router.register('tipolocacoes', TipoLocacaoViewSet)
router.register('fornecedores', FornecedorViewSet)
router.register('locais', LocalViewSet)
router.register('linguagens', LinguagemViewSet)
router.register('projetos', ProjetoViewSet)
router.register('acoes', AcaoViewSet)
router.register('status', StatusViewSet)


urlpatterns = [
    path('grafico_solicitacoes/', views.piechart, name='piechart'),

    # URLS para APIs
    path('locacoes/', LocacaoAPIView.as_view(), name='locacoes'),
    path('tipolocacoes/', TipoLocacaoAPIView.as_view(), name='tipolocacoes'),
    path('fornecedores/', FornecedorAPIView.as_view(), name='fornecedores'),

    # URLS para página inicial do sistema e central de ajuda
    path('', IndexView.as_view(), name='index'),
    path('sistema/', SistemaView.as_view(), name='sistema'),
    path('central_de_ajuda', CentralAjudaView.as_view(),
         name='centralajuda'),
    path('faqs/', FaqsView.as_view(), name='faqs'),
    path('manualsistema/', ManualSistemaView.as_view(),
         name='manualsistema'),

    # URLs de inserção de solicitações
    path('add/', core.views.CreateSolicitView.as_view(),
         name='add_loc'),
    path('add_aquisicao/', core.views.CreateAquisicaoView.as_view(),
         name='add_aquisicao'),
    path('add_manut/', core.views.CreateManutencaoView.as_view(),
         name='add_manut'),

    # URLs de listar as solicitações
    path('listlocacoes/', core.views.ListLocacaoAcaoView.as_view(),
         name='list_loc'),
    path('listaquisicoes/', core.views.ListAquisicaoAcaoView.as_view(),
         name='list_aquis'),
    path('listmanutencoes/', core.views.ListManutencaoAcaoView.as_view(),
         name='list_manut'),

    # URLs de listar as solicitaçoes em Compras
    path('listloc_compras/', core.views.listloc_compras,
         name='listloc_compras'),
    path('listaquis_compras/', core.views.listaquis_compras,
         name='listaquis_compras'),
    path('listmanut_compras/', core.views.listmanut_compras,
         name='listmanut_compras'),

    # URLs de listar as solicitaçoes em Contratação
    path('listloc_contr/', core.views.listloc_contr,
         name='listloc_contr'),

    # URLs de listar as solicitaçoes em Pagamento
    path('listloc_pagto/', core.views.listloc_pagto,
         name='listloc_pagto'),

    # URLs de listar as solicitaçoes em Cronograma
    path('listloc_crono/', core.views.listloc_crono,
         name='listloc_crono'),

    # URLs de listar as solicitaçoes em Finalizados
    path('listloc_fin/', core.views.listloc_fin,
         name='listloc_fin'),

    # URLs para consultar solicitações
    path('<int:pk>/consultalocacao/', ConsultaLocacaoAcaoView.as_view(),
         name='cons_loc'),
    path('<int:pk>/consultaaquisicao/', ConsultaAquisicaoAcaoView.as_view(),
         name='cons_aquis'),
    path('<int:pk>/consultamanutencao/', ConsultaManutencaoAcaoView.as_view(),
         name='cons_manut'),

    path('add_acao/', CreateAcaoView.as_view(),
         name='add_acao'),
    path('add_tipoloc/', CreateTipoLocView.as_view(),
         name='add_tipoloc'),
    path('add_memorial/', CreateMemorialView.as_view(),
         name='add_memorial'),

    # URLs para adicionar compras nos processos
    path('add_comprasloc/', core.views.CreateComprasLocView.as_view(),
         name='add_comprasloc'),
    path('add_comprasaquis/', core.views.CreateComprasAquisView.as_view(),
         name='add_comprasaquis'),
    path('add_comprasmanut/', core.views.CreateComprasManutView.as_view(),
         name='add_comprasmanut'),


    path('add_trp/', CreateTRPView.as_view(),
         name='add_trp'),
    path('add_orc/', CreateOrcView.as_view(),
         name='add_orc'),

    # URLs para adicionar Sede nos processos
    path('add_sede/', CreateSedeView.as_view(),
         name='add_sede'),
    path('add_sede_aquis/', CreateSedeAquisicaoView.as_view(),
         name='add_sede_aquis'),
    path('add_sede_manut/', CreateSedeManutencaoView.as_view(),
         name='add_sede_aquis'),

    # URLs para adicionar Contratação nos processos
    path('add_contr/', CreateContrView.as_view(),
         name='add_contr'),
    path('add_contr_aquis/', CreateContrAquisicaoView.as_view(),
         name='add_contr_aquis'),
    path('add_contr_manut/', CreateContrManutencaoView.as_view(),
         name='add_contr_manut'),

    # URLs para adicionar Pagamento nos processos
    path('add_pagto/', CreatePagtoView.as_view(),
         name='add_pagto'),
    path('add_pagto_aquis/', CreatePagtoAquisicaoView.as_view(),
         name='add_pagto_aquis'),
    path('add_pagto_manut/', CreatePagtoManutencaoView.as_view(),
         name='add_pagto_manut'),

    # URLs para adicionar Cronograma nos processos
    path('add_crono/', CreateCronoView.as_view(),
         name='add_crono'),
    path('add_crono_aquis/', CreateCronoAquisicaoView.as_view(),
         name='add_crono_aquis'),
    path('add_crono_manut/', CreateCronoManutencaoView.as_view(),
         name='add_crono_manut'),

    path('add_lic/', CreateLicView.as_view(),
         name='add_lic'),
    path('add_aprov/', CreateAprovView.as_view(),
         name='add_aprov'),
    path('add_fornec/', CreateFornecView.as_view(),
         name='add_fornec'),
    path('add_catfornec/', CreateCatFornecView.as_view(),
         name='add_catfornec'),
    path('add_endfornec/', CreateEndFornecView.as_view(),
         name='add_endfornec'),
    path('add_contfornec/', CreateContFornecView.as_view(),
         name='add_contfornec'),
    path('add_status/', CreateStatusView.as_view(),
         name='add_status'),
    path('add_tipostatus/', CreateTipoStatusView.as_view(),
         name='add_tipostatus'),
    path('add_local/', CreateLocalView.as_view(),
         name='add_local'),
    path('add_linguagem/', CreateLinguagemView.as_view(),
         name='add_linguagem'),
    path('add_projeto/', CreateProjetoView.as_view(),
         name='add_projeto'),
    path('add_tipopagto/', CreateTipoPagtoView.as_view(),
         name='add_tipopagto'),

    # URLs para salvar dados dos modais
    path('salvamemorial', core.views.salvamemorial,
         name='salvamemorial'),
    path('salvaprojeto', core.views.salvaprojeto,
         name='salvaprojeto'),
    path('salvatipoloc', core.views.salvatipoloc,
         name='salvatipoloc'),

    # URLs para consultar solicitacoes
    path('consultalocacao',
         core.views.consultalocacao,
         name='consultalocacao'),
    path('consultaaquisicao',
         core.views.consultaaquisicao,
         name='consultaaquisicao'),
    path('consultamanutencao',
         core.views.consultamanutencao,
         name='consultamanutencao'),

    # URLs para finalizar as solicitações
    path('finalizarlocacao/<int:pk>',
         core.views.finalizarlocacao,
         name='finalizarlocacao'),
    path('finalizaraquisicao/<int:pk>',
         core.views.finalizaraquisicao,
         name='finalizaraquisicao'),
    path('finalizarmanutencao/<int:pk>',
         core.views.finalizarmanutencao,
         name='finalizarmanutencao'),

    path('resultloc/<int:id>', core.views.resultloc,
         name='resultloc'),


    # URLs para atualizar processos em compras
    path('updatecompras/<int:pk>/',
         core.views.UpdComprasLocacaoView.as_view(),
         name='updatecompras'),
    path('updatecomprasaquis/<int:pk>/',
         core.views.UpdComprasAquisicaoView.as_view(),
         name='updatecomprasaquis'),
    path('updatecomprasmanut/<int:pk>/',
         core.views.UpdComprasManutencaoView.as_view(),
         name='updatecomprasmanut'),

    path('updatesede/<int:pk>/',
         core.views.UpdSedeView.as_view(),
         name='updatesede'),
    path('updatesedeaquis/<int:pk>/',
         core.views.UpdSedeAquisicaoView.as_view(),
         name='updatesedeaquis'),
    path('updatesedemanut/<int:pk>/',
         core.views.UpdSedeManutencaoView.as_view(),
         name='updatesedemanut'),

    path('updatecontrat/<int:pk>/',
         core.views.UpdContratView.as_view(),
         name='updatecontrat'),
    path('updatecontrataquis/<int:pk>/',
         core.views.UpdContratAquisicaoView.as_view(),
         name='updatecontrataquis'),
    path('updatecontratmanut/<int:pk>/',
         core.views.UpdContratManutencaoView.as_view(),
         name='updatecontratmanut'),

    path('updatepagto/<int:pk>/',
         core.views.UpdPagtoView.as_view(),
         name='updatepagto'),
    path('updatepagtoaquis/<int:pk>/',
         core.views.UpdPagtoAquisicaoView.as_view(),
         name='updatepagtoaquis'),
    path('updatepagtomanut/<int:pk>/',
         core.views.UpdPagtoManutencaoView.as_view(),
         name='updatepagtomanut'),

    path('updatecrono/<int:pk>/',
         core.views.UpdCronoView.as_view(), name='updatecrono'),
    path('updatecronoaquis/<int:pk>/',
         core.views.UpdCronoAquisicaoView.as_view(), name='updatecronoaquis'),
    path('updatecronomanut/<int:pk>/',
         core.views.UpdCronoManutencaoView.as_view(), name='updatecronomanut'),

    # URLs para consultar uma unica solicitacao
    path('consultaumalocacao/<int:pk>/', core.views.consultaumalocacao,
         name='consultaumalocacao'),
    path('consultaumaaquisicao/<int:pk>/', core.views.consultaumaaquisicao,
         name='consultaumaaquisicao'),
    path('consultaumamanutencao/<int:pk>/', core.views.consultaumamanutencao,
         name='consultaumamanutencao')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
