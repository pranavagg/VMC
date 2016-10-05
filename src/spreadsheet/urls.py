from django.conf.urls import url
import views

urlpatterns = [
    url(r'^display/(?P<sheet_id>[0-9]+)/$', views.display_sheet, name='display_sheet'),
    url(r'^add_column/(?P<sheet_id>[0-9]+)/$', views.add_column, name='add_column'),
    url(r'^delete_column/(?P<sheet_id>[0-9]+)/$', views.delete_column, name='delete_column'),
    url(r'^add_row/(?P<sheet_id>[0-9]+)/$', views.add_row, name='add_row'),
    url(r'^delete_row/(?P<sheet_id>[0-9]+)/$', views.delete_row, name='delete_row'),
    url(r'^edit_row/(?P<sheet_id>[0-9]+)/(?P<row_id>[0-9]+)/$', views.edit_row, name='edit_row'),
]
