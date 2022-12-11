from django.urls import path

from characters.views import (CollectionCreateView, CollectionDetailView,
                              CollectionListView)

app_name = "characters"

urlpatterns = [
    path("collections/", CollectionListView.as_view(), name="collections"),
    path(
        "create-collections/", CollectionCreateView.as_view(), name="create-collections"
    ),
    path(
        "collections/<int:pk>/",
        CollectionDetailView.as_view(),
        name="detail-collections",
    ),
]
