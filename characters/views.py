import petl
from django.contrib import messages
from django.core.files import File
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from characters.clients import SwapiClient
from characters.models import Collection
from utils.exceptions import EndpointTimeout, UnexpectedApiError


class CollectionListView(ListView):
    model = Collection
    paginate_by = 10
    ordering = "-id"


class CollectionCreateView(View):
    model = Collection
    client = SwapiClient()

    def get(self, request, *args, **kwargs):
        self.post(request)
        return HttpResponseRedirect(reverse("characters:collections"))

    def post(self, request, *args, **kwargs) -> None:
        try:
            csv_file = self.client.create_characters_csv()
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
        client = SwapiClient(csv_file=self.object.csv)

        limit = int(self.request.GET.get("limit", self.paginate_by))
        table = client.get_characters_table()
        object_list = table.data().tail(limit - 1)

        context["headers"] = table[0]
        context["table"] = object_list
        context["load_more"] = len(object_list) == limit
        return context


class CollectionDetailAggregateView(DetailView):
    model = Collection
    template_name = "characters/collection_detail_aggregate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = SwapiClient(csv_file=self.object.csv)

        table = client.get_characters_table()
        aggregate_params = self.request.GET.getlist("agg")
        object_list = self._get_object_list(aggregate_params, table)

        context["aggregate"] = self._get_aggregate_buttons(aggregate_params, table)
        context["headers"] = object_list[0]
        context["table"] = object_list.data()

        return context

    def _get_aggregate_buttons(
        self, aggregate_params: list, table: petl.Table
    ) -> list[tuple[str, str]]:
        return [
            (element, "active") if element in aggregate_params else (element, "")
            for element in table[0]
        ]

    def _get_object_list(
        self, aggregate_params: list[str], table: petl.Table
    ) -> list[petl.Table]:
        if aggregate_params := self._aggregate_params_validation(
            aggregate_params, table
        ):
            return table.aggregate([*aggregate_params], len)
        else:
            return table

    def _aggregate_params_validation(
        self, aggregate_params: list[str], table: petl.Table
    ) -> list[str]:
        return [param for param in aggregate_params if param in table[0]]
