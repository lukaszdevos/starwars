import petl
from django.contrib import messages
from django.core.files import File
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin

from characters.clients import SwapiClient
from characters.models import Collection
from utils.exceptions import EndpointTimeout, UnexpectedApiError


class CollectionListView(ListView):
    model = Collection
    paginate_by = 10
    ordering = "-id"


class CollectionCreateView(View):
    model = Collection

    def get(self, request, *args, **kwargs):
        self.post(request)
        return HttpResponseRedirect(reverse("characters:collections"))

    def post(self, request, *args, **kwargs) -> None:
        client = SwapiClient()
        try:
            csv_file = client.create_characters_csv()
            Collection.objects.create(csv=File(csv_file))
            csv_file.close()
            messages.success(request, "Successful fetched collection")
        except (EndpointTimeout, UnexpectedApiError) as error:
            messages.error(request, error)
        return


class CollectionDetailView(DetailView):
    model = Collection
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        limit = int(self.request.GET.get("limit", self.paginate_by))
        table = petl.fromcsv(self.object.csv)
        object_list = table.data().tail(limit - 1)
        
        context["headers"] = table[0]
        context["table"] = object_list
        context["load_more"] = len(object_list) == limit
        return context
