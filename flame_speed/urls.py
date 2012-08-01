from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'flame_speed.views.home', name='home'),  
                       url(r'^home/$', 'flame_speed.views.home', name='home'), 
                       url(r'^data/$', 'flame_speed.views.data', name='data'),
                       url(r'^characteristic/$', 'flame_speed.views.characteristic', name='characteristic'),
                       url(r'^reference/$', 'flame_speed.views.reference', name='reference'),
                       url(r'^mixture/$', 'flame_speed.views.mixture', name='mixture'),
                       url(r'^graph/$', 'flame_speed.views.graph', name='graph'),
                       url(r'^display_graph/$', 'flame_speed.views.display_graph', name='display_graph'),
                       url(r'^H2/$', 'flame_speed.views.H2', name='H2'),
                       url(r'^H2_equivalence_ratio/$', 'flame_speed.views.H2_equivalence_ratio', name='H2_equivalence_ratio'),
                       url(r'^H2_equivalence_ratio_ref6/$', 'flame_speed.views.H2_equivalence_ratio_ref6', name='H2_equivalence_ratio_ref6'),                       
                       url(r'^reference/populate_reference/$', 'flame_speed.views.populate_reference', name='populate_reference'),  
                       url(r'^characteristic/characteristic/$', 'flame_speed.views.characteristic', name='characteristic'), 
                       url(r'^mixture/populate_mixture_characteristic/$', 'flame_speed.views.populate_mixture_characteristic', name='populate_mixture_characteristic'),                                           
)
