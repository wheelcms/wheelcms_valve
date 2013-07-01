from twotest.util import create_request

from wheelcms_axle.node import Node

from wheelcms_axle.tests.test_spoke import BaseLocalRegistry
from wheelcms_axle.tests.test_handler import MainHandlerTestable

from ..models import ValveBlog, ValveBlogType
from ..models import ValveEntry, ValveEntryType

from ..models import blog_context, global_blog_context


class TestContext(BaseLocalRegistry):
    """
        Test the context methods that provide the template context
        for the global / content blog view
    """
    types = (ValveBlogType, ValveEntryType)

    def test_context_on_blog(self, client):
        """ should find published entries, several levels deep """
        root = Node.root()
        _ = ValveBlog(node=root, state="published").save()
        _ = ValveEntry(node=root.add("e1"), state="published").save()
        _ = ValveEntry(node=root.add("e2"), state="published").save()
        _ = ValveEntry(node=root.add("e3"), state="private").save()

        request = create_request("GET", "/", data={})

        handler = MainHandlerTestable(request=request, instance=root)
        ctx = blog_context(handler, request, root)

        assert 'paginator' in ctx
        res = ctx['paginator'].object_list
        assert len(res) == 2
        assert set(x.slug() for x in res) == set(("e1", "e2"))

    def test_context_global(self, client):
        """ collect global entries, i.e. from multiple blogs """
        root = Node.root()
        n1 = root.add("b1")
        n2 = root.add("b2")
        n3 = root.add("b3")
        ## blog state is actually ignored!
        _ = ValveBlog(node=n1, state="published").save()
        _ = ValveBlog(node=n2, state="published").save()
        _ = ValveBlog(node=n3, state="published").save()
        _ = ValveEntry(node=n1.add("e1"), state="published").save()
        _ = ValveEntry(node=n2.add("e2"), state="published").save()
        _ = ValveEntry(node=n3.add("e3"), state="published").save()

        request = create_request("GET", "/", data={})

        handler = MainHandlerTestable(request=request, instance=root)
        ctx = blog_context(handler, request, root)

        assert 'paginator' in ctx
        res = ctx['paginator'].object_list
        assert len(res) == 3
        assert set(x.slug() for x in res) == set(("e1", "e2", "e3"))

    def test_allblogs(self, client):
        """ in a global context (i.e. not directly on a blog instance) we
            want a list of all underlying (published) blogs for proper rss
            feed linking """
        root = Node.root()
        n1 = root.add("b1")
        n2 = root.add("b2")
        n3 = root.add("b3")
        
        _ = ValveBlog(node=n1, state="published").save()
        _ = ValveBlog(node=n2, state="private").save()
        _ = ValveBlog(node=n3, state="published").save()

        request = create_request("GET", "/", data={})

        handler = MainHandlerTestable(request=request, instance=root)
        ctx = global_blog_context(handler, request, root)

        res = ctx['all_blogs']
        assert res.count() == 2
        assert set(x.node.slug() for x in res) == set(("b1", "b3"))
