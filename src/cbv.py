from src.conf import code_success
from src.render import render


class TemplateView:

    template = "template.html"

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template

    def render(self):
        template = self.get_template()
        context = self.get_context_data()
        return code_success, render(template, **context)

    def __call__(self, request):
        return self.render()


class ListView(TemplateView):
    queryset = []
    template = "list.html"
    context_object_name = "objects_list"

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template = "create.html"

    @staticmethod
    def get_request_data(request: dict) -> dict:
        return request["data"]

    def create_object(self, data: dict):
        pass

    def __call__(self, request: dict):
        if request["method"] == "POST":

            data = self.get_request_data(request)
            self.create_object(data)

            return self.render()
        else:
            return super().__call__(request)
