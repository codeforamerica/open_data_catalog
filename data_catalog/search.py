"""Search functionality for the data catalog."""

from data_catalog.models import App, Data, Idea, Tag


class Search(object):

    """
    This class has static methods used to search through the models for
    matching instances.

    >>> Search.find_resources('keyword')

    You can also categorize results -- therefore looking for all apps, data, or
    ideas with a specific tag.

    >>> Search.category('apps', 'tag')
    """

    @staticmethod
    def find_resources(keyword):
        """
        Return all resources linked to a tag. If the tag is not found,
        search through App, Data, and Idea models for instances that contain
        the keyword in their name.
        """
        results = {}
        try:
            tag = Tag.objects.select_related().get(name__iexact=keyword)
        except Tag.DoesNotExist:
            results['apps'] = App.objects.filter(name__icontains=keyword)
            results['data'] = Data.objects.filter(name__icontains=keyword)
            results['ideas'] = Idea.objects.filter(name__icontains=keyword)
        else:
            results['apps'] = tag.apps.all()
            results['data'] = tag.data.all()
            results['ideas'] = tag.ideas.all()
        return results

    @staticmethod
    def category(related_name, tag):
        """
        Given the model `related_name` attribute of the Tag model (apps, ideas,
        data), this function will check to see if a specific tag can be found.
        If not, all of the available records of the `related_name` model are
        returned.
        """
        available_models = {'apps': App, 'data': Data, 'ideas': Idea}
        if related_name not in available_models:
            results = None
        elif tag:
            try:
                tag_model = Tag.objects.get(name=tag)
                results = getattr(tag_model, related_name).all()
            except:
                results = []
        else:
            model = available_models[related_name]
            results = model.objects.all()
        context = {'results': results}
        return context
